from functools import cached_property
from typing import Annotated

from gql import Client
from gql.transport.aiohttp import AIOHTTPTransport
from pydantic import BaseModel, Field


class BaseQuery(BaseModel):
    token: Annotated[str, Field(exclude=True)]

    @cached_property
    def client(self):
        transport = AIOHTTPTransport(
            url="https://api.github.com/graphql", headers={"Authorization": f"bearer {self.token}"}
        )
        return Client(transport=transport, fetch_schema_from_transport=True)
