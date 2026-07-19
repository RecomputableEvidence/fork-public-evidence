#!/usr/bin/env python3
"""Cross-platform launcher for Fork preservation-integrity verification."""

from __future__ import annotations

import importlib.util
from pathlib import Path, PurePosixPath
import sys


IMPLEMENTATION = Path(__file__).with_name("_check_preservation_integrity_v0_1_impl.py")


def load_implementation():
    spec = importlib.util.spec_from_file_location(
        "_fork_preservation_integrity_v0_1_impl",
        IMPLEMENTATION,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load preservation checker: {IMPLEMENTATION}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    # Archive paths are serialized as repository-relative POSIX paths. Keep the
    # comparison flavor stable on Windows while leaving filesystem paths native.
    module.DEPENDENCY_EXAMPLE_ROOT = PurePosixPath(
        module.DEPENDENCY_EXAMPLE_ROOT.as_posix()
    )
    return module


if __name__ == "__main__":
    raise SystemExit(load_implementation().main())
