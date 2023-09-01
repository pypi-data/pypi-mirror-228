from logging import getLogger
from typing import Iterator, Tuple

from pydantic import BaseModel

from ghutter.github_api.fetch_history_graph.query import FetchHistoryQuery

LOGGER = getLogger(__package__)


class FetchHistoryGraph(BaseModel):
    token: str
    repositoryOwner: str
    repository: str
    maxCommits: int | None = None

    def __call__(self) -> Iterator[Tuple[str, str]]:
        query = FetchHistoryQuery(**self.model_dump())

        commit_counter = 0

        while True:
            if self.maxCommits == commit_counter:
                break

            if self.maxCommits is not None and query.limit + self.maxCommits > commit_counter:
                query.limit = min(self.maxCommits - commit_counter, 100)  # 100 is GitHub API pagination limit

            response = query()

            for i in response.repository.defaultBranchRef.target.history.nodes:
                for j in i.parents.nodes:
                    yield i.oid, j.oid

                if i.parents.pageInfo.hasNextPage:
                    # TODO remove this small limitation
                    LOGGER.warning(
                        f"Commit {i.short_sha} parents exceeds the max number of allowed, "
                        f"skipping the rest of the parents"
                    )

            commit_counter += len(response.repository.defaultBranchRef.target.history.nodes)

            if not response.repository.defaultBranchRef.target.history.pageInfo.hasNextPage:
                break

            query.after = response.repository.defaultBranchRef.target.history.pageInfo.endCursor
