import re
from enum import Enum
from typing import List, Tuple

from lupin_grognard.core.commit.commit import Commit
from lupin_grognard.core.commit.commit_error import BodyError, ErrorCount
from lupin_grognard.core.commit.commit_reporter import CommitReporter
from lupin_grognard.core.config import (
    COMMIT_TYPE_MUST_HAVE_SCOPE,
    COMMIT_TYPE_MUST_NOT_HAVE_SCOPE,
    COMMIT_WITH_SCOPE,
    INITIAL_COMMIT,
    JAMA_REGEX,
    MAIN_BRANCHES_LIST,
    MAX_COMMIT_DESCR_LINES,
    MIN_COMMIT_DESCR_LENTH,
    PATTERN,
    TITLE_FAILED,
)


class CommitCheckModes(Enum):
    # Check all commits starting from the initial commit
    CHECK_ALL_COMMITS = 1
    # Check all commits of the current branch (until the last merge)
    CHECK_CURRENT_BRANCH_ONLY = 2


def define_commits_check_mode(
    current_branch: str, ci_mr_target_branch: str, CHECK_ALL_COMMITS_flag: bool
) -> CommitCheckModes:
    if (
        current_branch in MAIN_BRANCHES_LIST
        or ci_mr_target_branch in MAIN_BRANCHES_LIST
        or CHECK_ALL_COMMITS_flag
    ):
        return CommitCheckModes.CHECK_ALL_COMMITS
    else:
        return CommitCheckModes.CHECK_CURRENT_BRANCH_ONLY


def define_permissive_mode(
    check_mode: CommitCheckModes,
    permissive_mode: bool,
) -> bool:
    """
    Ensures that permissive mode can be enabled on a CommitCheckModes.CHECK_ALL_COMMITS
    if the --permissive flag is specified.

    Args:
        check_mode (CommitCheckModes): The check mode.
        permissive_mode (bool): The permissive flag.
    """
    if check_mode == CommitCheckModes.CHECK_ALL_COMMITS and permissive_mode is True:
        return True
    else:
        return False


class CommitValidator(Commit):
    def __init__(
        self,
        commit: Commit,
        error_counter: ErrorCount,
        check_mode: CommitCheckModes,
        no_jama: bool = False,
        no_approvers: bool = False,
    ):
        super().__init__(commit=commit.commit)
        self.reporter = CommitReporter(commit=commit)
        self.error_counter = error_counter
        self.check_mode = check_mode
        self.no_jama = no_jama
        self.no_approvers = no_approvers

    def perform_checks(self) -> None:
        if self.check_mode == CommitCheckModes.CHECK_ALL_COMMITS:
            if self._is_merge_commit(self.title):
                if not self.no_approvers:
                    if not self._validate_commit_merge():
                        self.error_counter.increment_merge_error()
                else:
                    self.reporter.display_merge_report_with_no_approver_option()
            else:
                if not self._validate_commit_title():
                    self.error_counter.increment_title_error()
                if not self._validate_body():
                    self.error_counter.increment_body_error()

        if self.check_mode == CommitCheckModes.CHECK_CURRENT_BRANCH_ONLY:
            if not self._validate_commit_title():
                self.error_counter.increment_title_error()
            if not self._is_merge_commit(self.title):
                if not self._validate_body():
                    self.error_counter.increment_body_error()

    def _validate_commit_title(self) -> bool:
        if self._validate_commit_message(self.title, self.type, self.scope):
            self.reporter.display_valid_title_report()
            return True
        else:
            return False

    def _validate_body(self) -> bool:
        body_error = BodyError(
            is_conventional=[],
            descr_is_too_short=[],
            num_empty_line=0,
            invalid_body_length=False,
            jama_not_referenced=False,
            duplicate_jama_line=False,
            duplicate_jama_refs=[],
            invalid_jama_refs=False,
        )

        if self.is_major_commit():
            if not self.no_jama:
                self._validate_jama_referencing(body_error=body_error)

        if self.body:
            if not self._is_commit_body_length_valid():
                body_error.invalid_body_length = True

            for message in self.body:
                if self._is_conventional_commit_body_valid(message=message):
                    body_error.is_conventional.append(
                        message
                    )  # must not start with a conventional message
                if not self._is_commit_body_line_length_valid(message=message):
                    if message != "":
                        body_error.descr_is_too_short.append(message)
                    else:
                        body_error.num_empty_line += 1
        if any(
            [
                body_error.is_conventional,
                body_error.descr_is_too_short,
                body_error.num_empty_line > 0,
                body_error.invalid_body_length,
                body_error.jama_not_referenced,
                body_error.duplicate_jama_line,
                body_error.duplicate_jama_refs,
                body_error.invalid_jama_refs,
            ]
        ):
            self.reporter.display_body_report(body_error=body_error)
            return False
        return True

    def _check_only_one_line_references_jama_items(self):
        """Checks whether the body contains several lines referencing jama"""
        jama_ref_count = 0
        for line in self.body:
            if line.startswith("JAMA:"):
                jama_ref_count += 1
                if jama_ref_count > 1:
                    return False
        return True

    def _validate_jama_referencing(self, body_error: BodyError) -> None:
        """
        Validate JAMA referencing in the body text

        - Check if the last description line starts with 'JAMA:'
        - Check if any other line starts with 'JAMA:'
        - Check if the signature line starts with a valid JAMA reference
        - Validate individual JAMA items by detecting duplicates and invalid references
        """
        if not self.is_last_description_line_starting_with_jama():
            body_error.jama_not_referenced = True
        else:
            if not self._check_only_one_line_references_jama_items():
                body_error.duplicate_jama_line = True

        if (
            self.is_last_description_line_starting_with_jama()
            and self.title not in INITIAL_COMMIT
        ):
            (
                duplicate_jama_refs,
                invalid_jama_refs,
            ) = self._validate_jama_items()
            if duplicate_jama_refs:
                body_error.duplicate_jama_refs = duplicate_jama_refs
            if invalid_jama_refs:
                body_error.invalid_jama_refs = invalid_jama_refs

    def _validate_jama_items(self) -> Tuple[List[str], List[str]]:
        """
        Validate individual JAMA items
        - Check if the JAMA item matches the JAMA reference pattern defined by JAMA_REGEX
        - Check for duplicate JAMA items and record them
        - Check for invalid JAMA items and record them

        Returns:
            A tuple containing two lists:
            - duplicate_jama_refs (List[str]): List of duplicate JAMA items
            - invalid_jama_refs (List[str]): List of invalid JAMA items
        """
        jama_ref_line = self.body[-1]
        jama_refs = jama_ref_line.replace("JAMA:", "").strip().split(" ")
        unique_jama_refs = set()
        duplicate_jama_refs = []
        invalid_jama_refs = []

        for jama_ref in jama_refs:
            if not re.match(JAMA_REGEX, jama_ref):
                invalid_jama_refs.append(jama_ref)
            elif jama_ref in unique_jama_refs and jama_ref not in duplicate_jama_refs:
                duplicate_jama_refs.append(jama_ref)
            else:
                unique_jama_refs.add(jama_ref)
        return duplicate_jama_refs, invalid_jama_refs

    def _validate_commit_message(self, commit_msg: str, type: str, scope: str) -> bool:
        if self._is_special_commit(commit_msg=commit_msg):
            return True

        match type:
            case None:
                self.reporter.display_invalid_title_report(error_message=TITLE_FAILED)
                return False
            case match_type if (match_type := type) in COMMIT_WITH_SCOPE:
                return self._validate_commit_message_for_specific_type(
                    scope=scope, type=match_type
                )
            case _:
                return self._validate_commit_message_for_generic_type(
                    type=type, scope=scope
                )

    def _is_conventional_commit_body_valid(self, message: str) -> bool:
        """Checks if the line in the body of a commit message starts with a conventional commit"""
        return bool(re.match(PATTERN, message))

    def _is_commit_body_line_length_valid(self, message: str) -> bool:
        """Checks if the body line is not less than MIN_COMMIT_DESCR_LENTH"""
        return len(message) >= MIN_COMMIT_DESCR_LENTH

    def _is_commit_body_length_valid(self) -> bool:
        """Checks if the body length is not greater than MAX_COMMIT_DESCR_LINES"""
        return len(self.body) <= MAX_COMMIT_DESCR_LINES

    def _is_special_commit(self, commit_msg: str) -> bool:
        """Checks if the commit is a Merge or in the list of initial commits"""
        return commit_msg.startswith("Merge") or commit_msg in INITIAL_COMMIT

    def _is_merge_commit(self, commit_msg: str) -> bool:
        return commit_msg.startswith("Merge")

    def _validate_commit_merge(self) -> bool:
        if len(self.approvers) < 1:
            self.reporter.display_merge_report_no_approver()
            return False
        else:
            if not self._is_autor_different_from_approvers():
                self.reporter.display_merge_report_author_same_approver()
                return False
            else:
                self.reporter.display_valid_merge_report(approvers=self.approvers)
                return True

    def _validate_commit_message_for_specific_type(self, scope: str, type: str) -> bool:
        """
        Validates the scope for a COMMIT_WITH_SCOPE list.
        If the scope is (change) then the commit title and description
        must not contain the words 'remove' or 'removed'
        """
        if scope is None or scope not in ["(add)", "(change)", "(remove)"]:
            self.reporter.display_invalid_title_report(
                error_message=COMMIT_TYPE_MUST_HAVE_SCOPE.format(type=type)
            )
            return False
        else:
            if scope == "(change)":
                return self._validate_change_scope_without_remove_word()
            return True

    def _contains_remove_words(self, text: str) -> bool:
        """Checks if the text contains the words 'remove' or 'removed'"""
        words = text.lower().split(" ")
        return any(str in words for str in ["remove", "removed"])

    def _validate_change_scope_without_remove_word(self):
        """
        Validate that a commit with the scope (change) does not contain the words
        'remove' and 'removed' in the title or description
        """
        full_text = self.title + " " + " ".join(self.body) if self.body else self.title
        if self._contains_remove_words(text=full_text):
            self.reporter.display_invalid_title_report(
                error_message=(
                    "Found a commit message that talks about removing something while given "
                    "scope is 'change': change scope to 'remove' or update the commit description"
                )
            )
            return False
        return True

    def _validate_commit_message_for_generic_type(self, type, scope: str) -> bool:
        """Validates other commit types do not contain a scope"""
        if scope is None:
            return True
        else:
            error_message = COMMIT_TYPE_MUST_NOT_HAVE_SCOPE.format(type, type)
            self.reporter.display_invalid_title_report(error_message=error_message)
            return False

    def _is_autor_different_from_approvers(self) -> bool:
        for approver in self.approvers:
            approver_mail = approver.split(" ")[-1]
            if self.author_mail == approver_mail:
                return False
        return True
