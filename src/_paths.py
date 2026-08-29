"""Reproducible paths for the analysis pipeline.

Every script resolves the data and output directories from the repository
root (the folder that contains src/), so the pipeline runs identically on
any machine. Both can be overridden with the environment variables
ITAPEMA_DATA and ITAPEMA_OUT for specialised setups.
"""
import atexit
import io
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

RAW = Path(os.environ.get('ITAPEMA_DATA', ROOT / 'data'))
OUT = Path(os.environ.get('ITAPEMA_OUT', ROOT / 'output'))
OUT.mkdir(parents=True, exist_ok=True)

LOGS = OUT / 'logs'
LOGS.mkdir(parents=True, exist_ok=True)


def setup():
    """Ensure the output tree exists and return (RAW, OUT)."""
    OUT.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)
    return RAW, OUT


class _Tee(io.TextIOBase):
    """A writable stdout that mirrors to a log file."""

    def __init__(self, stream, fileobj):
        self._stream = stream
        self._fileobj = fileobj

    def writable(self):
        return True

    def write(self, data):
        self._stream.write(data)
        self._fileobj.write(data)
        return len(data)

    def flush(self):
        try:
            self._stream.flush()
            self._fileobj.flush()
        except ValueError:
            pass


def tee(logname):
    """Mirror stdout/console to <OUT>/logs/<logname> and to the console."""
    path = LOGS / logname
    f = open(path, 'w', buffering=1)
    tee.std = _Tee(sys.stdout, f)

    def _close():
        try:
            tee.std.flush()
            f.close()
        except Exception:
            pass

    atexit.register(_close)
    sys.stdout = tee.std
    return path


tee.std = None