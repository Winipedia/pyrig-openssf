"""Tests for OpenSSF Security Insights configuration."""

from datetime import UTC, datetime
from io import StringIO
from operator import itemgetter
from pathlib import Path

import requests
from pyrig.rig.configs.community.code_of_conduct import CodeOfConductConfigFile
from pyrig.rig.configs.community.contributing import ContributingConfigFile
from pyrig.rig.configs.community.license import LicenseConfigFile
from pyrig.rig.configs.community.security import SecurityConfigFile
from pyrig.rig.configs.pyproject import PyprojectConfigFile
from pyrig.rig.configs.readme import ReadmeConfigFile
from pyrig.rig.configs.version_control.remote.workflows.deploy import (
    DeployWorkflowConfigFile,
)
from pyrig.rig.configs.version_control.remote.workflows.health_check import (
    HealthCheckWorkflowConfigFile,
)
from pyrig.rig.configs.version_control.remote.workflows.release import (
    ReleaseWorkflowConfigFile,
)
from pyrig.rig.tools.docs.builder import DocsBuilder
from pyrig.rig.tools.packages.manager import PackageManager
from pyrig.rig.tools.version_control.controller import VersionController
from pyrig.rig.tools.version_control.remote.controller import RemoteVersionController

from pyrig_openssf.rig.configs.security_insights import SecurityInsightsConfigFile


def test_using_latest_schema_version() -> None:
    """Test that the header uses the latest schema version."""
    response = requests.get(
        "https://api.github.com/repos/ossf/security-insights/releases/latest",
        timeout=30,
    )
    latest_version = response.json()["tag_name"].removeprefix("v")
    header_version = SecurityInsightsConfigFile.I.header()["schema-version"]
    assert header_version == latest_version


class TestSecurityInsightsConfigFile:
    """Test Security Insights configuration."""

    def test__configs(self) -> None:
        """Test section assembly and file-wide line-length suppression."""
        config = SecurityInsightsConfigFile.I
        configs = config._configs()  # noqa: SLF001
        assert configs["header"]
        assert configs["project"]
        assert configs["repository"]
        output = StringIO()
        config.dumper().dump(configs, output)
        assert output.getvalue().startswith(
            '---\n# ryl disable rule:line-length\n"header":\n',
        )

    def test_administrator(self) -> None:
        """Test the primary administrator's identity and contact details."""
        assert SecurityInsightsConfigFile.I.administrator() == {
            "name": VersionController.I.repo_owner(),
            "primary": True,
            "email": PyprojectConfigFile.I.maintainer_email(),
            "social": RemoteVersionController.I.profile_url(),
        }

    def test_core_team(self) -> None:
        """Test that the administrator precedes the remaining maintainers."""
        config = SecurityInsightsConfigFile.I
        administrator = config.administrator()
        assert config.core_team() == [
            administrator,
            *[
                {**maintainer, "primary": False}
                for maintainer in PyprojectConfigFile.I.maintainers()
                if maintainer["name"] != administrator["name"]
            ],
        ]

    def test_header(self) -> None:
        """Test schema metadata and preservation of existing dates."""
        config = SecurityInsightsConfigFile.I
        existing = config.safe_load().get("header", {})
        today = datetime.now(UTC).date().isoformat()
        assert config.header() == {
            "last-reviewed": existing.get("last-reviewed", today),
            "last-updated": existing.get("last-updated", today),
            "schema-version": "2.2.0",
            "url": RemoteVersionController.I.file_url(config.path()),
        }

    def test_license(self) -> None:
        """Test the license URL and SPDX expression."""
        assert SecurityInsightsConfigFile.I.license() == {
            "url": RemoteVersionController.I.file_url(LicenseConfigFile.I.path()),
            "expression": LicenseConfigFile.I.spdx_identifier(),
        }

    def test_parent_path(self) -> None:
        """Test that the configuration file is in the project root."""
        assert SecurityInsightsConfigFile.I.parent_path() == Path()

    def test_project(self) -> None:
        """Test project identity and section assembly."""
        config = SecurityInsightsConfigFile.I
        assert config.project() == {
            "administrators": [config.administrator()],
            "name": PackageManager.I.project_name(),
            "homepage": RemoteVersionController.I.repo_url(),
            "repositories": [
                {
                    "name": PackageManager.I.project_name(),
                    "comment": PyprojectConfigFile.I.project_description(),
                    "url": RemoteVersionController.I.repo_url(),
                },
            ],
            "documentation": config.project_documentation(),
            "vulnerability-reporting": config.vulnerability_reporting(),
        }

    def test_project_documentation(self) -> None:
        """Test links to project guides and policies."""
        assert SecurityInsightsConfigFile.I.project_documentation() == {
            "detailed-guide": DocsBuilder.I.documentation_url(),
            "quickstart-guide": RemoteVersionController.I.file_url(
                ReadmeConfigFile.I.path(),
            ),
            "code-of-conduct": RemoteVersionController.I.file_url(
                CodeOfConductConfigFile.I.path(),
            ),
            "release-process": RemoteVersionController.I.file_url(
                ReleaseWorkflowConfigFile.I.path(),
            ),
            "support-policy": RemoteVersionController.I.file_url(
                SecurityConfigFile.I.path(),
            ),
        }

    def test_release(self) -> None:
        """Test the release pipeline, distribution links, and changelog."""
        assert SecurityInsightsConfigFile.I.release() == {
            "automated-pipeline": True,
            "distribution-points": [
                {
                    "uri": RemoteVersionController.I.releases_url(),
                    "comment": "GitHub releases.",
                },
                {
                    "uri": RemoteVersionController.I.file_url(
                        DeployWorkflowConfigFile.I.path(),
                    ),
                    "comment": "Describes additional distribution points.",
                },
            ],
            "changelog": RemoteVersionController.I.releases_url(),
        }

    def test_repository(self) -> None:
        """Test repository defaults and section assembly."""
        config = SecurityInsightsConfigFile.I
        assert config.repository() == {
            "status": "active",
            "url": RemoteVersionController.I.repo_url(),
            "accepts-change-request": True,
            "accepts-automated-change-request": True,
            "bug-fixes-only": False,
            "no-third-party-packages": False,
            "core-team": config.core_team(),
            "license": config.license(),
            "documentation": config.repository_documentation(),
            "release": config.release(),
            "security": config.security(),
        }

    def test_repository_documentation(self) -> None:
        """Test links to contribution, review, and security policies."""
        assert SecurityInsightsConfigFile.I.repository_documentation() == {
            "contributing-guide": RemoteVersionController.I.file_url(
                ContributingConfigFile.I.path(),
            ),
            "review-policy": RemoteVersionController.I.file_url(
                ContributingConfigFile.I.path(),
            ),
            "security-policy": RemoteVersionController.I.file_url(
                SecurityConfigFile.I.path(),
            ),
        }

    def test_security(self) -> None:
        """Test the self-assessment, champions, and tool ordering."""
        config = SecurityInsightsConfigFile.I
        assert config.security() == {
            "champions": config.security_champions(),
            "assessments": {
                "self": {
                    "name": "Security controls",
                    "comment": (
                        "Changes require human review and are gated by automated "
                        "checks, including dependency vulnerability auditing, static "
                        "security analysis, and secret scanning."
                    ),
                    "evidence": RemoteVersionController.I.file_url(
                        HealthCheckWorkflowConfigFile.I.path(),
                    ),
                },
            },
            "tools": sorted(config.security_tools(), key=itemgetter("name")),
        }

    def test_security_champions(self) -> None:
        """Test that the administrator is the default security champion."""
        config = SecurityInsightsConfigFile.I
        assert config.security_champions() == [config.administrator()]

    def test_security_tools(self) -> None:
        """Test tool categories, integration defaults, and empty results."""
        tools = SecurityInsightsConfigFile.I.security_tools()
        assert {tool["name"]: tool["type"] for tool in tools} == {
            "bandit": "SAST",
            "detect-secrets": "secret",  # pragma: allowlist secret
            "zizmor": "SAST",
            "uv": "SCA",
            "scorecard": "other",
            "Dependabot": "SCA",
        }
        for tool in tools:
            assert tool["rulesets"]
            assert all(url.startswith("https://") for url in tool["rulesets"])
            assert tool["integration"] == {
                "adhoc": True,
                "ci": tool["name"] != "Dependabot",
                "release": tool["name"] != "Dependabot",
            }
            assert tool["results"] == {}

    def test_stem(self) -> None:
        """Test the configuration file stem."""
        assert SecurityInsightsConfigFile.I.stem() == "security-insights"

    def test_vulnerability_reporting(self) -> None:
        """Test reporting acceptance, bounty defaults, policy, and scope."""
        config = SecurityInsightsConfigFile.I
        assert config.vulnerability_reporting() == {
            "contact": config.administrator(),
            "reports-accepted": True,
            "bug-bounty-available": False,
            "policy": RemoteVersionController.I.file_url(SecurityConfigFile.I.path()),
            "in-scope": ["Vulnerabilities in this project's own code."],
            "out-of-scope": ["Report dependency vulnerabilities to that project."],
        }
