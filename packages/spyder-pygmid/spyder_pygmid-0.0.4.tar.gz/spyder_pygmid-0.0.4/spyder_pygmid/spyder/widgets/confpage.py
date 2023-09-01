# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Copyright © 2023, Tiarnach Ó Riada
#
# Licensed under the terms of the Apache Software License 2.0
# ----------------------------------------------------------------------------
"""
PyGMID Plugin Preferences Page.
"""
from spyder.api.preferences import PluginConfigPage
from spyder.api.translations import get_translation

_ = get_translation("spyder_pygmid.spyder")


class PyGMIDPluginConfigPage(PluginConfigPage):

    # --- PluginConfigPage API
    # ------------------------------------------------------------------------
    def setup_page(self):
        pass
