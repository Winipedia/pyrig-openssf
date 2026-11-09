"""OpenSSF Scorecard identity and repository security assessment badges."""

from typing import override
from urllib.parse import urlencode

from pyrig.rig.tools.base.tool import Group, Tool
from pyrig.rig.tools.version_control.remote.controller import RemoteVersionController


class SecurityPracticesChecker(Tool):
    """Represent Scorecard and display related OpenSSF assessment badges."""

    @override
    def badges(self) -> tuple[tuple[str, str, str, str], ...]:
        """Return Scorecard, Best Practices, and Baseline badge metadata."""
        return (*super().badges(), self.badge_best_practices(), self.badge_baseline())

    @override
    def dev_dependencies(self) -> tuple[str, ...]:
        """Return no dev dependencies because Scorecard runs in GitHub Actions."""
        return ()

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

    @override
    def group(self) -> str:
        """Return the project-status badge group."""
        return Group.PROJECT_STATUS

    def badge_baseline(self) -> tuple[str, str, str, str]:
        """Return the repository's Baseline badge and assessment link."""
        return (
            self.group(),
            self.project_url("baseline"),
            self.project_url(),
            "Baseline",
        )

    def badge_best_practices(self) -> tuple[str, str, str, str]:
        """Return the repository's Best Practices badge and assessment link."""
        return (
            self.group(),
            self.project_url("badge"),
            self.project_url(),
            "Best Practices",
        )

    def project_url(self, as_: str = "entry") -> str:
        """Return an OpenSSF project lookup URL without requiring a project ID."""
        query = urlencode({"as": as_, "url": RemoteVersionController.I.repo_url()})
        return f"https://www.bestpractices.dev/en/projects?{query}"
