import sublime
import sys
# Rename this if you have renamed the package's directory
from PluginLogger import plugin_logger

class _PluginLogWriter33(plugin_logger._PluginLogWriter):
    def __init__(self, pyversion):
        super().__init__(pyversion)


def plugin_loaded():
    sys.stdout = _PluginLogWriter33("3.3")  # type: ignore
    sys.stderr = _PluginLogWriter33("3.3")  # type: ignore


def plugin_unloaded():
    sys.stdout = sublime._LogWriter() # type: ignore
    sys.stderr = sublime._LogWriter() # type: ignore
