import sublime
import sublime_api

import io
import sys
import inspect
import re


class _PluginLogWriter(io.TextIOBase):
    def __init__(self):
        self.buf = None

    def flush(self):
        b = self.buf
        self.buf = None

        if b is None or len(b) == 0:
            return

        # Let's get the call stack without context
        frames = inspect.stack(0)

        if len(frames) < 3:
            sublime_api.log_message(b)

        # Plugin call should be right after 2 frames
        plugin = self.get_plugin(frames[2])
        msg = "[%s]: %s" % (plugin, b) if plugin is not False else b

        sublime_api.log_message(msg)

    def write(self, s):
        if self.buf is None:
            self.buf = s
        else:
            self.buf += s
        if '\n' in s or '\r' in s:
            self.flush()

    def get_plugin(self, frame):
        packages_path = sublime.packages_path()
        installed_packages_path = sublime.installed_packages_path()

        is_packages_path = re.search(r'^%s' % (re.escape(packages_path)), frame[1]) is not None
        is_installed_packages_path = re.search(r'^%s' % (re.escape(installed_packages_path)), frame[1]) is not None

        if is_packages_path is False and is_installed_packages_path is False:
            return False

        if is_packages_path:
            loc = frame[1].replace(packages_path + "\\", "").split("\\")
            return loc[0]

        if is_installed_packages_path:
            loc = frame[1].replace(installed_packages_path + "\\", "").split("\\")
            return loc[0].split(".")[0]


def plugin_loaded():
    sys.stdout = _PluginLogWriter()  # type: ignore
    sys.stderr = _PluginLogWriter()  # type: ignore


def plugin_unloaded():
    sys.stdout = sublime._LogWriter() # type: ignore
    sys.stderr = sublime._LogWriter() # type: ignore
