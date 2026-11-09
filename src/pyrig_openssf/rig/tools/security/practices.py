"""OpenSSF Scorecard tool identity and published assessment badge."""

from typing import override

from pyrig.rig.tools.base.tool import Group, Tool
from pyrig.rig.tools.version_control.remote.controller import RemoteVersionController


class SecurityPracticesChecker(Tool):
    """Represent Scorecard, which runs through GitHub Actions."""

    @override
    def dev_dependencies(self) -> tuple[str, ...]:
        """Return no dev dependencies because Scorecard runs in GitHub Actions."""
        return ()

    @override
    def group(self) -> str:
        """Return the project-status badge group."""
        return Group.PROJECT_STATUS

    @override
    def image_url(self) -> str:
        """Return the repository's published Scorecard badge URL."""
        repository = RemoteVersionController.I.repository()
        return f"https://api.scorecard.dev/projects/github.com/{repository}/badge"

    @override
    def link_url(self) -> str:
        """Return the repository's public Scorecard assessment URL."""
        repository = RemoteVersionController.I.repository()
        return f"https://scorecard.dev/viewer/?uri=github.com/{repository}"

    @override
    def name(self) -> str:
        """Return the Scorecard executable name."""
        return "scorecard"
