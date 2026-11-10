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

if TYPE_CHECKING:
    from types import MethodType


class BestPracticesConfigFile(JSONDictConfigFile):
    """Generate proposed OpenSSF Best Practices and Baseline answers."""

    STATUS_MET = "Met"
    STATUS_UNMET = "Unmet"
    STATUS_NOT_APPLICABLE = "N/A"

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
        """Expand each assessment into status and justification fields."""
        return {
            key: value
            for method in sorted(
                self.justifications(),
                key=self.criterion_from_method,
            )
            for key, value in self.criterion_config(method).items()
        }

    def criterion_config(self, method: Callable[[], tuple[str, str]]) -> dict[str, str]:
        """Build status and justification fields from a criterion method."""
        criterion = self.criterion_from_method(method)
        status, justification = method()
        return {
            f"{criterion}_status": status,
            f"{criterion}_justification": justification,
        }

    def justifications(self) -> tuple[Callable[[], tuple[str, str]], ...]:
        """Return the registered status-and-justification methods."""
        return (
            self.justification_accessibility_best_practices,
            self.justification_automated_integration_testing,
            self.justification_build,
            self.justification_build_common_tools,
            self.justification_build_floss_tools,
            self.justification_build_non_recursive,
            self.justification_build_preserve_debug,
            self.justification_build_repeatable,
            self.justification_build_reproducible,
            self.justification_build_standard_variables,
            self.justification_code_of_conduct,
            self.justification_code_review_standards,
            self.justification_coding_standards,
            self.justification_coding_standards_enforced,
            self.justification_contribution,
            self.justification_contribution_requirements,
            self.justification_copyright_per_file,
            self.justification_crypto_call,
            self.justification_crypto_certificate_verification,
            self.justification_crypto_floss,
            self.justification_crypto_keylength,
            self.justification_crypto_password_storage,
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
            self.justification_dynamic_analysis_unsafe,
            self.justification_english,
            self.justification_enhancement_responses,
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
            self.justification_license_per_file,
            self.justification_maintained,
            self.justification_no_leaked_credentials,
            self.justification_osps_ac_01_01,
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
            self.justification_osps_qa_04_01,
            self.justification_osps_qa_04_02,
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
            self.justification_sites_password_security,
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
            self.justification_version_tags_signed,
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

    def criterion_from_method(self, method: Callable[[], tuple[str, str]]) -> str:
        """Return the criterion identifier from a `justification_*` method."""
        return cast("MethodType", method).__name__.removeprefix("justification_")

    def justification_accessibility_best_practices(self) -> tuple[str, str]:
        """Propose accessibility based on the project site and documentation."""
        repo_url = RemoteVersionController.I.repo_url()
        docs_url = DocsBuilder.I.documentation_url()
        return self.STATUS_MET, f"See {repo_url} and {docs_url}."

    def justification_automated_integration_testing(self) -> tuple[str, str]:
        """Show that each check-in on a shared branch runs tests with results."""
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        release_url = RemoteVersionController.I.file_url(
            ReleaseWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {health_url} and {release_url}."

    def justification_build(self) -> tuple[str, str]:
        """Provide an automated build from source."""
        config_url = RemoteVersionController.I.file_url(
            PyprojectConfigFile.I.path(),
        )
        deploy_url = RemoteVersionController.I.file_url(
            DeployWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {config_url} and {deploy_url}."

    def justification_build_common_tools(self) -> tuple[str, str]:
        """Show that the project uses common build tools."""
        url = RemoteVersionController.I.file_url(PyprojectConfigFile.I.path())
        return self.STATUS_MET, f"See {url}."

    def justification_build_floss_tools(self) -> tuple[str, str]:
        """Show that the project can be built with FLOSS tools."""
        url = RemoteVersionController.I.file_url(PyprojectConfigFile.I.path())
        return self.STATUS_MET, f"See {url}."

    def justification_build_non_recursive(self) -> tuple[str, str]:
        """Avoid recursive builds across dependent subdirectories."""
        config_url = RemoteVersionController.I.file_url(
            PyprojectConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {config_url}."

    def justification_build_preserve_debug(self) -> tuple[str, str]:
        """Preserve requested debugging information when building."""
        config_url = RemoteVersionController.I.file_url(
            PyprojectConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {config_url}."

    def justification_build_repeatable(self) -> tuple[str, str]:
        """Assess build repeatability."""
        config_url = RemoteVersionController.I.file_url(
            PyprojectConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {config_url}."

    def justification_build_reproducible(self) -> tuple[str, str]:
        """Assess build reproducibility."""
        config_url = RemoteVersionController.I.file_url(
            PyprojectConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {config_url}."

    def justification_build_standard_variables(self) -> tuple[str, str]:
        """Assess support for standard compiler and linker variables."""
        url = RemoteVersionController.I.file_url(PyprojectConfigFile.I.path())
        return self.STATUS_NOT_APPLICABLE, f"See {url}."

    def justification_code_of_conduct(self) -> tuple[str, str]:
        """Show that the project adopts and publishes a code of conduct."""
        url = RemoteVersionController.I.file_url(CodeOfConductConfigFile.I.path())
        return self.STATUS_MET, f"See {url}."

    def justification_code_review_standards(self) -> tuple[str, str]:
        """Assess documented code review standards."""
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
        return self.STATUS_MET, (
            f"See {contributing_url}, {owners_url}, {settings_url}, "
            f"{configure_url}, and {health_url}."
        )

    def justification_coding_standards(self) -> tuple[str, str]:
        """Show that contributions must follow defined coding standards."""
        config_url = RemoteVersionController.I.file_url(PyprojectConfigFile.I.path())
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {config_url} and {hooks_url}."

    def justification_coding_standards_enforced(self) -> tuple[str, str]:
        """Show that coding style is enforced automatically."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {hooks_url} and {health_url}."

    def justification_contribution(self) -> tuple[str, str]:
        """Show that the contribution process is documented."""
        url = RemoteVersionController.I.file_url(ContributingConfigFile.I.path())
        return self.STATUS_MET, f"See {url}."

    def justification_contribution_requirements(self) -> tuple[str, str]:
        """Show that acceptable contribution requirements are documented."""
        url = RemoteVersionController.I.file_url(ContributingConfigFile.I.path())
        return self.STATUS_MET, f"See {url}."

    def justification_copyright_per_file(self) -> tuple[str, str]:
        """Assess per-file copyright notices."""
        repo_url = RemoteVersionController.I.repo_url()
        license_url = RemoteVersionController.I.file_url(LicenseConfigFile.I.path())
        return self.STATUS_UNMET, f"See {repo_url} and {license_url}."

    def justification_crypto_call(self) -> tuple[str, str]:
        """Assess delegation of cryptographic operations to libraries."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {hooks_url} and {health_url}."

    def justification_crypto_certificate_verification(self) -> tuple[str, str]:
        """Assess default TLS certificate verification."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {hooks_url} and {health_url}."

    def justification_crypto_floss(self) -> tuple[str, str]:
        """Assess whether cryptographic functionality is implementable using FLOSS."""
        repo_url = RemoteVersionController.I.repo_url()
        config_url = RemoteVersionController.I.file_url(PyprojectConfigFile.I.path())
        lock_url = RemoteVersionController.I.file_url(PackageManager.I.lock_file())
        return self.STATUS_MET, f"See {repo_url}, {config_url}, and {lock_url}."

    def justification_crypto_keylength(self) -> tuple[str, str]:
        """Assess cryptographic key lengths."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {hooks_url} and {health_url}."

    def justification_crypto_password_storage(self) -> tuple[str, str]:
        """Assess password storage security."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {hooks_url} and {health_url}."

    def justification_crypto_published(self) -> tuple[str, str]:
        """Assess use of published, reviewed cryptography."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {hooks_url} and {health_url}."

    def justification_crypto_random(self) -> tuple[str, str]:
        """Assess cryptographic randomness."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {hooks_url} and {health_url}."

    def justification_crypto_tls12(self) -> tuple[str, str]:
        """Assess supported TLS versions."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {hooks_url} and {health_url}."

    def justification_crypto_used_network(self) -> tuple[str, str]:
        """Assess secure network defaults."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {hooks_url} and {health_url}."

    def justification_crypto_verification_private(self) -> tuple[str, str]:
        """Assess certificate verification before sending private data."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {hooks_url} and {health_url}."

    def justification_crypto_weaknesses(self) -> tuple[str, str]:
        """Assess avoidance of known cryptographic weaknesses."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {hooks_url} and {health_url}."

    def justification_crypto_working(self) -> tuple[str, str]:
        """Assess cryptographic algorithm and mode suitability."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {hooks_url} and {health_url}."

    def justification_delivery_mitm(self) -> tuple[str, str]:
        """Show that software delivery counters man-in-the-middle attacks."""
        url = RemoteVersionController.I.releases_url()
        return self.STATUS_MET, f"See {url}."

    def justification_delivery_unsigned(self) -> tuple[str, str]:
        """Do not trust unsigned cryptographic hashes retrieved over HTTP."""
        url = RemoteVersionController.I.releases_url()
        return self.STATUS_MET, f"See {url}."

    def justification_dependency_monitoring(self) -> tuple[str, str]:
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
            self.STATUS_MET,
            f"See {hooks_url}, {dependencies_url}, {configure_url}, and {health_url}.",
        )

    def justification_description_good(self) -> tuple[str, str]:
        """Show that the project explains what its software does."""
        readme_url = RemoteVersionController.I.file_url(ReadmeConfigFile.I.path())
        docs_url = DocsBuilder.I.documentation_url()
        return self.STATUS_MET, f"See {readme_url} and {docs_url}."

    def justification_discussion(self) -> tuple[str, str]:
        """Provide searchable, addressable, open discussion channels."""
        issues_url = RemoteVersionController.I.issues_url()
        return self.STATUS_MET, f"See {issues_url}."

    def justification_documentation_achievements(self) -> tuple[str, str]:
        """Assess accuracy of published project achievements."""
        readme_url = RemoteVersionController.I.file_url(
            ReadmeConfigFile.I.path(),
        )
        docs_url = DocsBuilder.I.documentation_url()
        return self.STATUS_MET, f"See {readme_url} and {docs_url}."

    def justification_documentation_basics(self) -> tuple[str, str]:
        """Document installation, startup, usage, and safe operation."""
        readme_url = RemoteVersionController.I.file_url(
            ReadmeConfigFile.I.path(),
        )
        docs_url = DocsBuilder.I.documentation_url()
        return self.STATUS_MET, f"See {readme_url} and {docs_url}."

    def justification_documentation_current(self) -> tuple[str, str]:
        """Keep documentation consistent with the software."""
        contributing_url = RemoteVersionController.I.file_url(
            ContributingConfigFile.I.path(),
        )
        deploy_url = RemoteVersionController.I.file_url(
            DeployWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {contributing_url} and {deploy_url}."

    def justification_documentation_interface(self) -> tuple[str, str]:
        """Document the software's external inputs and outputs."""
        docs_url = DocsBuilder.I.documentation_url()
        return self.STATUS_MET, f"See {docs_url}."

    def justification_documentation_quick_start(self) -> tuple[str, str]:
        """Provide a quick introduction to useful software behavior."""
        readme_url = RemoteVersionController.I.file_url(
            ReadmeConfigFile.I.path(),
        )
        docs_url = DocsBuilder.I.documentation_url()
        return self.STATUS_MET, f"See {readme_url} and {docs_url}."

    def justification_dynamic_analysis(self) -> tuple[str, str]:
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
        return self.STATUS_MET, f"See {config_url}, {health_url}, and {release_url}."

    def justification_dynamic_analysis_enable_assertions(self) -> tuple[str, str]:
        """Assess runtime assertions during dynamic analysis."""
        config_url = RemoteVersionController.I.file_url(
            PyprojectConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {config_url} and {health_url}."

    def justification_dynamic_analysis_fixed(self) -> tuple[str, str]:
        """Assess remediation of dynamic-analysis findings."""
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        release_url = RemoteVersionController.I.file_url(
            ReleaseWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {health_url} and {release_url}."

    def justification_dynamic_analysis_unsafe(self) -> tuple[str, str]:
        """Assess dynamic analysis of memory-unsafe code."""
        repo_url = RemoteVersionController.I.repo_url()
        pyproject_url = RemoteVersionController.I.file_url(PyprojectConfigFile.I.path())
        return self.STATUS_NOT_APPLICABLE, f"See {repo_url} and {pyproject_url}."

    def justification_english(self) -> tuple[str, str]:
        """Show that documentation and bug reporting support English."""
        contributing_url = RemoteVersionController.I.file_url(
            ContributingConfigFile.I.path(),
        )
        report_url = RemoteVersionController.I.file_url(BugReportConfigFile.I.path())
        return self.STATUS_MET, f"See {contributing_url} and {report_url}."

    def justification_enhancement_responses(self) -> tuple[str, str]:
        """Assess responsiveness to enhancement requests."""
        url = RemoteVersionController.I.issues_url()
        return self.STATUS_MET, f"See {url}."

    def justification_external_dependencies(self) -> tuple[str, str]:
        """Show that dependencies are listed in a machine-readable format."""
        config_url = RemoteVersionController.I.file_url(PyprojectConfigFile.I.path())
        lock_url = RemoteVersionController.I.file_url(PackageManager.I.lock_file())
        return self.STATUS_MET, f"See {config_url} and {lock_url}."

    def justification_floss_license(self) -> tuple[str, str]:
        """Show that the software is released under a FLOSS license."""
        url = RemoteVersionController.I.file_url(LicenseConfigFile.I.path())
        return self.STATUS_MET, f"See {url}."

    def justification_floss_license_osi(self) -> tuple[str, str]:
        """Show that the software uses an OSI-approved license."""
        url = RemoteVersionController.I.file_url(LicenseConfigFile.I.path())
        return self.STATUS_MET, f"See {url}."

    def justification_installation_common(self) -> tuple[str, str]:
        """Show that standard installation and uninstallation are supported."""
        url = RemoteVersionController.I.file_url(PyprojectConfigFile.I.path())
        return self.STATUS_MET, f"See {url}."

    def justification_installation_development_quick(self) -> tuple[str, str]:
        """Show that developers can quickly set up the development environment."""
        url = RemoteVersionController.I.file_url(ContributingConfigFile.I.path())
        return self.STATUS_MET, f"See {url}."

    def justification_installation_standard_variables(self) -> tuple[str, str]:
        """Assess support for standard installation variables."""
        config_url = RemoteVersionController.I.file_url(
            PyprojectConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {config_url}."

    def justification_interact(self) -> tuple[str, str]:
        """Explain how to obtain, give feedback on, and contribute to the software."""
        readme_url = RemoteVersionController.I.file_url(
            ReadmeConfigFile.I.path(),
        )
        docs_url = DocsBuilder.I.documentation_url()
        contributing_url = RemoteVersionController.I.file_url(
            ContributingConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {readme_url}, {docs_url}, and {contributing_url}."

    def justification_interfaces_current(self) -> tuple[str, str]:
        """Avoid deprecated interfaces in supported environments."""
        config_url = RemoteVersionController.I.file_url(
            PyprojectConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {config_url} and {health_url}."

    def justification_know_common_errors(self) -> tuple[str, str]:
        """Assess developer knowledge of common security errors."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {hooks_url} and {health_url}."

    def justification_know_secure_design(self) -> tuple[str, str]:
        """Assess developer knowledge of secure design."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        release_url = RemoteVersionController.I.file_url(
            ReleaseWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {hooks_url}, {health_url} and {release_url}."

    def justification_license_location(self) -> tuple[str, str]:
        """Show that the license is published in a standard repository location."""
        url = RemoteVersionController.I.file_url(LicenseConfigFile.I.path())
        return self.STATUS_MET, f"See {url}."

    def justification_license_per_file(self) -> tuple[str, str]:
        """Assess per-file license notices."""
        repo_url = RemoteVersionController.I.repo_url()
        license_url = RemoteVersionController.I.file_url(LicenseConfigFile.I.path())
        return self.STATUS_UNMET, f"See {repo_url} and {license_url}."

    def justification_maintained(self) -> tuple[str, str]:
        """Keep the project maintained."""
        dependencies_url = RemoteVersionController.I.file_url(
            DependencyBotConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        repo_url = RemoteVersionController.I.repo_url()
        return self.STATUS_MET, f"See {dependencies_url}, {health_url}, and {repo_url}."

    def justification_no_leaked_credentials(self) -> tuple[str, str]:
        """Keep valid credentials out of the public repository."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {hooks_url} and {health_url}."

    def justification_osps_ac_01_01(self) -> tuple[str, str]:
        """Assess multi-factor authentication for sensitive repository access."""
        repo_url = RemoteVersionController.I.repo_url()
        docs_url = (
            "https://docs.github.com/en/authentication/"
            "securing-your-account-with-two-factor-authentication-2fa/"
            "about-mandatory-two-factor-authentication"
        )
        return self.STATUS_MET, f"See {repo_url} and {docs_url}."

    def justification_osps_ac_02_01(self) -> tuple[str, str]:
        """Assign new collaborators' repository permissions manually."""
        repo_url = RemoteVersionController.I.repo_url()
        return self.STATUS_MET, f"See {repo_url}."

    def justification_osps_ac_03_01(self) -> tuple[str, str]:
        """Assess protection against direct commits."""
        settings_url = RemoteVersionController.I.file_url(
            RepositorySettingsConfigFile.I.path(),
        )
        configure_url = RemoteVersionController.I.file_url(
            ConfigureRepositoryConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {settings_url} and {configure_url}."

    def justification_osps_ac_03_02(self) -> tuple[str, str]:
        """Protect primary-branch deletion as a sensitive operation."""
        settings_url = RemoteVersionController.I.file_url(
            RepositorySettingsConfigFile.I.path(),
        )
        configure_url = RemoteVersionController.I.file_url(
            ConfigureRepositoryConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {settings_url} and {configure_url}."

    def justification_osps_ac_04_01(self) -> tuple[str, str]:
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
        return self.STATUS_MET, f"See {health_url}, {release_url}, and {deploy_url}."

    def justification_osps_ac_04_02(self) -> tuple[str, str]:
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
        return self.STATUS_MET, f"See {health_url}, {release_url}, and {deploy_url}."

    def justification_osps_br_01_01(self) -> tuple[str, str]:
        """Assess handling of untrusted CI input."""
        release_url = RemoteVersionController.I.file_url(
            ReleaseWorkflowConfigFile.I.path(),
        )
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {release_url}, {hooks_url}, and {health_url}."

    def justification_osps_br_01_03(self) -> tuple[str, str]:
        """Assess isolation of CI credentials from untrusted code."""
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
            self.STATUS_MET,
            f"See {settings_url}, {configure_url}, and {health_url}.",
        )

    def justification_osps_br_01_04(self) -> tuple[str, str]:
        """Assess handling of collaborator-supplied CI input."""
        release_url = RemoteVersionController.I.file_url(
            ReleaseWorkflowConfigFile.I.path(),
        )
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {release_url}, {hooks_url}, and {health_url}."

    def justification_osps_br_02_01(self) -> tuple[str, str]:
        """Show that every release receives a unique version identifier."""
        url = RemoteVersionController.I.file_url(
            ReleaseWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {url}."

    def justification_osps_br_02_02(self) -> tuple[str, str]:
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
        return self.STATUS_MET, f"See {config_url}, {release_url}, and {deploy_url}."

    def justification_osps_br_03_01(self) -> tuple[str, str]:
        """Deliver official project channels exclusively over encryption."""
        config_url = RemoteVersionController.I.file_url(
            PyprojectConfigFile.I.path(),
        )
        repo_url = RemoteVersionController.I.repo_url()
        docs_url = DocsBuilder.I.documentation_url()
        releases_url = RemoteVersionController.I.releases_url()
        return (
            self.STATUS_MET,
            f"See {config_url}, {repo_url}, {docs_url}, and {releases_url}.",
        )

    def justification_osps_br_03_02(self) -> tuple[str, str]:
        """Show that distribution uses cryptographically authenticated channels."""
        url = RemoteVersionController.I.releases_url()
        return self.STATUS_MET, f"See {url}."

    def justification_osps_br_04_01(self) -> tuple[str, str]:
        """Describe functional and security modifications in every release."""
        release_url = RemoteVersionController.I.file_url(
            ReleaseWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {release_url}."

    def justification_osps_br_05_01(self) -> tuple[str, str]:
        """Show that pipelines use standard dependency management tools."""
        url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {url}."

    def justification_osps_br_07_01(self) -> tuple[str, str]:
        """Show that mechanisms prevent accidental credential commits."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {hooks_url} and {health_url}."

    def justification_osps_do_01_01(self) -> tuple[str, str]:
        """Provide guides for all basic functionality."""
        readme_url = RemoteVersionController.I.file_url(
            ReadmeConfigFile.I.path(),
        )
        docs_url = DocsBuilder.I.documentation_url()
        return self.STATUS_MET, f"See {readme_url} and {docs_url}."

    def justification_osps_do_02_01(self) -> tuple[str, str]:
        """Show that defect reporting is documented."""
        url = RemoteVersionController.I.file_url(ContributingConfigFile.I.path())
        return self.STATUS_MET, f"See {url}."

    def justification_osps_do_03_02(self) -> tuple[str, str]:
        """Assess release-author verification instructions."""
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
        return (
            self.STATUS_MET,
            f"See {settings_url}, {configure_url}, {release_url}, and {deploy_url}.",
        )

    def justification_osps_do_04_01(self) -> tuple[str, str]:
        """Document the scope and duration of release support."""
        security_url = RemoteVersionController.I.file_url(
            SecurityConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {security_url}."

    def justification_osps_do_05_01(self) -> tuple[str, str]:
        """Show that the end of security support is documented."""
        url = RemoteVersionController.I.file_url(SecurityConfigFile.I.path())
        return self.STATUS_MET, f"See {url}."

    def justification_osps_do_06_01(self) -> tuple[str, str]:
        """Document how dependencies are selected, obtained, and tracked."""
        config_url = RemoteVersionController.I.file_url(PyprojectConfigFile.I.path())
        lock_url = RemoteVersionController.I.file_url(PackageManager.I.lock_file())
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {config_url}, {lock_url}, and {hooks_url}."

    def justification_osps_do_07_01(self) -> tuple[str, str]:
        """Document build instructions and required dependencies."""
        config_url = RemoteVersionController.I.file_url(
            PyprojectConfigFile.I.path(),
        )
        deploy_url = RemoteVersionController.I.file_url(
            DeployWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {config_url} and {deploy_url}."

    def justification_osps_gv_01_01(self) -> tuple[str, str]:
        """Assess the inventory of members with sensitive-resource access."""
        config_url = RemoteVersionController.I.file_url(
            PyprojectConfigFile.I.path(),
        )
        owners_url = RemoteVersionController.I.file_url(
            CodeownersConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {config_url} and {owners_url}."

    def justification_osps_gv_01_02(self) -> tuple[str, str]:
        """Describe project members' roles and responsibilities."""
        config_url = RemoteVersionController.I.file_url(
            PyprojectConfigFile.I.path(),
        )
        owners_url = RemoteVersionController.I.file_url(
            CodeownersConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {config_url} and {owners_url}."

    def justification_osps_gv_02_01(self) -> tuple[str, str]:
        """Provide public discussions of proposed changes and usage issues."""
        issues_url = RemoteVersionController.I.issues_url()
        repo_url = RemoteVersionController.I.repo_url()
        return self.STATUS_MET, f"See {issues_url} and {repo_url}."

    def justification_osps_gv_03_01(self) -> tuple[str, str]:
        """Show that the contribution process is documented."""
        url = RemoteVersionController.I.file_url(ContributingConfigFile.I.path())
        return self.STATUS_MET, f"See {url}."

    def justification_osps_gv_03_02(self) -> tuple[str, str]:
        """Show that acceptable contribution requirements are documented."""
        url = RemoteVersionController.I.file_url(ContributingConfigFile.I.path())
        return self.STATUS_MET, f"See {url}."

    def justification_osps_le_01_01(self) -> tuple[str, str]:
        """Require legal authorization for code contributions."""
        terms_url = (
            "https://docs.github.com/en/site-policy/github-terms/"
            "github-terms-of-service#d-user-generated-content"
        )
        repo_url = RemoteVersionController.I.repo_url()
        return self.STATUS_MET, f"See {terms_url} and {repo_url}."

    def justification_osps_le_02_01(self) -> tuple[str, str]:
        """Show that the source license meets the open-source definition."""
        url = RemoteVersionController.I.file_url(LicenseConfigFile.I.path())
        return self.STATUS_MET, f"See {url}."

    def justification_osps_le_02_02(self) -> tuple[str, str]:
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
        return (
            self.STATUS_MET,
            f"See {license_url}, {config_url}, {release_url}, and {deploy_url}.",
        )

    def justification_osps_le_03_01(self) -> tuple[str, str]:
        """Show that source licensing is kept in a standard repository file."""
        url = RemoteVersionController.I.file_url(LicenseConfigFile.I.path())
        return self.STATUS_MET, f"See {url}."

    def justification_osps_le_03_02(self) -> tuple[str, str]:
        """Include licenses with released assets."""
        config_url = RemoteVersionController.I.file_url(
            PyprojectConfigFile.I.path(),
        )
        deploy_url = RemoteVersionController.I.file_url(
            DeployWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {config_url} and {deploy_url}."

    def justification_osps_qa_01_01(self) -> tuple[str, str]:
        """Make the source repository publicly readable."""
        repo_url = RemoteVersionController.I.repo_url()
        return self.STATUS_MET, f"See {repo_url}."

    def justification_osps_qa_01_02(self) -> tuple[str, str]:
        """Assess access to source history and authorship."""
        repo_url = RemoteVersionController.I.repo_url()
        return self.STATUS_MET, f"See {repo_url}."

    def justification_osps_qa_02_01(self) -> tuple[str, str]:
        """Show that direct language dependencies are listed."""
        url = RemoteVersionController.I.file_url(PyprojectConfigFile.I.path())
        return self.STATUS_MET, f"See {url}."

    def justification_osps_qa_03_01(self) -> tuple[str, str]:
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
        return (
            self.STATUS_MET,
            f"See {settings_url}, {configure_url}, and {health_url}.",
        )

    def justification_osps_qa_04_01(self) -> tuple[str, str]:
        """Assess documentation of project code repositories."""
        url = RemoteVersionController.I.repo_url()
        return self.STATUS_NOT_APPLICABLE, f"See {url}."

    def justification_osps_qa_04_02(self) -> tuple[str, str]:
        """Assess security requirements across release repositories."""
        repo_url = RemoteVersionController.I.repo_url()
        release_url = RemoteVersionController.I.file_url(
            ReleaseWorkflowConfigFile.I.path(),
        )
        return self.STATUS_NOT_APPLICABLE, f"See {repo_url} and {release_url}."

    def justification_osps_qa_05_01(self) -> tuple[str, str]:
        """Keep generated executables out of version control."""
        ignore_url = RemoteVersionController.I.file_url(
            VersionControllerIgnoreConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {ignore_url}."

    def justification_osps_qa_05_02(self) -> tuple[str, str]:
        """Keep unreviewable binary artifacts out of version control."""
        ignore_url = RemoteVersionController.I.file_url(
            VersionControllerIgnoreConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {ignore_url}."

    def justification_osps_qa_06_01(self) -> tuple[str, str]:
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
        return (
            self.STATUS_MET,
            f"See {settings_url}, {configure_url}, and {health_url}.",
        )

    def justification_osps_qa_06_02(self) -> tuple[str, str]:
        """Document when and how tests run."""
        contributing_url = RemoteVersionController.I.file_url(
            ContributingConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {contributing_url} and {health_url}."

    def justification_osps_qa_06_03(self) -> tuple[str, str]:
        """Document a policy to add or update tests for major changes."""
        contributing_url = RemoteVersionController.I.file_url(
            ContributingConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {contributing_url} and {health_url}."

    def justification_osps_qa_07_01(self) -> tuple[str, str]:
        """Assess independent human approval of changes."""
        settings_url = RemoteVersionController.I.file_url(
            RepositorySettingsConfigFile.I.path(),
        )
        configure_url = RemoteVersionController.I.file_url(
            ConfigureRepositoryConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {settings_url} and {configure_url}."

    def justification_osps_sa_02_01(self) -> tuple[str, str]:
        """Document every released external interface and its inputs and outputs."""
        docs_url = DocsBuilder.I.documentation_url()
        return self.STATUS_MET, f"See {docs_url}."

    def justification_osps_vm_01_01(self) -> tuple[str, str]:
        """Assess coordinated vulnerability disclosure."""
        security_url = RemoteVersionController.I.file_url(
            SecurityConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {security_url}."

    def justification_osps_vm_02_01(self) -> tuple[str, str]:
        """Show that security reporting contacts are documented."""
        url = RemoteVersionController.I.file_url(SecurityConfigFile.I.path())
        return self.STATUS_MET, f"See {url}."

    def justification_osps_vm_03_01(self) -> tuple[str, str]:
        """Provide a private channel for vulnerability reporting."""
        security_url = RemoteVersionController.I.file_url(
            SecurityConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {security_url}."

    def justification_osps_vm_05_01(self) -> tuple[str, str]:
        """Assess dependency and license remediation policy."""
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
            self.STATUS_MET,
            f"See {hooks_url}, {dependencies_url}, {configure_url}, and {health_url}.",
        )

    def justification_osps_vm_05_02(self) -> tuple[str, str]:
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
        return self.STATUS_MET, f"See {hooks_url}, {health_url}, and {release_url}."

    def justification_osps_vm_05_03(self) -> tuple[str, str]:
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
        return (
            self.STATUS_MET,
            f"See {hooks_url}, {health_url}, {settings_url}, and {configure_url}.",
        )

    def justification_osps_vm_06_01(self) -> tuple[str, str]:
        """Assess static-analysis remediation policy."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {hooks_url} and {health_url}."

    def justification_osps_vm_06_02(self) -> tuple[str, str]:
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
        return (
            self.STATUS_MET,
            f"See {hooks_url}, {settings_url}, {configure_url}, and {health_url}.",
        )

    def justification_regression_tests_added50(self) -> tuple[str, str]:
        """Assess regression tests for bug fixes."""
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
        return self.STATUS_MET, (
            f"See {contributing_url}, {report_url}, {template_url}, "
            f"{config_url}, {health_url}, and {repo_url}."
        )

    def justification_release_notes(self) -> tuple[str, str]:
        """Explain major changes and upgrade impacts in release notes."""
        release_url = RemoteVersionController.I.file_url(
            ReleaseWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {release_url}."

    def justification_repo_distributed(self) -> tuple[str, str]:
        """Show that the project uses distributed version control."""
        url = RemoteVersionController.I.repo_url()
        return self.STATUS_MET, f"See {url}."

    def justification_repo_interim(self) -> tuple[str, str]:
        """Share interim source changes for collaborative review."""
        contributing_url = RemoteVersionController.I.file_url(
            ContributingConfigFile.I.path(),
        )
        repo_url = RemoteVersionController.I.repo_url()
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {contributing_url}, {repo_url}, and {health_url}."

    def justification_repo_public(self) -> tuple[str, str]:
        """Provide a publicly readable source repository."""
        repo_url = RemoteVersionController.I.repo_url()
        return self.STATUS_MET, f"See {repo_url}."

    def justification_repo_track(self) -> tuple[str, str]:
        """Show that version control records what changed, who changed it, and when."""
        url = RemoteVersionController.I.repo_url()
        return self.STATUS_MET, f"See {url}."

    def justification_report_archive(self) -> tuple[str, str]:
        """Provide a public archive of reports and responses."""
        issues_url = RemoteVersionController.I.issues_url()
        return self.STATUS_MET, f"See {issues_url}."

    def justification_report_process(self) -> tuple[str, str]:
        """Show that users have a documented way to report bugs."""
        url = RemoteVersionController.I.file_url(ContributingConfigFile.I.path())
        return self.STATUS_MET, f"See {url}."

    def justification_report_responses(self) -> tuple[str, str]:
        """Assess responsiveness to bug reports."""
        url = RemoteVersionController.I.issues_url()
        return self.STATUS_MET, f"See {url}."

    def justification_report_tracker(self) -> tuple[str, str]:
        """Show that individual issues are tracked in an issue tracker."""
        url = RemoteVersionController.I.issues_url()
        return self.STATUS_MET, f"See {url}."

    def justification_roles_responsibilities(self) -> tuple[str, str]:
        """Document project roles and responsibilities."""
        config_url = RemoteVersionController.I.file_url(
            PyprojectConfigFile.I.path(),
        )
        owners_url = RemoteVersionController.I.file_url(
            CodeownersConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {config_url} and {owners_url}."

    def justification_sites_https(self) -> tuple[str, str]:
        """Show that project sites support HTTPS."""
        repo_url = RemoteVersionController.I.repo_url()
        docs_url = DocsBuilder.I.documentation_url()
        releases_url = RemoteVersionController.I.releases_url()
        return self.STATUS_MET, f"See {repo_url}, {docs_url}, and {releases_url}."

    def justification_sites_password_security(self) -> tuple[str, str]:
        """Assess password security of project sites."""
        repo_url = RemoteVersionController.I.repo_url()
        docs_url = DocsBuilder.I.documentation_url()
        releases_url = RemoteVersionController.I.releases_url()
        return self.STATUS_MET, f"See {repo_url}, {docs_url}, and {releases_url}."

    def justification_static_analysis(self) -> tuple[str, str]:
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
        return self.STATUS_MET, f"See {hooks_url}, {health_url}, and {release_url}."

    def justification_static_analysis_common_vulnerabilities(self) -> tuple[str, str]:
        """Show that static analysis checks for common vulnerabilities."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {hooks_url} and {health_url}."

    def justification_static_analysis_fixed(self) -> tuple[str, str]:
        """Assess remediation of static-analysis findings."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        release_url = RemoteVersionController.I.file_url(
            ReleaseWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {hooks_url}, {health_url}, and {release_url}."

    def justification_static_analysis_often(self) -> tuple[str, str]:
        """Show that static analysis runs often."""
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {hooks_url} and {health_url}."

    def justification_test(self) -> tuple[str, str]:
        """Show that an automated test suite is used with a documented command."""
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        license_url = RemoteVersionController.I.file_url(LicenseConfigFile.I.path())
        return self.STATUS_MET, f"See {health_url} and {license_url}."

    def justification_test_branch_coverage80(self) -> tuple[str, str]:
        """Assess the 80 percent branch coverage criterion."""
        config_url = RemoteVersionController.I.file_url(
            PyprojectConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {config_url} and {health_url}."

    def justification_test_continuous_integration(self) -> tuple[str, str]:
        """Show that automated tests run as changes are integrated."""
        url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {url}."

    def justification_test_invocation(self) -> tuple[str, str]:
        """Show that tests use a standard invocation for Python."""
        url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {url}."

    def justification_test_most(self) -> tuple[str, str]:
        """Test most functionality and inputs."""
        config_url = RemoteVersionController.I.file_url(
            PyprojectConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {config_url} and {health_url}."

    def justification_test_policy(self) -> tuple[str, str]:
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
        return (
            self.STATUS_MET,
            f"See {contributing_url}, {config_url}, and {health_url}.",
        )

    def justification_test_policy_mandated(self) -> tuple[str, str]:
        """Assess the written requirement to add tests."""
        contributing_url = RemoteVersionController.I.file_url(
            ContributingConfigFile.I.path(),
        )
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return (
            self.STATUS_MET,
            f"See {contributing_url}, {hooks_url}, and {health_url}.",
        )

    def justification_test_statement_coverage80(self) -> tuple[str, str]:
        """Assess the 80 percent statement coverage criterion."""
        config_url = RemoteVersionController.I.file_url(
            PyprojectConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {config_url} and {health_url}."

    def justification_test_statement_coverage90(self) -> tuple[str, str]:
        """Assess the 90 percent statement coverage criterion."""
        config_url = RemoteVersionController.I.file_url(
            PyprojectConfigFile.I.path(),
        )
        health_url = RemoteVersionController.I.file_url(
            HealthCheckWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {config_url} and {health_url}."

    def justification_tests_are_added(self) -> tuple[str, str]:
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
        return self.STATUS_MET, (
            f"See {contributing_url}, {template_url}, {config_url}, "
            f"{health_url}, and {repo_url}."
        )

    def justification_tests_documented_added(self) -> tuple[str, str]:
        """Assess test requirements in contribution instructions."""
        contributing_url = RemoteVersionController.I.file_url(
            ContributingConfigFile.I.path(),
        )
        template_url = RemoteVersionController.I.file_url(
            PullRequestTemplateConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {contributing_url} and {template_url}."

    def justification_two_person_review(self) -> tuple[str, str]:
        """Assess two-person review of proposed changes."""
        settings_url = RemoteVersionController.I.file_url(
            RepositorySettingsConfigFile.I.path(),
        )
        configure_url = RemoteVersionController.I.file_url(
            ConfigureRepositoryConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {settings_url} and {configure_url}."

    def justification_updateable_reused_components(self) -> tuple[str, str]:
        """Show that reused components can be identified and updated."""
        config_url = RemoteVersionController.I.file_url(PyprojectConfigFile.I.path())
        lock_url = RemoteVersionController.I.file_url(PackageManager.I.lock_file())
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {config_url}, {lock_url}, and {hooks_url}."

    def justification_version_semver(self) -> tuple[str, str]:
        """Assess use of Semantic Versioning or Calendar Versioning."""
        config_url = RemoteVersionController.I.file_url(
            PyprojectConfigFile.I.path(),
        )
        release_url = RemoteVersionController.I.file_url(
            ReleaseWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {config_url} and {release_url}."

    def justification_version_tags(self) -> tuple[str, str]:
        """Show that releases are identified by version-control tags."""
        url = RemoteVersionController.I.file_url(
            ReleaseWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {url}."

    def justification_version_tags_signed(self) -> tuple[str, str]:
        """Assess cryptographic signing of version tags."""
        url = RemoteVersionController.I.file_url(ReleaseWorkflowConfigFile.I.path())
        return self.STATUS_UNMET, f"See {url}."

    def justification_version_unique(self) -> tuple[str, str]:
        """Show that releases have unique version identifiers."""
        url = RemoteVersionController.I.file_url(
            ReleaseWorkflowConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {url}."

    def justification_vulnerabilities_critical_fixed(self) -> tuple[str, str]:
        """Assess remediation of critical vulnerabilities."""
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
        return (
            self.STATUS_MET,
            f"See {security_url}, {hooks_url}, {health_url}, and {release_url}.",
        )

    def justification_vulnerabilities_fixed_60_days(self) -> tuple[str, str]:
        """Assess the 60-day vulnerability remediation criterion."""
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
        return (
            self.STATUS_MET,
            f"See {security_url}, {hooks_url}, {health_url}, and {release_url}.",
        )

    def justification_vulnerability_report_private(self) -> tuple[str, str]:
        """Support private reports over encrypted channels."""
        security_url = RemoteVersionController.I.file_url(
            SecurityConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {security_url}."

    def justification_vulnerability_report_process(self) -> tuple[str, str]:
        """Show that the vulnerability reporting process is published."""
        url = RemoteVersionController.I.file_url(SecurityConfigFile.I.path())
        return self.STATUS_MET, f"See {url}."

    def justification_vulnerability_report_response(self) -> tuple[str, str]:
        """Assess the 14-day initial vulnerability response criterion."""
        url = RemoteVersionController.I.file_url(SecurityConfigFile.I.path())
        return self.STATUS_MET, f"See {url}."

    def justification_vulnerability_response_process(self) -> tuple[str, str]:
        """Show that the vulnerability response process is documented."""
        url = RemoteVersionController.I.file_url(SecurityConfigFile.I.path())
        return self.STATUS_MET, f"See {url}."

    def justification_warnings(self) -> tuple[str, str]:
        """Show that tools are enabled to detect code quality problems."""
        url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {url}."

    def justification_warnings_fixed(self) -> tuple[str, str]:
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
        return self.STATUS_MET, f"See {hooks_url}, {health_url}, and {release_url}."

    def justification_warnings_strict(self) -> tuple[str, str]:
        """Show that warning checks are configured strictly."""
        config_url = RemoteVersionController.I.file_url(PyprojectConfigFile.I.path())
        hooks_url = RemoteVersionController.I.file_url(
            VersionControlHookManagerConfigFile.I.path(),
        )
        return self.STATUS_MET, f"See {config_url} and {hooks_url}."
