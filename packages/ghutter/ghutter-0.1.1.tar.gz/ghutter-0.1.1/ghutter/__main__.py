from logging import getLogger

import networkx as nx

from ghutter.github_api.exceptions import (
    GitHubApiException,
    RepositoryNotFoundException,
    UnauthorizedException,
)
from ghutter.github_api.fetch_history_graph import FetchHistoryGraph
from ghutter.utils.arguments import Arguments

LOGGER = getLogger(__package__)


def main():
    args = Arguments.parse_arguments()

    graph = nx.DiGraph()

    try:
        fetch = FetchHistoryGraph(**args.model_dump())
        result = fetch()

        for i, j in result:
            graph.add_edge(i, j)

    except UnauthorizedException:
        LOGGER.fatal("GitHub api returned 401, please check your token")
        exit(1)
    except RepositoryNotFoundException:
        LOGGER.fatal("Repository not found, please check the repository name")
        exit(1)
    except GitHubApiException as e:
        LOGGER.fatal(f"GitHub api error {e}")
        exit(1)

    try:
        nx.find_cycle(graph)
        LOGGER.error("The history graph contains a cycle, are you sure this is a valid git repository?")
    except nx.NetworkXNoCycle:
        pass

    try:
        graph_dot = nx.nx_agraph.to_agraph(graph)
        graph_dot.write(args.dotOutput)

        if args.drawOutput:
            for o in args.drawOutput:
                graph_dot.draw(o, prog="dot")

    except ImportError:
        LOGGER.fatal("Unable to find graphviz, please install it and try again.")
        exit(1)


if __name__ == "__main__":
    main()
