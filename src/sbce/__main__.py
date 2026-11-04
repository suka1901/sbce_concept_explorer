"""Lets you start the tool with `python -m sbce` or by running this file directly (e.g. VS Code's Run button)."""
import sys
from pathlib import Path

if not __package__:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sbce.cli import main  # noqa: E402

main()
