"""Configuration for OpenSSF Security Insights metadata."""

from datetime import UTC, datetime
from operator import itemgetter
from pathlib import Path
from typing import Any, override

from pyrig.core.iterate import deep_sorted_dict
from pyrig.rig.configs.base.yaml import YMLDictConfigFile, commented_map
from pyrig.rig.configs.community.code_of_conduct import CodeOfConductConfigFile
from pyrig.rig.configs.community.contributing import ContributingConfigFile
from pyrig.rig.configs.community.license import LicenseConfigFile
from pyrig.rig.configs.community.security import SecurityConfigFile
from pyrig.rig.configs.pyproject import PyprojectConfigFile
from pyrig.rig.configs.readme import ReadmeConfigFile
from pyrig.rig.configs.version_control.hooks.manager import (
    VersionControlHookManagerConfigFile,
)
from pyrig.rig.configs.version_control.remote.dependency_bot import (
    DependencyBotConfigFile,
)
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
from pyrig.rig.tools.linting.yaml import YAMLLinter
from pyrig.rig.tools.packages.manager import PackageManager
from pyrig.rig.tools.security.checker import SecurityChecker
from pyrig.rig.tools.security.ci_cd import CICDSecurityChecker
from pyrig.rig.tools.security.secrets import SecretsChecker
from pyrig.rig.tools.version_control.controller import VersionController
from pyrig.rig.tools.version_control.remote.controller import RemoteVersionController

from pyrig_openssf.rig.configs.version_control.remote.workflows.security_practices import (  # noqa: E501
    SecurityPracticesWorkflowConfigFile,
)
from pyrig_openssf.rig.tools.security.practices import SecurityPracticesChecker


class SecurityInsightsConfigFile(YMLDictConfigFile):
    """Generate Security Insights metadata using overridable project defaults."""

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
        """Assemble the Security Insights configuration."""
        configs = deep_sorted_dict(
            {
                "header": self.header(),
                "project": self.project(),
                "repository": self.repository(),
            },
        )
        return commented_map(
            configs,
            comments={},
            comments_before={
                next(iter(configs.keys())): YAMLLinter.I.disable_line_length(
                    line=False,
                ),
            },
        )

    def header(self) -> dict[str, Any]:
        """Generate the header metadata section."""
        existing_header = self.safe_load().get("header", {})
        today = datetime.now(UTC).date().isoformat()
        return {
            "last-reviewed": existing_header.get("last-reviewed", today),
            "last-updated": existing_header.get("last-updated", today),
            "schema-version": "2.2.0",
            "url": RemoteVersionController.I.file_url(self.path()),
        }

    def project(self) -> dict[str, Any]:
        """Build the project metadata section."""
        return {
            "administrators": [self.administrator()],
            "name": PackageManager.I.project_name(),
            "homepage": RemoteVersionController.I.repo_url(),
            "repositories": [
                {
                    "name": PackageManager.I.project_name(),
                    "comment": PyprojectConfigFile.I.project_description(),
                    "url": RemoteVersionController.I.repo_url(),
                },
            ],
            "documentation": self.project_documentation(),
            "vulnerability-reporting": self.vulnerability_reporting(),
        }

    def repository(self) -> dict[str, Any]:
        """Build the repository metadata section."""
        return {
            "status": "active",
            "url": RemoteVersionController.I.repo_url(),
            "accepts-change-request": True,
            "accepts-automated-change-request": True,
            "bug-fixes-only": False,
            "no-third-party-packages": False,
            "core-team": self.core_team(),
            "license": self.license(),
            "documentation": self.repository_documentation(),
            "release": self.release(),
            "security": self.security(),
        }

    def core_team(self) -> list[dict[str, Any]]:
        """Build the core team contact list."""
        administrator: dict[str, Any] = self.administrator()
        maintainers = (
            {**maintainer, "primary": False}
            for maintainer in PyprojectConfigFile.I.maintainers()
            if maintainer["name"] != administrator["name"]
        )
        return [administrator, *maintainers]

    def license(self) -> dict[str, Any]:
        """Declare the repository license."""
        return {
            "url": RemoteVersionController.I.file_url(LicenseConfigFile.I.path()),
            "expression": LicenseConfigFile.I.spdx_identifier(),
        }

    def project_documentation(self) -> dict[str, Any]:
        """Declare links to generated project documentation."""
        return {
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

    def release(self) -> dict[str, Any]:
        """Describe releases and distribution channels."""
        return {
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

    def repository_documentation(self) -> dict[str, Any]:
        """Declare links to generated repository policies."""
        return {
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

    def security(self) -> dict[str, Any]:
        """Build the repository security section."""
        return {
            "champions": self.security_champions(),
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
            "tools": sorted(self.security_tools(), key=itemgetter("name")),
        }

    def vulnerability_reporting(self) -> dict[str, Any]:
        """Describe vulnerability reporting."""
        return {
            "contact": self.administrator(),
            "reports-accepted": True,
            "bug-bounty-available": False,
            "policy": RemoteVersionController.I.file_url(SecurityConfigFile.I.path()),
            "in-scope": ["Vulnerabilities in this project's own code."],
            "out-of-scope": ["Report dependency vulnerabilities to that project."],
        }

    def security_champions(self) -> list[dict[str, Any]]:
        """Build the security champion contact list."""
        return [self.administrator()]

    def security_tools(self) -> list[dict[str, Any]]:
        """Describe security tools and their integrations."""
        pyproject_url = RemoteVersionController.I.file_url(PyprojectConfigFile.I.path())
        pre_commit_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        return [
            {
                "name": SecurityChecker.I.name(),
                "type": "SAST",
                "rulesets": [
                    pyproject_url,
                    pre_commit_url,
                ],
                "integration": {"adhoc": True, "ci": True, "release": True},
                "results": {},
            },
            {
                "name": SecretsChecker.I.name(),
                "type": "secret",
                "rulesets": [
                    pyproject_url,
                    pre_commit_url,
                ],
                "integration": {"adhoc": True, "ci": True, "release": True},
                "results": {},
            },
            {
                "name": CICDSecurityChecker.I.name(),
                "type": "SAST",
                "rulesets": [
                    pyproject_url,
                    pre_commit_url,
                ],
                "integration": {"adhoc": True, "ci": True, "release": True},
                "results": {},
            },
            {
                "name": PackageManager.I.name(),
                "type": "SCA",
                "rulesets": [
                    pyproject_url,
                    pre_commit_url,
                ],
                "integration": {"adhoc": True, "ci": True, "release": True},
                "results": {},
            },
            {
                "name": SecurityPracticesChecker.I.name(),
                "type": "other",
                "rulesets": [
                    RemoteVersionController.I.file_url(
                        SecurityPracticesWorkflowConfigFile.I.path(),
                    ),
                ],
                "integration": {"adhoc": True, "ci": True, "release": True},
                "results": {},
            },
            {
                "name": "Dependabot",
                "type": "SCA",
                "rulesets": [
                    RemoteVersionController.I.file_url(
                        DependencyBotConfigFile.I.path(),
                    ),
                ],
                "integration": {"adhoc": True, "ci": False, "release": False},
                "results": {},
            },
        ]

    def administrator(self) -> dict[str, Any]:
        """Build the primary administrator contact."""
        return {
            "name": VersionController.I.repo_owner(),
            "primary": True,
            "email": PyprojectConfigFile.I.maintainer_email(),
            "social": RemoteVersionController.I.profile_url(),
        }
