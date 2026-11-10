"""Configuration for OpenSSF Security Insights metadata."""

from pathlib import Path
from typing import Any, override

from pyrig.rig.configs.base.yaml import YMLDictConfigFile


class SecurityInsightsConfigFile(YMLDictConfigFile):
    """Manage project Security Insights metadata."""

    @override
    def parent_path(self) -> Path:
        """Return the project root."""
        return Path()

    @override
    def stem(self) -> str:
        """Return `security-insights`."""
        return "security-insights"

    @override
    def _configs(self) -> dict[str, Any]:
        """Return an empty configuration."""
        return {}
