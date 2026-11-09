"""OpenSSF tool and assessment badge tests."""

from urllib.parse import parse_qs, urlsplit

import pytest
from pyrig.rig.tools.base.tool import Group, Tool
from pyrig.rig.tools.version_control.remote.controller import RemoteVersionController

from pyrig_openssf.rig.tools.security.practices import SecurityPracticesChecker


class TestSecurityPracticesChecker:
    """Test Scorecard metadata and related OpenSSF assessment badges."""

    def test_badge_baseline(self) -> None:
        """Test method."""
        tool = SecurityPracticesChecker.I
        assert tool.badge_baseline() == (
            Group.PROJECT_STATUS,
            tool.project_url("baseline"),
            tool.project_url(),
            "Baseline",
        )

    def test_badge_best_practices(self) -> None:
        """Test method."""
        tool = SecurityPracticesChecker.I
        assert tool.badge_best_practices() == (
            Group.PROJECT_STATUS,
            tool.project_url("badge"),
            tool.project_url(),
            "Best Practices",
        )

    def test_badges(self) -> None:
        """Test method."""
        tool = SecurityPracticesChecker.I
        assert tool.badges() == (
            tool.badge(),
            tool.badge_best_practices(),
            tool.badge_baseline(),
        )
        assert all(
            badge in Tool.grouped_badges()[Group.PROJECT_STATUS]
            for _, badge in tool.badges_markdown()
        )

    def test_dev_dependencies(self) -> None:
        """Test method."""
        assert SecurityPracticesChecker.I.dev_dependencies() == ()

    def test_group(self) -> None:
        """Test method."""
        assert SecurityPracticesChecker.I.group() == Group.PROJECT_STATUS

    def test_image_url(self) -> None:
        """Test method."""
        repository = RemoteVersionController.I.repository()
        assert SecurityPracticesChecker.I.image_url() == (
            f"https://api.scorecard.dev/projects/github.com/{repository}/badge"
        )

    def test_link_url(self) -> None:
        """Test method."""
        repository = RemoteVersionController.I.repository()
        assert SecurityPracticesChecker.I.link_url() == (
            f"https://scorecard.dev/viewer/?uri=github.com/{repository}"
        )

    def test_name(self) -> None:
        """Test method."""
        assert SecurityPracticesChecker.I.name() == "scorecard"

    @pytest.mark.parametrize("as_", ["entry", "badge", "baseline"])
    def test_project_url(self, as_: str) -> None:
        """Test repository lookup encoding and the default assessment link."""
        repository_url = RemoteVersionController.I.repo_url()
        tool = SecurityPracticesChecker.I
        url = tool.project_url(as_)
        assert url.startswith("https://www.bestpractices.dev/en/projects?as=")
        assert parse_qs(urlsplit(url).query) == {
            "as": [as_],
            "url": [repository_url],
        }
        assert "%3A%2F%2F" in url
        assert tool.project_url() == tool.project_url("entry")
