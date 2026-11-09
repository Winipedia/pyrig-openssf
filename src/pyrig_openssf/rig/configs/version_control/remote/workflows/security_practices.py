"""Reusable security-practices analysis and code-scanning alert gate."""

from collections.abc import Callable
from pathlib import Path
from typing import Any, override

from pyrig.rig.configs.base.workflow import WorkflowConfigFile
from pyrig.rig.tools.version_control.remote.controller import RemoteVersionController

from pyrig_openssf.rig import resources
from pyrig_openssf.rig.tools.security.practices import SecurityPracticesChecker


class SecurityPracticesWorkflowConfigFile(WorkflowConfigFile):
    """Analyze repository practices and fail on open Scorecard alerts."""

    @override
    def jobs(self) -> tuple[Callable[[], dict[str, Any]], ...]:
        """Return the analysis and alert-gate job builders."""
        return (self.job_analyze, self.job_check_alerts)

    @override
    def stem(self) -> str:
        """Return the workflow filename stem."""
        return "security-practices"

    @override
    def workflow_triggers(self) -> dict[str, Any]:
        """Allow invocation only through a reusable-workflow call."""
        return self.on_workflow_call()

    def job_check_alerts(self) -> dict[str, Any]:
        """Check alerts after the uploaded analysis has been processed."""
        return self.job(
            self.job_check_alerts,
            needs=(self.job_analyze,),
            permissions=self.job_check_alerts_permissions(),
            steps=self.steps_check_alerts(),
            timeout_minutes=5,
        )

    def job_analyze(self) -> dict[str, Any]:
        """Build the isolated analysis and upload job."""
        return self.job(
            self.job_analyze,
            permissions=self.job_analyze_permissions(),
            steps=self.steps_analyze(),
            timeout_minutes=30,
        )

    def job_check_alerts_permissions(self) -> dict[str, str]:
        """Grant read access to code-scanning alerts without OIDC."""
        return self.permission("security-events")

    def steps_check_alerts(self) -> list[dict[str, Any]]:
        """Return the code-scanning alert check."""
        return [self.step_check_alerts()]

    def job_analyze_permissions(self) -> dict[str, str]:
        """Grant repository reads, SARIF upload, and publication signing."""
        return {
            **self.permission_contents(),
            **self.permission("actions"),
            **self.permission("security-events", write=True),
            **self.permission_id_token(write=True),
        }

    def step_check_alerts(self) -> dict[str, Any]:
        """Fail on open Scorecard alerts for the analyzed ref or API errors."""
        return self.step(
            self.step_check_alerts,
            run=RemoteVersionController.I.api_method_args(
                '--raw-field="ref=${GITHUB_REF}"',
                "--raw-field=state=open",
                "--raw-field=tool_name=Scorecard",
                """--jq='if . != [] then error("Alerts found") end'""",
                endpoint='"repos/${GITHUB_REPOSITORY}/code-scanning/alerts"',
                method="GET",
            ).multiline(),
            env={"GH_TOKEN": self.insert_github_token()},
        )

    def steps_analyze(self) -> list[dict[str, Any]]:
        """Return checkout, analysis, and code-scanning upload steps."""
        return [
            self.step_checkout_repository(),
            self.step_analyze_scorecard(),
            self.step_upload_sarif(),
        ]

    def step_analyze_scorecard(self) -> dict[str, Any]:
        """Run Scorecard with public publication enabled."""
        return self.step(
            self.step_analyze_scorecard,
            uses=self.action_scorecard(),
            with_={
                "results_file": self.results_file().as_posix(),
                "results_format": self.results_format(),
                "publish_results": True,
            },
        )

    def step_upload_sarif(self) -> dict[str, Any]:
        """Upload Scorecard results and wait for code-scanning processing."""
        return self.step(
            self.step_upload_sarif,
            uses=self.action_upload_sarif(),
            with_={
                "sarif_file": self.results_file().as_posix(),
            },
        )

    def action_scorecard(self) -> tuple[str, str, str]:
        """Return the Scorecard action name, pinned SHA, and release tag."""
        return self.action_from_resource(self.action_scorecard, resources)

    def action_upload_sarif(self) -> tuple[str, str, str]:
        """Return the SARIF uploader name, pinned SHA, and release tag."""
        return self.action_from_resource(self.action_upload_sarif, resources)

    def results_file(self) -> Path:
        """Return the SARIF report path."""
        return Path(f"{SecurityPracticesChecker.I.name()}.{self.results_format()}")

    def results_format(self) -> str:
        """Return the SARIF report format."""
        return "sarif"
