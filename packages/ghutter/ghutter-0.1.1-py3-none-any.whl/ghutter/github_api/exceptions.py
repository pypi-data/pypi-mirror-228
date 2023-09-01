class GitHubApiException(Exception):
    """Base exception for all GitHubApi exceptions."""


class UnauthorizedException(GitHubApiException):
    """Raised when the GitHub API returns 401."""


class RepositoryNotFoundException(GitHubApiException):
    """Raised when the GitHub API returns 'NOT_FOUND' error."""
