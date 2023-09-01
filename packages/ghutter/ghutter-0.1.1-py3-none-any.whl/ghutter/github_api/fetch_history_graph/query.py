from abc import ABC
from typing import List

from gql import gql
from gql.transport.exceptions import TransportQueryError, TransportServerError
from pydantic import BaseModel

from ghutter.github_api.base import BaseQuery
from ghutter.github_api.exceptions import (
    GitHubApiException,
    RepositoryNotFoundException,
    UnauthorizedException,
)
from ghutter.utils.helpers import sha_2_short_sha


class PageInfo(BaseModel):
    hasNextPage: bool
    endCursor: str | None


class BaseCommit(BaseModel, ABC):
    oid: str

    @property
    def short_sha(self) -> str:
        return sha_2_short_sha(self.oid)


class ParentCommit(BaseCommit):
    pass


class Parents(BaseModel):
    pageInfo: PageInfo
    nodes: List[ParentCommit]


class Commit(BaseCommit):
    parents: Parents


class History(BaseModel):
    pageInfo: PageInfo
    nodes: List[Commit]


class RootCommit(BaseModel):
    history: History


class BranchRef(BaseModel):
    name: str
    target: RootCommit


class Repository(BaseModel):
    defaultBranchRef: BranchRef


class QueryResponse(BaseModel):
    repository: Repository


class FetchHistoryQuery(BaseQuery):
    """
    Raw gql query to fetch the history of a repository
    """

    repositoryOwner: str
    repository: str
    limit: int = 50
    after: str | None = None

    _QUERY = gql(
        """
            query($repositoryOwner: String!, $repository: String!, $limit: Int!, $after: String) {
              repository(owner: $repositoryOwner, name: $repository) {
                defaultBranchRef {
                  name
                  target {
                    ... on Commit {
                      history(first: $limit, after: $after) {
                        pageInfo {
                          hasNextPage
                          endCursor
                        }
                        nodes {
                          ... on Commit {
                            ...commitFields
                            parents(first:100) {
                              pageInfo {
                                hasNextPage
                                endCursor
                              }
                              nodes {
                                ...commitFields
                              }
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
            fragment commitFields on Commit {
              oid
            }
        """
    )

    def __call__(self) -> QueryResponse:
        try:
            variables = self.model_dump()
            response = self.client.execute(self._QUERY, variable_values=variables)
            return QueryResponse(**response)
        except TransportQueryError as e:
            if e.errors[0]["type"] == "NOT_FOUND":
                raise RepositoryNotFoundException() from e

            raise GitHubApiException(e.errors) from e
        except TransportServerError as e:
            if e.code == 401:
                raise UnauthorizedException() from e

            raise GitHubApiException(e.code) from e
