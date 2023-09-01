# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Copyright © 2023, Tiarnach Ó Riada
#
# Licensed under the terms of the Apache Software License 2.0
# ----------------------------------------------------------------------------
"""
PyGMID Plugin Plugin.
"""

# Third-party imports
from qtpy.QtGui import QIcon

# Spyder imports
from spyder.api.plugins import Plugins, SpyderDockablePlugin
from spyder.api.shellconnect.mixins import ShellConnectMixin
from spyder.api.translations import get_translation

# Local imports
from spyder_pygmid.spyder.widgets.confpage import PyGMIDPluginConfigPage
from spyder_pygmid.spyder.widgets.main_widget import PyGMIDPluginWidget

_ = get_translation("spyder_pygmid.spyder")


class PyGMIDPlugin(SpyderDockablePlugin, ShellConnectMixin):
    """
    PyGMID Plugin plugin.
    """

    NAME = "spyder_pygmid"
    REQUIRES = [Plugins.IPythonConsole]
    OPTIONAL = []
    WIDGET_CLASS = PyGMIDPluginWidget
    CONF_SECTION = NAME
    CONF_WIDGET_CLASS = PyGMIDPluginConfigPage
    TABIFY = [Plugins.VariableExplorer]

    # --- Signals

    # --- SpyderDockablePlugin API
    # ------------------------------------------------------------------------
    @staticmethod
    def get_name():
        return _("PyGMID Plugin")

    def get_description(self):
        return _("Use PyGMID sweep and lookup within spyder")

    def get_icon(self):
        return QIcon("icon.png")

    def on_initialize(self):
        widget = self.get_widget()
        
    # ShellConnectMixin requires this
    def current_widget(self):
        return self.get_widget().current_widget()

    def check_compatibility(self):
        valid = True
        message = ""  # Note: Remember to use _("") to localize the string
        return valid, message

    def on_close(self, cancellable=True):
        return True

    # --- Public API
    # ------------------------------------------------------------------------
