"""Secrets scanner command construction and badge metadata."""

import re
from typing import Any, override

from pyrig.core.subprocesses import Args
from pyrig.rig.tools.security.secrets import SecretsChecker as BaseSecretsChecker


class SecretsChecker(BaseSecretsChecker):
    """Customize detect-secrets for generated Best Practices criteria."""

    @override
    def check_hook(self) -> dict[str, Any]:
        """Exclude only the generated Best Practices assessment file."""
        from pyrig_openssf.rig.configs.best_practices import (  # noqa: PLC0415
            BestPracticesConfigFile,
        )

        hook = super().check_hook()
        path = re.escape(BestPracticesConfigFile.I.path().as_posix())
        hook.setdefault("args", []).extend(
            Args(f"--exclude-files=^{path}$"),
        )
        return hook
