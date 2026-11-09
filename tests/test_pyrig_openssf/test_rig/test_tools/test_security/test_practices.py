"""Scorecard tool tests."""

from pyrig.rig.tools.base.tool import Group
from pyrig.rig.tools.version_control.remote.controller import RemoteVersionController

from pyrig_openssf.rig.tools.security.practices import SecurityPracticesChecker


class TestSecurityPracticesChecker:
    """Test Scorecard tool metadata."""

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
