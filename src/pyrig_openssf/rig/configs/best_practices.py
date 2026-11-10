"""Configuration for OpenSSF Best Practices assessment answers."""

from collections.abc import Callable
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast, override

from pyrig.rig.configs.base.json import JSONDictConfigFile
from pyrig.rig.configs.community.code_of_conduct import CodeOfConductConfigFile
from pyrig.rig.configs.community.contributing import ContributingConfigFile
from pyrig.rig.configs.community.license import LicenseConfigFile
from pyrig.rig.configs.community.security import SecurityConfigFile
from pyrig.rig.configs.pyproject import PyprojectConfigFile
from pyrig.rig.configs.readme import ReadmeConfigFile
from pyrig.rig.configs.version_control.hooks.manager import (
    VersionControlHookManagerConfigFile,
)
from pyrig.rig.configs.version_control.ignore import VersionControllerIgnoreConfigFile
from pyrig.rig.configs.version_control.remote.codeowners import CodeownersConfigFile
from pyrig.rig.configs.version_control.remote.configure import (
    ConfigureRepositoryConfigFile,
)
from pyrig.rig.configs.version_control.remote.dependency_bot import (
    DependencyBotConfigFile,
)
from pyrig.rig.configs.version_control.remote.issue_templates.bug_report import (
    BugReportConfigFile,
)
from pyrig.rig.configs.version_control.remote.pull_request_template import (
    PullRequestTemplateConfigFile,
)
from pyrig.rig.configs.version_control.remote.settings import (
    RepositorySettingsConfigFile,
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
from pyrig.rig.tools.packages.manager import PackageManager
from pyrig.rig.tools.version_control.remote.controller import RemoteVersionController

from pyrig_openssf.rig.tools.security.practices import SecurityPracticesChecker

if TYPE_CHECKING:
    from types import MethodType


class BestPracticesConfigFile(JSONDictConfigFile):
    """Manage proposed Best Practices statuses and justifications."""

    @override
    def parent_path(self) -> Path:
        """Return the project root."""
        return Path()

    @override
    def stem(self) -> str:
        """Return `.bestpractices`."""
        return ".bestpractices"

    @override
    def _configs(self) -> dict[str, Any]:
        """Expand each justification into a met status and justification field."""
        return {
            key: value
            for method in sorted(
                self.justifications(),
                key=self.criterion_from_method,
            )
            for key, value in self.criterion_config(method).items()
        }

    def criterion_config(self, method: Callable[[], str]) -> dict[str, Any]:
        """Return the configuration for a specific criterion."""
        criterion = self.criterion_from_method(method)
        return {
            f"{criterion}_status": "Met",
            f"{criterion}_justification": method(),
        }

    def justifications(self) -> tuple[Callable[[], str], ...]:
        """Return the registered justification methods."""
        return (
            self.justification_accessibility_best_practices,
            self.justification_achieve_passing,
            self.justification_achieve_silver,
            self.justification_automated_integration_testing,
            self.justification_build,
            self.justification_build_common_tools,
            self.justification_build_floss_tools,
            self.justification_build_non_recursive,
            self.justification_build_preserve_debug,
            self.justification_build_repeatable,
            self.justification_build_reproducible,
            self.justification_code_of_conduct,
            self.justification_code_review_standards,
            self.justification_coding_standards,
            self.justification_coding_standards_enforced,
            self.justification_contribution,
            self.justification_contribution_requirements,
            self.justification_crypto_call,
            self.justification_crypto_certificate_verification,
            self.justification_crypto_keylength,
            self.justification_crypto_published,
            self.justification_crypto_random,
            self.justification_crypto_tls12,
            self.justification_crypto_used_network,
            self.justification_crypto_verification_private,
            self.justification_crypto_weaknesses,
            self.justification_crypto_working,
            self.justification_dependency_monitoring,
            self.justification_description_good,
            self.justification_delivery_mitm,
            self.justification_delivery_unsigned,
            self.justification_discussion,
            self.justification_documentation_achievements,
            self.justification_documentation_basics,
            self.justification_documentation_current,
            self.justification_documentation_interface,
            self.justification_documentation_quick_start,
            self.justification_dynamic_analysis,
            self.justification_dynamic_analysis_enable_assertions,
            self.justification_dynamic_analysis_fixed,
            self.justification_english,
            self.justification_external_dependencies,
            self.justification_floss_license,
            self.justification_floss_license_osi,
            self.justification_installation_common,
            self.justification_installation_development_quick,
            self.justification_installation_standard_variables,
            self.justification_interact,
            self.justification_interfaces_current,
            self.justification_know_common_errors,
            self.justification_know_secure_design,
            self.justification_license_location,
            self.justification_maintained,
            self.justification_no_leaked_credentials,
            self.justification_osps_ac_02_01,
            self.justification_osps_ac_03_01,
            self.justification_osps_ac_03_02,
            self.justification_osps_ac_04_01,
            self.justification_osps_ac_04_02,
            self.justification_osps_br_01_01,
            self.justification_osps_br_01_03,
            self.justification_osps_br_01_04,
            self.justification_osps_br_02_01,
            self.justification_osps_br_02_02,
            self.justification_osps_br_03_01,
            self.justification_osps_br_03_02,
            self.justification_osps_br_04_01,
            self.justification_osps_br_05_01,
            self.justification_osps_br_07_01,
            self.justification_osps_do_01_01,
            self.justification_osps_do_02_01,
            self.justification_osps_do_03_02,
            self.justification_osps_do_04_01,
            self.justification_osps_do_05_01,
            self.justification_osps_do_06_01,
            self.justification_osps_do_07_01,
            self.justification_osps_gv_01_01,
            self.justification_osps_gv_01_02,
            self.justification_osps_gv_02_01,
            self.justification_osps_gv_03_01,
            self.justification_osps_gv_03_02,
            self.justification_osps_le_01_01,
            self.justification_osps_le_02_01,
            self.justification_osps_le_02_02,
            self.justification_osps_le_03_01,
            self.justification_osps_le_03_02,
            self.justification_osps_qa_01_01,
            self.justification_osps_qa_01_02,
            self.justification_osps_qa_02_01,
            self.justification_osps_qa_03_01,
            self.justification_osps_qa_05_01,
            self.justification_osps_qa_05_02,
            self.justification_osps_qa_06_01,
            self.justification_osps_qa_06_02,
            self.justification_osps_qa_06_03,
            self.justification_osps_qa_07_01,
            self.justification_osps_sa_02_01,
            self.justification_osps_vm_01_01,
            self.justification_osps_vm_02_01,
            self.justification_osps_vm_03_01,
            self.justification_osps_vm_05_01,
            self.justification_osps_vm_05_02,
            self.justification_osps_vm_05_03,
            self.justification_osps_vm_06_01,
            self.justification_osps_vm_06_02,
            self.justification_regression_tests_added50,
            self.justification_release_notes,
            self.justification_repo_distributed,
            self.justification_repo_interim,
            self.justification_repo_public,
            self.justification_repo_track,
            self.justification_report_archive,
            self.justification_report_process,
            self.justification_report_responses,
            self.justification_report_tracker,
            self.justification_roles_responsibilities,
            self.justification_sites_https,
            self.justification_static_analysis,
            self.justification_static_analysis_common_vulnerabilities,
            self.justification_static_analysis_fixed,
            self.justification_static_analysis_often,
            self.justification_test,
            self.justification_test_branch_coverage80,
            self.justification_test_continuous_integration,
            self.justification_test_invocation,
            self.justification_test_most,
            self.justification_test_policy,
            self.justification_test_policy_mandated,
            self.justification_test_statement_coverage80,
            self.justification_test_statement_coverage90,
            self.justification_tests_are_added,
            self.justification_tests_documented_added,
            self.justification_two_person_review,
            self.justification_updateable_reused_components,
            self.justification_version_semver,
            self.justification_version_tags,
            self.justification_version_unique,
            self.justification_vulnerabilities_critical_fixed,
            self.justification_vulnerabilities_fixed_60_days,
            self.justification_vulnerability_report_private,
            self.justification_vulnerability_report_process,
            self.justification_vulnerability_report_response,
            self.justification_vulnerability_response_process,
            self.justification_warnings,
            self.justification_warnings_fixed,
            self.justification_warnings_strict,
        )

    def criterion_from_method(self, method: Callable[[], str]) -> str:
        """Return the criterion identifier from a named `justification_*` method."""
        return cast("MethodType", method).__name__.removeprefix("justification_")

    def justification_accessibility_best_practices(self) -> str:
        """Follow accessibility best practices for project sites and results."""
        repo_url = RemoteVersionController.I.repo_url()
        docs_url = DocsBuilder.I.documentation_url()
        return f"See {repo_url} and {docs_url}."

    def justification_achieve_passing(self) -> str:
        """Achieve the passing Best Practices badge."""
        url = SecurityPracticesChecker.I.project_url()
        return f"See {url}."

    def justification_achieve_silver(self) -> str:
        """Achieve the silver Best Practices badge."""
        url = SecurityPracticesChecker.I.project_url()
        return f"See {url}."

    def justification_automated_integration_testing(self) -> str:
        """Show that each check-in on a shared branch runs tests with results."""
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        release_url = RemoteVersionController.I.file_url(
            ReleaseWorkflowConfigFile.I.path(),
        )
        return f"See {health_url} and {release_url}."

    def justification_build(self) -> str:
        """Provide an automated build from source."""
        config_url = RemoteVersionController.I.file_url(
            PyprojectConfigFile.I.path(),
        )
        deploy_url = RemoteVersionController.I.file_url(
            DeployWorkflowConfigFile.I.path(),
        )
        return f"See {config_url} and {deploy_url}."

    def justification_build_common_tools(self) -> str:
        """Show that the project uses common build tools."""
        url = RemoteVersionController.I.file_url(PyprojectConfigFile.I.path())
        return f"See {url}."

    def justification_build_floss_tools(self) -> str:
        """Show that the project can be built with FLOSS tools."""
        url = RemoteVersionController.I.file_url(PyprojectConfigFile.I.path())
        return f"See {url}."

    def justification_build_non_recursive(self) -> str:
        """Avoid recursive builds across dependent subdirectories."""
        config_url = RemoteVersionController.I.file_url(
            PyprojectConfigFile.I.path(),
        )
        return f"See {config_url}."

    def justification_build_preserve_debug(self) -> str:
        """Preserve requested debugging information when building."""
        config_url = RemoteVersionController.I.file_url(
            PyprojectConfigFile.I.path(),
        )
        return f"See {config_url}."

    def justification_build_repeatable(self) -> str:
        """Produce bit-for-bit identical results on repeated builds."""
        config_url = RemoteVersionController.I.file_url(
            PyprojectConfigFile.I.path(),
        )
        return f"See {config_url}."

    def justification_build_reproducible(self) -> str:
        """Allow independent reproduction of identical build artifacts."""
        config_url = RemoteVersionController.I.file_url(
            PyprojectConfigFile.I.path(),
        )
        return f"See {config_url}."

    def justification_code_of_conduct(self) -> str:
        """Show that the project adopts and publishes a code of conduct."""
        url = RemoteVersionController.I.file_url(CodeOfConductConfigFile.I.path())
        return f"See {url}."

    def justification_code_review_standards(self) -> str:
        """Document code review requirements."""
        contributing_url = RemoteVersionController.I.file_url(
            ContributingConfigFile.I.path(),
        )
        owners_url = RemoteVersionController.I.file_url(
            CodeownersConfigFile.I.path(),
        )
        settings_url = RemoteVersionController.I.file_url(
            RepositorySettingsConfigFile.I.path(),
        )
        configure_url = RemoteVersionController.I.file_url(
            ConfigureRepositoryConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return (
            f"See {contributing_url}, {owners_url}, {settings_url}, "
            f"{configure_url}, and {health_url}."
        )

    def justification_coding_standards(self) -> str:
        """Show that contributions must follow defined coding standards."""
        config_url = RemoteVersionController.I.file_url(PyprojectConfigFile.I.path())
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        return f"See {config_url} and {hooks_url}."

    def justification_coding_standards_enforced(self) -> str:
        """Show that coding style is enforced automatically."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return f"See {hooks_url} and {health_url}."

    def justification_contribution(self) -> str:
        """Show that the contribution process is documented."""
        url = RemoteVersionController.I.file_url(ContributingConfigFile.I.path())
        return f"See {url}."

    def justification_contribution_requirements(self) -> str:
        """Show that acceptable contribution requirements are documented."""
        url = RemoteVersionController.I.file_url(ContributingConfigFile.I.path())
        return f"See {url}."

    def justification_crypto_call(self) -> str:
        """Delegate cryptographic operations to dedicated implementations."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return f"See {hooks_url} and {health_url}."

    def justification_crypto_certificate_verification(self) -> str:
        """Verify TLS certificates by default, including on subresources."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return f"See {hooks_url} and {health_url}."

    def justification_crypto_keylength(self) -> str:
        """Use sufficiently strong default keys and allow disabling weaker ones."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return f"See {hooks_url} and {health_url}."

    def justification_crypto_published(self) -> str:
        """Use publicly published, expert-reviewed cryptography by default."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return f"See {hooks_url} and {health_url}."

    def justification_crypto_random(self) -> str:
        """Generate cryptographic keys and nonces with secure randomness."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return f"See {hooks_url} and {health_url}."

    def justification_crypto_tls12(self) -> str:
        """Support TLS 1.2 or newer wherever TLS is used."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return f"See {hooks_url} and {health_url}."

    def justification_crypto_used_network(self) -> str:
        """Support secure networking and disable insecure protocols by default."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return f"See {hooks_url} and {health_url}."

    def justification_crypto_verification_private(self) -> str:
        """Verify TLS certificates before sending private HTTP information."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return f"See {hooks_url} and {health_url}."

    def justification_crypto_weaknesses(self) -> str:
        """Avoid algorithms and modes with known serious weaknesses."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return f"See {hooks_url} and {health_url}."

    def justification_crypto_working(self) -> str:
        """Avoid broken cryptography and context-inappropriate cipher modes."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return f"See {hooks_url} and {health_url}."

    def justification_delivery_mitm(self) -> str:
        """Show that software delivery counters man-in-the-middle attacks."""
        url = RemoteVersionController.I.releases_url()
        return f"See {url}."

    def justification_delivery_unsigned(self) -> str:
        """Do not trust unsigned cryptographic hashes retrieved over HTTP."""
        url = RemoteVersionController.I.releases_url()
        return f"See {url}."

    def justification_dependency_monitoring(self) -> str:
        """Monitor dependencies and address exploitable vulnerabilities."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        dependencies_url = RemoteVersionController.I.file_url(
            DependencyBotConfigFile.I.path(),
        )
        configure_url = RemoteVersionController.I.file_url(
            ConfigureRepositoryConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return (
            f"See {hooks_url}, {dependencies_url}, {configure_url}, and {health_url}."
        )

    def justification_description_good(self) -> str:
        """Show that the project explains what its software does."""
        readme_url = RemoteVersionController.I.file_url(ReadmeConfigFile.I.path())
        docs_url = DocsBuilder.I.documentation_url()
        return f"See {readme_url} and {docs_url}."

    def justification_discussion(self) -> str:
        """Provide searchable, addressable, open discussion channels."""
        issues_url = RemoteVersionController.I.issues_url()
        return f"See {issues_url}."

    def justification_documentation_achievements(self) -> str:
        """Keep published project achievements accurate and current."""
        readme_url = RemoteVersionController.I.file_url(
            ReadmeConfigFile.I.path(),
        )
        docs_url = DocsBuilder.I.documentation_url()
        return f"See {readme_url} and {docs_url}."

    def justification_documentation_basics(self) -> str:
        """Document installation, startup, usage, and safe operation."""
        readme_url = RemoteVersionController.I.file_url(
            ReadmeConfigFile.I.path(),
        )
        docs_url = DocsBuilder.I.documentation_url()
        return f"See {readme_url} and {docs_url}."

    def justification_documentation_current(self) -> str:
        """Keep documentation consistent with the software."""
        contributing_url = RemoteVersionController.I.file_url(
            ContributingConfigFile.I.path(),
        )
        deploy_url = RemoteVersionController.I.file_url(
            DeployWorkflowConfigFile.I.path(),
        )
        return f"See {contributing_url} and {deploy_url}."

    def justification_documentation_interface(self) -> str:
        """Document the software's external inputs and outputs."""
        docs_url = DocsBuilder.I.documentation_url()
        return f"See {docs_url}."

    def justification_documentation_quick_start(self) -> str:
        """Provide a quick introduction to useful software behavior."""
        readme_url = RemoteVersionController.I.file_url(
            ReadmeConfigFile.I.path(),
        )
        docs_url = DocsBuilder.I.documentation_url()
        return f"See {readme_url} and {docs_url}."

    def justification_dynamic_analysis(self) -> str:
        """Run qualifying dynamic analysis before major releases."""
        config_url = RemoteVersionController.I.file_url(
            PyprojectConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        release_url = RemoteVersionController.I.file_url(
            ReleaseWorkflowConfigFile.I.path(),
        )
        return f"See {config_url}, {health_url}, and {release_url}."

    def justification_dynamic_analysis_enable_assertions(self) -> str:
        """Exercise runtime assertions during dynamic analysis."""
        config_url = RemoteVersionController.I.file_url(
            PyprojectConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return f"See {config_url} and {health_url}."

    def justification_dynamic_analysis_fixed(self) -> str:
        """Promptly fix confirmed medium-or-higher dynamic-analysis findings."""
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        release_url = RemoteVersionController.I.file_url(
            ReleaseWorkflowConfigFile.I.path(),
        )
        return f"See {health_url} and {release_url}."

    def justification_english(self) -> str:
        """Show that documentation and bug reporting support English."""
        contributing_url = RemoteVersionController.I.file_url(
            ContributingConfigFile.I.path(),
        )
        report_url = RemoteVersionController.I.file_url(BugReportConfigFile.I.path())
        return f"See {contributing_url} and {report_url}."

    def justification_external_dependencies(self) -> str:
        """Show that dependencies are listed in a machine-readable format."""
        config_url = RemoteVersionController.I.file_url(PyprojectConfigFile.I.path())
        lock_url = RemoteVersionController.I.file_url(PackageManager.I.lock_file())
        return f"See {config_url} and {lock_url}."

    def justification_floss_license(self) -> str:
        """Show that the software is released under a FLOSS license."""
        url = RemoteVersionController.I.file_url(LicenseConfigFile.I.path())
        return f"See {url}."

    def justification_floss_license_osi(self) -> str:
        """Show that the software uses an OSI-approved license."""
        url = RemoteVersionController.I.file_url(LicenseConfigFile.I.path())
        return f"See {url}."

    def justification_installation_common(self) -> str:
        """Show that standard installation and uninstallation are supported."""
        url = RemoteVersionController.I.file_url(PyprojectConfigFile.I.path())
        return f"See {url}."

    def justification_installation_development_quick(self) -> str:
        """Show that developers can quickly set up the development environment."""
        url = RemoteVersionController.I.file_url(ContributingConfigFile.I.path())
        return f"See {url}."

    def justification_installation_standard_variables(self) -> str:
        """Honor standard installation variables where applicable."""
        config_url = RemoteVersionController.I.file_url(
            PyprojectConfigFile.I.path(),
        )
        return f"See {config_url}."

    def justification_interact(self) -> str:
        """Explain how to obtain, give feedback on, and contribute to the software."""
        readme_url = RemoteVersionController.I.file_url(
            ReadmeConfigFile.I.path(),
        )
        docs_url = DocsBuilder.I.documentation_url()
        contributing_url = RemoteVersionController.I.file_url(
            ContributingConfigFile.I.path(),
        )
        return f"See {readme_url}, {docs_url}, and {contributing_url}."

    def justification_interfaces_current(self) -> str:
        """Avoid deprecated interfaces in supported environments."""
        config_url = RemoteVersionController.I.file_url(
            PyprojectConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return f"See {config_url} and {health_url}."

    def justification_know_common_errors(self) -> str:
        """Have a primary developer who knows common errors and countermeasures."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return f"See {hooks_url} and {health_url}."

    def justification_know_secure_design(self) -> str:
        """Have a primary developer who understands secure-design principles."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        release_url = RemoteVersionController.I.file_url(
            ReleaseWorkflowConfigFile.I.path(),
        )
        return f"See {hooks_url}, {health_url} and {release_url}."

    def justification_license_location(self) -> str:
        """Show that the license is published in a standard repository location."""
        url = RemoteVersionController.I.file_url(LicenseConfigFile.I.path())
        return f"See {url}."

    def justification_maintained(self) -> str:
        """Keep the project maintained."""
        dependencies_url = RemoteVersionController.I.file_url(
            DependencyBotConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        repo_url = RemoteVersionController.I.repo_url()
        return f"See {dependencies_url}, {health_url}, and {repo_url}."

    def justification_no_leaked_credentials(self) -> str:
        """Keep valid credentials out of the public repository."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return f"See {hooks_url} and {health_url}."

    def justification_osps_ac_02_01(self) -> str:
        """Assign new collaborators' repository permissions manually."""
        repo_url = RemoteVersionController.I.repo_url()
        return f"See {repo_url}."

    def justification_osps_ac_03_01(self) -> str:
        """Prevent direct commits to the primary branch."""
        settings_url = RemoteVersionController.I.file_url(
            RepositorySettingsConfigFile.I.path(),
        )
        configure_url = RemoteVersionController.I.file_url(
            ConfigureRepositoryConfigFile.I.path(),
        )
        return f"See {settings_url} and {configure_url}."

    def justification_osps_ac_03_02(self) -> str:
        """Protect primary-branch deletion as a sensitive operation."""
        settings_url = RemoteVersionController.I.file_url(
            RepositorySettingsConfigFile.I.path(),
        )
        configure_url = RemoteVersionController.I.file_url(
            ConfigureRepositoryConfigFile.I.path(),
        )
        return f"See {settings_url} and {configure_url}."

    def justification_osps_ac_04_01(self) -> str:
        """Show that CI tasks default to the lowest permissions."""
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        release_url = RemoteVersionController.I.file_url(
            ReleaseWorkflowConfigFile.I.path(),
        )
        deploy_url = RemoteVersionController.I.file_url(
            DeployWorkflowConfigFile.I.path(),
        )
        return f"See {health_url}, {release_url}, and {deploy_url}."

    def justification_osps_ac_04_02(self) -> str:
        """Grant each CI task only the permissions it needs."""
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        release_url = RemoteVersionController.I.file_url(
            ReleaseWorkflowConfigFile.I.path(),
        )
        deploy_url = RemoteVersionController.I.file_url(
            DeployWorkflowConfigFile.I.path(),
        )
        return f"See {health_url}, {release_url}, and {deploy_url}."

    def justification_osps_br_01_01(self) -> str:
        """Validate untrusted input before using it in CI."""
        release_url = RemoteVersionController.I.file_url(
            ReleaseWorkflowConfigFile.I.path(),
        )
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return f"See {release_url}, {hooks_url}, and {health_url}."

    def justification_osps_br_01_03(self) -> str:
        """Keep privileged CI credentials away from untrusted code."""
        settings_url = RemoteVersionController.I.file_url(
            RepositorySettingsConfigFile.I.path(),
        )
        configure_url = RemoteVersionController.I.file_url(
            ConfigureRepositoryConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return f"See {settings_url}, {configure_url}, and {health_url}."

    def justification_osps_br_01_04(self) -> str:
        """Validate trusted collaborator input before using it in CI."""
        release_url = RemoteVersionController.I.file_url(
            ReleaseWorkflowConfigFile.I.path(),
        )
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return f"See {release_url}, {hooks_url}, and {health_url}."

    def justification_osps_br_02_01(self) -> str:
        """Show that every release receives a unique version identifier."""
        url = RemoteVersionController.I.file_url(
            ReleaseWorkflowConfigFile.I.path(),
        )
        return f"See {url}."

    def justification_osps_br_02_02(self) -> str:
        """Associate every release asset with a unique identifier."""
        config_url = RemoteVersionController.I.file_url(
            PyprojectConfigFile.I.path(),
        )
        release_url = RemoteVersionController.I.file_url(
            ReleaseWorkflowConfigFile.I.path(),
        )
        deploy_url = RemoteVersionController.I.file_url(
            DeployWorkflowConfigFile.I.path(),
        )
        return f"See {config_url}, {release_url}, and {deploy_url}."

    def justification_osps_br_03_01(self) -> str:
        """Deliver official project channels exclusively over encryption."""
        config_url = RemoteVersionController.I.file_url(
            PyprojectConfigFile.I.path(),
        )
        repo_url = RemoteVersionController.I.repo_url()
        docs_url = DocsBuilder.I.documentation_url()
        releases_url = RemoteVersionController.I.releases_url()
        return f"See {config_url}, {repo_url}, {docs_url}, and {releases_url}."

    def justification_osps_br_03_02(self) -> str:
        """Show that distribution uses cryptographically authenticated channels."""
        url = RemoteVersionController.I.releases_url()
        return f"See {url}."

    def justification_osps_br_04_01(self) -> str:
        """Describe functional and security modifications in every release."""
        release_url = RemoteVersionController.I.file_url(
            ReleaseWorkflowConfigFile.I.path(),
        )
        return f"See {release_url}."

    def justification_osps_br_05_01(self) -> str:
        """Show that pipelines use standard dependency management tools."""
        url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return f"See {url}."

    def justification_osps_br_07_01(self) -> str:
        """Show that mechanisms prevent accidental credential commits."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return f"See {hooks_url} and {health_url}."

    def justification_osps_do_01_01(self) -> str:
        """Provide guides for all basic functionality."""
        readme_url = RemoteVersionController.I.file_url(
            ReadmeConfigFile.I.path(),
        )
        docs_url = DocsBuilder.I.documentation_url()
        return f"See {readme_url} and {docs_url}."

    def justification_osps_do_02_01(self) -> str:
        """Show that defect reporting is documented."""
        url = RemoteVersionController.I.file_url(ContributingConfigFile.I.path())
        return f"See {url}."

    def justification_osps_do_03_02(self) -> str:
        """Document verification of the expected release author's identity."""
        settings_url = RemoteVersionController.I.file_url(
            RepositorySettingsConfigFile.I.path(),
        )
        configure_url = RemoteVersionController.I.file_url(
            ConfigureRepositoryConfigFile.I.path(),
        )
        release_url = RemoteVersionController.I.file_url(
            ReleaseWorkflowConfigFile.I.path(),
        )
        deploy_url = RemoteVersionController.I.file_url(
            DeployWorkflowConfigFile.I.path(),
        )
        return f"See {settings_url}, {configure_url}, {release_url}, and {deploy_url}."

    def justification_osps_do_04_01(self) -> str:
        """Document the scope and duration of release support."""
        security_url = RemoteVersionController.I.file_url(
            SecurityConfigFile.I.path(),
        )
        return f"See {security_url}."

    def justification_osps_do_05_01(self) -> str:
        """Show that the end of security support is documented."""
        url = RemoteVersionController.I.file_url(SecurityConfigFile.I.path())
        return f"See {url}."

    def justification_osps_do_06_01(self) -> str:
        """Document how dependencies are selected, obtained, and tracked."""
        config_url = RemoteVersionController.I.file_url(PyprojectConfigFile.I.path())
        lock_url = RemoteVersionController.I.file_url(PackageManager.I.lock_file())
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        return f"See {config_url}, {lock_url}, and {hooks_url}."

    def justification_osps_do_07_01(self) -> str:
        """Document build instructions and required dependencies."""
        config_url = RemoteVersionController.I.file_url(
            PyprojectConfigFile.I.path(),
        )
        deploy_url = RemoteVersionController.I.file_url(
            DeployWorkflowConfigFile.I.path(),
        )
        return f"See {config_url} and {deploy_url}."

    def justification_osps_gv_01_01(self) -> str:
        """List project members with access to sensitive resources."""
        config_url = RemoteVersionController.I.file_url(
            PyprojectConfigFile.I.path(),
        )
        owners_url = RemoteVersionController.I.file_url(
            CodeownersConfigFile.I.path(),
        )
        return f"See {config_url} and {owners_url}."

    def justification_osps_gv_01_02(self) -> str:
        """Describe project members' roles and responsibilities."""
        config_url = RemoteVersionController.I.file_url(
            PyprojectConfigFile.I.path(),
        )
        owners_url = RemoteVersionController.I.file_url(
            CodeownersConfigFile.I.path(),
        )
        return f"See {config_url} and {owners_url}."

    def justification_osps_gv_02_01(self) -> str:
        """Provide public discussions of proposed changes and usage issues."""
        issues_url = RemoteVersionController.I.issues_url()
        repo_url = RemoteVersionController.I.repo_url()
        return f"See {issues_url} and {repo_url}."

    def justification_osps_gv_03_01(self) -> str:
        """Show that the contribution process is documented."""
        url = RemoteVersionController.I.file_url(ContributingConfigFile.I.path())
        return f"See {url}."

    def justification_osps_gv_03_02(self) -> str:
        """Show that acceptable contribution requirements are documented."""
        url = RemoteVersionController.I.file_url(ContributingConfigFile.I.path())
        return f"See {url}."

    def justification_osps_le_01_01(self) -> str:
        """Require legal authorization for code contributions."""
        terms_url = (
            "https://docs.github.com/en/site-policy/github-terms/"
            "github-terms-of-service#d-user-generated-content"
        )
        repo_url = RemoteVersionController.I.repo_url()
        return f"See {terms_url} and {repo_url}."

    def justification_osps_le_02_01(self) -> str:
        """Show that the source license meets the open-source definition."""
        url = RemoteVersionController.I.file_url(LicenseConfigFile.I.path())
        return f"See {url}."

    def justification_osps_le_02_02(self) -> str:
        """Distribute release assets under open-source licenses."""
        license_url = RemoteVersionController.I.file_url(
            LicenseConfigFile.I.path(),
        )
        config_url = RemoteVersionController.I.file_url(
            PyprojectConfigFile.I.path(),
        )
        release_url = RemoteVersionController.I.file_url(
            ReleaseWorkflowConfigFile.I.path(),
        )
        deploy_url = RemoteVersionController.I.file_url(
            DeployWorkflowConfigFile.I.path(),
        )
        return f"See {license_url}, {config_url}, {release_url}, and {deploy_url}."

    def justification_osps_le_03_01(self) -> str:
        """Show that source licensing is kept in a standard repository file."""
        url = RemoteVersionController.I.file_url(LicenseConfigFile.I.path())
        return f"See {url}."

    def justification_osps_le_03_02(self) -> str:
        """Include licenses with released assets."""
        config_url = RemoteVersionController.I.file_url(
            PyprojectConfigFile.I.path(),
        )
        deploy_url = RemoteVersionController.I.file_url(
            DeployWorkflowConfigFile.I.path(),
        )
        return f"See {config_url} and {deploy_url}."

    def justification_osps_qa_01_01(self) -> str:
        """Make the source repository publicly readable."""
        repo_url = RemoteVersionController.I.repo_url()
        return f"See {repo_url}."

    def justification_osps_qa_01_02(self) -> str:
        """Make source history and authorship publicly accessible."""
        repo_url = RemoteVersionController.I.repo_url()
        return f"See {repo_url}."

    def justification_osps_qa_02_01(self) -> str:
        """Show that direct language dependencies are listed."""
        url = RemoteVersionController.I.file_url(PyprojectConfigFile.I.path())
        return f"See {url}."

    def justification_osps_qa_03_01(self) -> str:
        """Require automated status checks before merging."""
        settings_url = RemoteVersionController.I.file_url(
            RepositorySettingsConfigFile.I.path(),
        )
        configure_url = RemoteVersionController.I.file_url(
            ConfigureRepositoryConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return f"See {settings_url}, {configure_url}, and {health_url}."

    def justification_osps_qa_05_01(self) -> str:
        """Keep generated executables out of version control."""
        ignore_url = RemoteVersionController.I.file_url(
            VersionControllerIgnoreConfigFile.I.path(),
        )
        return f"See {ignore_url}."

    def justification_osps_qa_05_02(self) -> str:
        """Keep unreviewable binary artifacts out of version control."""
        ignore_url = RemoteVersionController.I.file_url(
            VersionControllerIgnoreConfigFile.I.path(),
        )
        return f"See {ignore_url}."

    def justification_osps_qa_06_01(self) -> str:
        """Require automated tests before accepting commits."""
        settings_url = RemoteVersionController.I.file_url(
            RepositorySettingsConfigFile.I.path(),
        )
        configure_url = RemoteVersionController.I.file_url(
            ConfigureRepositoryConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return f"See {settings_url}, {configure_url}, and {health_url}."

    def justification_osps_qa_06_02(self) -> str:
        """Document when and how tests run."""
        contributing_url = RemoteVersionController.I.file_url(
            ContributingConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return f"See {contributing_url} and {health_url}."

    def justification_osps_qa_06_03(self) -> str:
        """Document a policy to add or update tests for major changes."""
        contributing_url = RemoteVersionController.I.file_url(
            ContributingConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return f"See {contributing_url} and {health_url}."

    def justification_osps_qa_07_01(self) -> str:
        """Require non-author human approval before merging."""
        settings_url = RemoteVersionController.I.file_url(
            RepositorySettingsConfigFile.I.path(),
        )
        configure_url = RemoteVersionController.I.file_url(
            ConfigureRepositoryConfigFile.I.path(),
        )
        return f"See {settings_url} and {configure_url}."

    def justification_osps_sa_02_01(self) -> str:
        """Document every released external interface and its inputs and outputs."""
        docs_url = DocsBuilder.I.documentation_url()
        return f"See {docs_url}."

    def justification_osps_vm_01_01(self) -> str:
        """Document coordinated disclosure with a clear response timeframe."""
        security_url = RemoteVersionController.I.file_url(
            SecurityConfigFile.I.path(),
        )
        return f"See {security_url}."

    def justification_osps_vm_02_01(self) -> str:
        """Show that security reporting contacts are documented."""
        url = RemoteVersionController.I.file_url(SecurityConfigFile.I.path())
        return f"See {url}."

    def justification_osps_vm_03_01(self) -> str:
        """Provide a private channel for vulnerability reporting."""
        security_url = RemoteVersionController.I.file_url(
            SecurityConfigFile.I.path(),
        )
        return f"See {security_url}."

    def justification_osps_vm_05_01(self) -> str:
        """Document remediation thresholds for dependency and license findings."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        dependencies_url = RemoteVersionController.I.file_url(
            DependencyBotConfigFile.I.path(),
        )
        configure_url = RemoteVersionController.I.file_url(
            ConfigureRepositoryConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return (
            f"See {hooks_url}, {dependencies_url}, {configure_url}, and {health_url}."
        )

    def justification_osps_vm_05_02(self) -> str:
        """Document a policy to resolve dependency violations before release."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        release_url = RemoteVersionController.I.file_url(
            ReleaseWorkflowConfigFile.I.path(),
        )
        return f"See {hooks_url}, {health_url}, and {release_url}."

    def justification_osps_vm_05_03(self) -> str:
        """Block changes that violate dependency-security policy."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        settings_url = RemoteVersionController.I.file_url(
            RepositorySettingsConfigFile.I.path(),
        )
        configure_url = RemoteVersionController.I.file_url(
            ConfigureRepositoryConfigFile.I.path(),
        )
        return f"See {hooks_url}, {health_url}, {settings_url}, and {configure_url}."

    def justification_osps_vm_06_01(self) -> str:
        """Document remediation thresholds for static-analysis findings."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return f"See {hooks_url} and {health_url}."

    def justification_osps_vm_06_02(self) -> str:
        """Block changes that violate documented security-weakness policy."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        settings_url = RemoteVersionController.I.file_url(
            RepositorySettingsConfigFile.I.path(),
        )
        configure_url = RemoteVersionController.I.file_url(
            ConfigureRepositoryConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return f"See {hooks_url}, {settings_url}, {configure_url}, and {health_url}."

    def justification_regression_tests_added50(self) -> str:
        """Add regression tests for at least half the bugs fixed in six months."""
        contributing_url = RemoteVersionController.I.file_url(
            ContributingConfigFile.I.path(),
        )
        report_url = RemoteVersionController.I.file_url(BugReportConfigFile.I.path())
        template_url = RemoteVersionController.I.file_url(
            PullRequestTemplateConfigFile.I.path(),
        )
        config_url = RemoteVersionController.I.file_url(
            PyprojectConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        repo_url = RemoteVersionController.I.repo_url()
        return (
            f"See {contributing_url}, {report_url}, {template_url}, "
            f"{config_url}, {health_url}, and {repo_url}."
        )

    def justification_release_notes(self) -> str:
        """Explain major changes and upgrade impacts in release notes."""
        release_url = RemoteVersionController.I.file_url(
            ReleaseWorkflowConfigFile.I.path(),
        )
        return f"See {release_url}."

    def justification_repo_distributed(self) -> str:
        """Show that the project uses distributed version control."""
        url = RemoteVersionController.I.repo_url()
        return f"See {url}."

    def justification_repo_interim(self) -> str:
        """Share interim source changes for collaborative review."""
        contributing_url = RemoteVersionController.I.file_url(
            ContributingConfigFile.I.path(),
        )
        repo_url = RemoteVersionController.I.repo_url()
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return f"See {contributing_url}, {repo_url}, and {health_url}."

    def justification_repo_public(self) -> str:
        """Provide a publicly readable source repository."""
        repo_url = RemoteVersionController.I.repo_url()
        return f"See {repo_url}."

    def justification_repo_track(self) -> str:
        """Show that version control records what changed, who changed it, and when."""
        url = RemoteVersionController.I.repo_url()
        return f"See {url}."

    def justification_report_archive(self) -> str:
        """Provide a public archive of reports and responses."""
        issues_url = RemoteVersionController.I.issues_url()
        return f"See {issues_url}."

    def justification_report_process(self) -> str:
        """Show that users have a documented way to report bugs."""
        url = RemoteVersionController.I.file_url(ContributingConfigFile.I.path())
        return f"See {url}."

    def justification_report_responses(self) -> str:
        """Acknowledge a majority of bug reports from the last 2-12 months."""
        url = RemoteVersionController.I.issues_url()
        return f"See {url}."

    def justification_report_tracker(self) -> str:
        """Show that individual issues are tracked in an issue tracker."""
        url = RemoteVersionController.I.issues_url()
        return f"See {url}."

    def justification_roles_responsibilities(self) -> str:
        """Document project roles and responsibilities."""
        config_url = RemoteVersionController.I.file_url(
            PyprojectConfigFile.I.path(),
        )
        owners_url = RemoteVersionController.I.file_url(
            CodeownersConfigFile.I.path(),
        )
        return f"See {config_url} and {owners_url}."

    def justification_sites_https(self) -> str:
        """Show that project sites support HTTPS."""
        repo_url = RemoteVersionController.I.repo_url()
        docs_url = DocsBuilder.I.documentation_url()
        releases_url = RemoteVersionController.I.releases_url()
        return f"See {repo_url}, {docs_url}, and {releases_url}."

    def justification_static_analysis(self) -> str:
        """Show that static analysis runs before releases."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        release_url = RemoteVersionController.I.file_url(
            ReleaseWorkflowConfigFile.I.path(),
        )
        return f"See {hooks_url}, {health_url}, and {release_url}."

    def justification_static_analysis_common_vulnerabilities(self) -> str:
        """Show that static analysis checks for common vulnerabilities."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return f"See {hooks_url} and {health_url}."

    def justification_static_analysis_fixed(self) -> str:
        """Fix confirmed exploitable static-analysis findings promptly."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        release_url = RemoteVersionController.I.file_url(
            ReleaseWorkflowConfigFile.I.path(),
        )
        return f"See {hooks_url}, {health_url}, and {release_url}."

    def justification_static_analysis_often(self) -> str:
        """Show that static analysis runs often."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return f"See {hooks_url} and {health_url}."

    def justification_test(self) -> str:
        """Show that an automated test suite is used with a documented command."""
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        license_url = RemoteVersionController.I.file_url(LicenseConfigFile.I.path())
        return f"See {health_url} and {license_url}."

    def justification_test_branch_coverage80(self) -> str:
        """Reach at least 80 percent branch coverage."""
        config_url = RemoteVersionController.I.file_url(
            PyprojectConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return f"See {config_url} and {health_url}."

    def justification_test_continuous_integration(self) -> str:
        """Show that automated tests run as changes are integrated."""
        url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return f"See {url}."

    def justification_test_invocation(self) -> str:
        """Show that tests use a standard invocation for Python."""
        url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return f"See {url}."

    def justification_test_most(self) -> str:
        """Test most functionality and inputs."""
        config_url = RemoteVersionController.I.file_url(
            PyprojectConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return f"See {config_url} and {health_url}."

    def justification_test_policy(self) -> str:
        """Have a policy to add tests for major new functionality."""
        contributing_url = RemoteVersionController.I.file_url(
            ContributingConfigFile.I.path(),
        )
        config_url = RemoteVersionController.I.file_url(
            PyprojectConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return f"See {contributing_url}, {config_url}, and {health_url}."

    def justification_test_policy_mandated(self) -> str:
        """Require tests for major new functionality in a written policy."""
        contributing_url = RemoteVersionController.I.file_url(
            ContributingConfigFile.I.path(),
        )
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return f"See {contributing_url}, {hooks_url}, and {health_url}."

    def justification_test_statement_coverage80(self) -> str:
        """Reach at least 80 percent statement coverage."""
        config_url = RemoteVersionController.I.file_url(
            PyprojectConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return f"See {config_url} and {health_url}."

    def justification_test_statement_coverage90(self) -> str:
        """Reach at least 90 percent statement coverage."""
        config_url = RemoteVersionController.I.file_url(
            PyprojectConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return f"See {config_url} and {health_url}."

    def justification_tests_are_added(self) -> str:
        """Add meaningful tests for the most recent major functionality changes."""
        contributing_url = RemoteVersionController.I.file_url(
            ContributingConfigFile.I.path(),
        )
        template_url = RemoteVersionController.I.file_url(
            PullRequestTemplateConfigFile.I.path(),
        )
        config_url = RemoteVersionController.I.file_url(
            PyprojectConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        repo_url = RemoteVersionController.I.repo_url()
        return (
            f"See {contributing_url}, {template_url}, {config_url}, "
            f"{health_url}, and {repo_url}."
        )

    def justification_tests_documented_added(self) -> str:
        """Include an add-tests policy in contribution instructions."""
        contributing_url = RemoteVersionController.I.file_url(
            ContributingConfigFile.I.path(),
        )
        template_url = RemoteVersionController.I.file_url(
            PullRequestTemplateConfigFile.I.path(),
        )
        return f"See {contributing_url} and {template_url}."

    def justification_two_person_review(self) -> str:
        """Have another person review at least half of proposed changes."""
        settings_url = RemoteVersionController.I.file_url(
            RepositorySettingsConfigFile.I.path(),
        )
        configure_url = RemoteVersionController.I.file_url(
            ConfigureRepositoryConfigFile.I.path(),
        )
        return f"See {settings_url} and {configure_url}."

    def justification_updateable_reused_components(self) -> str:
        """Show that reused components can be identified and updated."""
        config_url = RemoteVersionController.I.file_url(PyprojectConfigFile.I.path())
        lock_url = RemoteVersionController.I.file_url(PackageManager.I.lock_file())
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        return f"See {config_url}, {lock_url}, and {hooks_url}."

    def justification_version_semver(self) -> str:
        """Use Semantic Versioning or Calendar Versioning."""
        config_url = RemoteVersionController.I.file_url(
            PyprojectConfigFile.I.path(),
        )
        release_url = RemoteVersionController.I.file_url(
            ReleaseWorkflowConfigFile.I.path(),
        )
        return f"See {config_url} and {release_url}."

    def justification_version_tags(self) -> str:
        """Show that releases are identified by version-control tags."""
        url = RemoteVersionController.I.file_url(
            ReleaseWorkflowConfigFile.I.path(),
        )
        return f"See {url}."

    def justification_version_unique(self) -> str:
        """Show that releases have unique version identifiers."""
        url = RemoteVersionController.I.file_url(
            ReleaseWorkflowConfigFile.I.path(),
        )
        return f"See {url}."

    def justification_vulnerabilities_critical_fixed(self) -> str:
        """Rapidly fix all reported critical vulnerabilities."""
        security_url = RemoteVersionController.I.file_url(SecurityConfigFile.I.path())
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        release_url = RemoteVersionController.I.file_url(
            ReleaseWorkflowConfigFile.I.path(),
        )
        return f"See {security_url}, {hooks_url}, {health_url}, and {release_url}."

    def justification_vulnerabilities_fixed_60_days(self) -> str:
        """Leave no publicly known medium-or-higher flaw unpatched over 60 days."""
        security_url = RemoteVersionController.I.file_url(SecurityConfigFile.I.path())
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        release_url = RemoteVersionController.I.file_url(
            ReleaseWorkflowConfigFile.I.path(),
        )
        return f"See {security_url}, {hooks_url}, {health_url}, and {release_url}."

    def justification_vulnerability_report_private(self) -> str:
        """Support private reports over encrypted channels."""
        security_url = RemoteVersionController.I.file_url(
            SecurityConfigFile.I.path(),
        )
        return f"See {security_url}."

    def justification_vulnerability_report_process(self) -> str:
        """Show that the vulnerability reporting process is published."""
        url = RemoteVersionController.I.file_url(SecurityConfigFile.I.path())
        return f"See {url}."

    def justification_vulnerability_report_response(self) -> str:
        """Initially respond to every vulnerability report within 14 days."""
        url = RemoteVersionController.I.file_url(SecurityConfigFile.I.path())
        return f"See {url}."

    def justification_vulnerability_response_process(self) -> str:
        """Show that the vulnerability response process is documented."""
        url = RemoteVersionController.I.file_url(SecurityConfigFile.I.path())
        return f"See {url}."

    def justification_warnings(self) -> str:
        """Show that tools are enabled to detect code quality problems."""
        url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        return f"See {url}."

    def justification_warnings_fixed(self) -> str:
        """Address warnings reported by configured checks."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        release_url = RemoteVersionController.I.file_url(
            ReleaseWorkflowConfigFile.I.path(),
        )
        return f"See {hooks_url}, {health_url}, and {release_url}."

    def justification_warnings_strict(self) -> str:
        """Show that warning checks are configured strictly."""
        config_url = RemoteVersionController.I.file_url(PyprojectConfigFile.I.path())
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        return f"See {config_url} and {hooks_url}."
