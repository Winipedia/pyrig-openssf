"""Tests for the customized detect-secrets scanner."""

import re

from pyrig.rig.tools.security.secrets import SecretsChecker as BaseSecretsChecker

from pyrig_openssf.rig.configs.best_practices import BestPracticesConfigFile
from pyrig_openssf.rig.tools.security.secrets import SecretsChecker


class TestSecretsChecker:
    """Test the assessment-file exclusion."""

    def test_check_hook(self) -> None:
        """Return the base hook with the assessment-file exclusion appended."""
        expected = BaseSecretsChecker().check_hook()
        path = re.escape(BestPracticesConfigFile.I.path().as_posix())
        expected.setdefault("args", []).append(f"--exclude-files=^{path}$")
        assert SecretsChecker.I.check_hook() == expected
