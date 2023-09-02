from typing import Optional, Set, Literal, Union
import re
from .interface import RawCommit, Commit, CommitParser
from . import errors
from .types import InvalidCommitAction
from .utils import warn_or_raise


class AngularCommitParser(CommitParser):
    def __init__(
        self,
        invalid_commit_action: InvalidCommitAction = InvalidCommitAction.skip,
        skip_commit_patterns: Set[str] = set(),
        valid_scopes: Union[Set[str], Literal[':anyscope:']] = ':anyscope:',
    ):
        self.type_and_scope_pattern = re.compile(
            r'(?P<type>\w+)\(?(?P<scope>[a-zA-Z-_]*)\)?: .*'
        )
        self.breaking_pattern = re.compile(
            r'BREAKING CHANGE: .*', flags=re.DOTALL
        )
        self.invalid_commit_action = invalid_commit_action
        self.valid_scopes = valid_scopes
        self.skip_commit_patterns = skip_commit_patterns

    def parse(self, commit: RawCommit) -> Optional[Commit]:
        # Commits that parse as None will be skipped
        if self.should_skip_by_pattern(commit.title):
            return None

        m = self.type_and_scope_pattern.match(commit.title)
        if m is None:
            warn_or_raise(
                f'Invalid commit: {commit.sha} {commit.title}',
                self.invalid_commit_action,
                errors.InvalidCommitFormat,
            )
            return None

        return self._prepare_commit(
            m,
            commit.sha,
            bool(self.breaking_pattern.match(commit.body)),
            commit.title,
        )

    def _prepare_commit(
        self, m: re.Match, sha: str, breaking: bool, title: str
    ) -> Commit:
        type = m.group('type')
        scope = m.group('scope')
        if self.valid_scopes == ':anyscope:':
            scope = scope or ':global:'
        else:
            if scope:
                if scope not in self.valid_scopes:
                    warn_or_raise(
                        f'Invalid commit scope: {sha} {title}',
                        self.invalid_commit_action,
                        errors.InvalidCommitFormat,
                    )
            else:
                scope = ':global:'
        return Commit(sha=sha, type=type, scope=scope, breaking=breaking)

    def should_skip_by_pattern(self, title: str) -> bool:
        for pattern in self.skip_commit_patterns:
            if re.match(pattern, title):
                return True
        return False
