import re
from argparse import Action, ArgumentError, ArgumentParser
from pathlib import Path
from typing import List, Self

from pydantic import BaseModel

import ghutter

REGEX_REPOSITORY = re.compile(
    r"^(https?://github.com/)?(?P<owner>[^\/\.]+)\/(?P<repo>[^\/\.]+)(\.git)?$", re.IGNORECASE
)


class Arguments(BaseModel):
    repositoryOwner: str
    repository: str
    token: str
    maxCommits: int | None = None
    drawOutput: List[Path] | None = None
    dotOutput: Path

    class _RepositoryAction(Action):
        def __call__(self, parser, namespace, value, option_string=None):
            match = REGEX_REPOSITORY.match(value)
            if not match:
                raise ArgumentError(self, f"invalid repository {value}")
            setattr(namespace, "repository", match.group("repo"))
            setattr(namespace, "repositoryOwner", match.group("owner"))

    @classmethod
    def parse_arguments(cls) -> Self:
        parser = ArgumentParser(
            prog=f"python -m {ghutter.__package__}",
            description="'GHutter' is a tool to recreate the history graph of a GitHub repository "
            "in Graphviz's Dot Language",
        )

        parser.add_argument(
            "repository", help='github repository in format "owner/repository" or url', action=cls._RepositoryAction
        )
        parser.add_argument("-t", "--token", help="github personal access token")
        parser.add_argument(
            "--max-commits",
            help="max number of commits to fetch from the history. "
            "If it is omitted it tries to fetch the whole history (parents will always be shown)",
            type=int,
            dest="maxCommits",
        )
        parser.add_argument(
            "-d",
            "--dot-output",
            help="graph dot file output path (default 'history.dot')",
            type=Path,
            default="history.dot",
            dest="dotOutput",
        )
        parser.add_argument(
            "-o",
            "--draw-output",
            help="graph render output path (there may be several). "
            "Check 'Graphviz' supported formats on your system",
            action="append",
            type=Path,
            dest="drawOutput",
        )

        return cls(**parser.parse_args().__dict__)
