"""Tests for OpenSSF Security Insights configuration."""

from pathlib import Path

from pyrig_openssf.rig.configs.security_insights import SecurityInsightsConfigFile


class TestSecurityInsightsConfigFile:
    """Test Security Insights configuration."""

    def test__configs(self) -> None:
        """Test that no metadata is generated yet."""
        assert SecurityInsightsConfigFile.I._configs() == {}  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]

    def test_parent_path(self) -> None:
        """Test that the configuration file is in the project root."""
        assert SecurityInsightsConfigFile.I.parent_path() == Path()

    def test_stem(self) -> None:
        """Test the configuration file stem."""
        assert SecurityInsightsConfigFile.I.stem() == "security-insights"
