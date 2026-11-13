"""Test module."""

import shlex
from pathlib import Path

from pyrig.core.resources import resource_content
from pyrig.core.strings import read_text_utf8

from pyrig_openssf.rig import resources
from pyrig_openssf.rig.configs.version_control.remote.workflows.security_practices import (  # noqa: E501
    SecurityPracticesWorkflowConfigFile,
)


class TestSecurityPracticesWorkflowConfigFile:
    """Test security-practices workflow configuration."""

    def test_action_scorecard(self) -> None:
        """Test method."""
        workflow = SecurityPracticesWorkflowConfigFile.I
        assert workflow.action_scorecard() == tuple(
            resource_content("ACTION_SCORECARD", resources).splitlines(),
        )
        action, ref, tag = workflow.action_scorecard()
        assert f'"uses": "{action}@{ref}"  # {tag}' in read_text_utf8(workflow.path())

    def test_action_upload_sarif(self) -> None:
        """Test method."""
        workflow = SecurityPracticesWorkflowConfigFile.I
        assert workflow.action_upload_sarif() == tuple(
            resource_content("ACTION_UPLOAD_SARIF", resources).splitlines(),
        )
        action, ref, tag = workflow.action_upload_sarif()
        assert f'"uses": "{action}@{ref}"  # {tag}' in read_text_utf8(workflow.path())

    def test_job_analyze(self) -> None:
        """Test method."""
        workflow = SecurityPracticesWorkflowConfigFile.I
        job = workflow.job_analyze()
        assert job["job_id"] == "analyze"
        assert job["runs-on"] == "ubuntu-latest"
        assert job["timeout-minutes"] == 30  # noqa: PLR2004
        assert job["permissions"] == workflow.permissions_job_analyze()
        assert [step["id"] for step in job["steps"]] == [
            "checkout-repository",
            "analyze-scorecard",
            "upload-sarif",
        ]

    def test_job_check_alerts(self) -> None:
        """Test method."""
        workflow = SecurityPracticesWorkflowConfigFile.I
        job = workflow.job_check_alerts()
        assert job["job_id"] == "check-alerts"
        assert job["needs"] == ["analyze"]
        assert job["timeout-minutes"] == 5  # noqa: PLR2004
        assert job["permissions"] == workflow.permissions_job_check_alerts()
        assert job["steps"] == workflow.steps_check_alerts()

    def test_jobs(self) -> None:
        """Test method."""
        workflow = SecurityPracticesWorkflowConfigFile.I
        assert workflow.jobs() == (workflow.job_analyze, workflow.job_check_alerts)

    def test_permissions_job_analyze(self) -> None:
        """Test method."""
        assert SecurityPracticesWorkflowConfigFile.I.permissions_job_analyze() == {
            "contents": "read",
            "actions": "read",
            "security-events": "write",
            "id-token": "write",
        }

    def test_permissions_job_check_alerts(self) -> None:
        """Test method."""
        assert SecurityPracticesWorkflowConfigFile.I.permissions_job_check_alerts() == {
            "security-events": "read",
        }

    def test_results_file(self) -> None:
        """Test method."""
        assert SecurityPracticesWorkflowConfigFile.I.results_file() == Path(
            "scorecard.sarif",
        )

    def test_results_format(self) -> None:
        """Test method."""
        assert SecurityPracticesWorkflowConfigFile.I.results_format() == "sarif"

    def test_stem(self) -> None:
        """Test method."""
        assert SecurityPracticesWorkflowConfigFile.I.stem() == "security-practices"

    def test_step_analyze_scorecard(self) -> None:
        """Test method."""
        workflow = SecurityPracticesWorkflowConfigFile.I
        assert workflow.step_analyze_scorecard()["with"] == {
            "results_file": "scorecard.sarif",
            "results_format": "sarif",
            "publish_results": True,
        }

    def test_step_check_alerts(self) -> None:
        """Test method."""
        step = SecurityPracticesWorkflowConfigFile.I.step_check_alerts()
        assert shlex.split(step["run"].replace("\\\n", "")) == [
            "gh",
            "api",
            "repos/${GITHUB_REPOSITORY}/code-scanning/alerts",
            "--method=GET",
            "--raw-field=ref=${GITHUB_REF}",
            "--raw-field=state=open",
            "--raw-field=tool_name=Scorecard",
            '--jq=if . != [] then error("Alerts found") end',
        ]
        assert step["env"] == {"GH_TOKEN": "${{ secrets.GITHUB_TOKEN }}"}

    def test_step_upload_sarif(self) -> None:
        """Test method."""
        assert SecurityPracticesWorkflowConfigFile.I.step_upload_sarif()["with"] == {
            "sarif_file": "scorecard.sarif",
        }

    def test_steps_analyze(self) -> None:
        """Test method."""
        workflow = SecurityPracticesWorkflowConfigFile.I
        steps = workflow.steps_analyze()
        assert [step["id"] for step in steps] == [
            "checkout-repository",
            "analyze-scorecard",
            "upload-sarif",
        ]

    def test_steps_check_alerts(self) -> None:
        """Test method."""
        workflow = SecurityPracticesWorkflowConfigFile.I
        assert workflow.steps_check_alerts() == [workflow.step_check_alerts()]

    def test_workflow_triggers(self) -> None:
        """Test method."""
        assert SecurityPracticesWorkflowConfigFile.I.workflow_triggers() == {
            "workflow_call": {},
        }
