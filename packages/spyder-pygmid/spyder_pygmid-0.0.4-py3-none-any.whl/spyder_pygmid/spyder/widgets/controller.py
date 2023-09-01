from pygmid import sweep
import pygmid
import numpy as np
from typing import Callable
from pathlib import Path

from qtpy import PYQT5
from qtpy.QtWidgets import *
from qtpy.QtCore import Qt
from pathlib import Path
import os

from spyder.api.translations import get_translation
from spyder.api.widgets.mixins import SpyderWidgetMixin
_ = get_translation("spyder_pygmid.spyder")

class ControllerTabs(QWidget, SpyderWidgetMixin):
    def __init__(self, parent, shellwidget):
        if PYQT5:
            super().__init__(parent=parent, class_parent=parent)
        else:
            QWidget.__init__(self, parent)
            SpyderWidgetMixin.__init__(self, class_parent=parent)

        self.shellwidget = shellwidget
        self.config_file_path = str(Path(os.getcwd()) / "sweep.cfg")

        self._tabWidget = QTabWidget(parent=self)
        self._tabWidget.addTab(SweepTab(parent=self), _("Sweep"))
        self._tabWidget.addTab(LookupTab(parent=self, execute=self.shellwidget.execute, set_value=self.shellwidget.set_value), _("Lookup"))
        layout = QVBoxLayout()
        layout.addWidget(self._tabWidget)
        self.setLayout(layout)

    def set_shellwidget(self, shellwidget):
        self.shellwidget = shellwidget
        self._refresh()

    def _refresh(self) -> None:
        if self.shellwidget.kernel_client is None:
            return
        self.shellwidget.call_kernel(interrupt=True)

class SweepTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.config_file_path = self.parent().config_file_path

        layout = QHBoxLayout()

        formLayout = QFormLayout()
        
        hlayout = QHBoxLayout()
        
        self._model_file = QLineEdit(self)
        self._model_file.setReadOnly(True)
        hlayout.addWidget(self._model_file)

        self._select_model_file = QPushButton(_("Select"), self)
        self._select_model_file.clicked.connect(self._on_select_model_file)
        hlayout.addWidget(self._select_model_file)
 
        formLayout.addRow(_("Model file"), hlayout)
      
        self._model_info = QLineEdit(self)
        formLayout.addRow(_("Model info"), self._model_info)
        self._corner = QLineEdit("NOM", self)
        formLayout.addRow(_("Corner"), self._corner)
        self._temperature = QLineEdit("300", self)
        formLayout.addRow(_("Temperature"), self._temperature)
        self._model_n = QLineEdit(self)
        formLayout.addRow(_("Model N"), self._model_n)
        self._model_p = QLineEdit(self)
        formLayout.addRow(_("Model P"), self._model_p)
        self._save_file_n = QLineEdit("nch",self)
        formLayout.addRow(_("Save File N"), self._save_file_n)
        self._save_file_p = QLineEdit("pch", self)
        formLayout.addRow(_("Save File P"), self._save_file_p)
        self._mn = QTextEdit(self)
        formLayout.addRow(_("MN"), self._mn)
        self._mp = QTextEdit(self)
        formLayout.addRow(_("MP"), self._mp)
      
        sweepFormLayout = QFormLayout()
        label = QLabel(_("Sweep Parameters"))
        sweepFormLayout.addRow(label)

        self._vgs = QLineEdit(_("(start, stop, step)"))
        sweepFormLayout.addRow(_("VGS"), self._vgs)
        self._vds = QLineEdit(_("(start, stop, step)"))
        sweepFormLayout.addRow(_("VDS"), self._vds)
        self._vsb = QLineEdit(_("(start, stop, step)"))
        sweepFormLayout.addRow(_("VSB"), self._vsb)
        self._length = QLineEdit(_("[(start, stop, step), ...]"))
        sweepFormLayout.addRow(_("Length"), self._length)
        self._width = QLineEdit("1")
        sweepFormLayout.addRow(_("Width"), self._width)
        self._nfing = QLineEdit("1")
        sweepFormLayout.addRow(_("Number of fingers"), self._nfing)

        formLayout.addRow(sweepFormLayout)

        self._generate_config = QPushButton(_("Generate"), parent=self)
        self._generate_config.clicked.connect(self._on_generate_config)
        formLayout.addRow(self._generate_config)

        layout.addLayout(formLayout)

        vlayout = QVBoxLayout()
        self._config_label = QLabel(_("Config File") + f": {self.config_file_path}")
        self._config = QTextEdit(self)
        vlayout.addWidget(self._config_label)
        vlayout.addWidget(self._config)

        self._save_config = QPushButton(_("Save Config"))
        self._save_config.clicked.connect(self._on_save_config)
        vlayout.addWidget(self._save_config)

        layout.addLayout(vlayout)
 
        self.setLayout(layout)

        # Generate a blank config on the right
        self._on_generate_config()

    def _on_select_model_file(self):
        file_name = QFileDialog.getOpenFileName(self, _("Select Model File"), "/", _("Model files (*.scs);;All files (*)"))
        print(file_name)
        if (len(file_name[0]) > 0):
            self._model_file.setText(file_name[0])

    def _on_generate_config(self):
        self._config.setText(self._to_config())
    def _on_save_config(self):
        with open(self.config_file_path, "w+") as f:
            print(f"WRITE CONFIG to {self.config_file_path}: {self._to_config()}")
            f.write(self._config.toPlainText())

    def _to_config(self) -> str:
        return "\n".join([
            "[MODEL]",
            "FILE = " + self._model_file.text(),
            "INFO = " + self._model_info.text(),
            "CORNER = " + self._corner.text(),
            "TEMP = " + self._temperature.text(),
            "MODELN = " + self._model_n.text(),
            "MODELP = " + self._model_p.text(),
            "SAVEFILEN = " +self._save_file_n.text(),
            "SACEFILEP = " + self._save_file_p.text(),
            "PARAMFILE = params.scs",
            "[SWEEP]",
            "VGS = " + self._vgs.text(),
            "VDS = " + self._vds.text(),
            "VSB = " + self._vsb.text(),
            "L = " + self._length.text(),
            "W = " + self._width.text(),
            "NFING = " + self._nfing.text(),
            ])

def run_sweep(config_file="sweep.cfg"):
    if Path(config_file).exists():
        mfn, mfp = sweep.run(config_file, skip_sweep=False)

class LookupTab(QWidget):
    valid_first_vars = ['GM','L','W','VGS','VDS','VSB','ID','VT','IGD','IGS','GMB','GDS','CGG','CGS','CSG','CGD','CDG','CGB','CDD','CSS','STH','SFL']
    valid_second_vars = [None,'ID','L','W','VGS','VDS','VSB','VT','IGD','IGS','GM','GMB','GDS','CGG','CGS','CSG','CGD','CDG','CGB','CDD','CSS','STH','SFL']


    def __init__(self, execute:Callable[[str], None], set_value: Callable[[str, str], None], parent=None):
        super().__init__(parent=parent)
        self.execute = execute
        self.set_value = set_value

        self.lookup:pygmid.Lookup.Lookup = None

        self.setMaximumWidth(720)
        layout = QVBoxLayout()

        headingFont = self.font()
        headingFont.setBold(True)
        headingFont.setPointSize(16)

        formLayout = QFormLayout()

        self._title = QLabel('New Lookup', parent=self)
        self._title.setFont(headingFont)
        formLayout.addRow(self._title)
        
        hlayout = QHBoxLayout()
        
        self._lookup_file = QLineEdit(self)
        self._lookup_file.setReadOnly(True)
        hlayout.addWidget(self._lookup_file)

        self._select_lookup_file = QPushButton(_("Select"), self)
        self._select_lookup_file.clicked.connect(self._on_select_lookup_file)
        hlayout.addWidget(self._select_lookup_file)
 
        formLayout.addRow(_("Lookup file"), hlayout)


        hlayout = QHBoxLayout()

        self._lookup_ratio_11 = QComboBox(self)
        self._lookup_ratio_11.addItems(LookupTab.valid_first_vars)
        self._lookup_ratio_11.currentIndexChanged.connect(self._update_lookup_ratio_1)
        hlayout.addWidget(self._lookup_ratio_11)

        spacer = QLabel("_")
        hlayout.addWidget(spacer)

        self._lookup_ratio_12 = QComboBox(self)
        self._lookup_ratio_12.addItems(LookupTab.valid_second_vars)
        self._lookup_ratio_12.currentIndexChanged.connect(self._update_lookup_ratio_1)
        hlayout.addWidget(self._lookup_ratio_12)

        self._lookup_ratio_1 = QLabel("", self)
        self._update_lookup_ratio_1()
        hlayout.addWidget(self._lookup_ratio_1)

        formLayout.addRow(_("Ratio 1"), hlayout)

        formLayout.addRow(QLabel("vs"))

        hlayout = QHBoxLayout()

        self._lookup_ratio_21 = QComboBox(self)
        self._lookup_ratio_21.addItem('')
        self._lookup_ratio_21.addItems(LookupTab.valid_first_vars)
        self._lookup_ratio_21.currentIndexChanged.connect(self._update_lookup_ratio_2)
        hlayout.addWidget(self._lookup_ratio_21)

        spacer = QLabel("_")
        hlayout.addWidget(spacer)

        self._lookup_ratio_22 = QComboBox(self)
        self._lookup_ratio_22.addItems(LookupTab.valid_second_vars)
        self._lookup_ratio_22.currentIndexChanged.connect(self._update_lookup_ratio_2)
        hlayout.addWidget(self._lookup_ratio_22)

        self._lookup_ratio_2 = QLabel("", self)
        self._update_lookup_ratio_2()
        hlayout.addWidget(self._lookup_ratio_2)

        self._lookup_ratio_2_value = QLineEdit(self)
        self._lookup_ratio_2_value.setMaximumWidth(200)
        hlayout.addWidget(self._lookup_ratio_2_value)


        formLayout.addRow(_("Ratio 2"), hlayout)
        

        # self._add_independent_var = QPushButton(_("Define Variable"), parent=self)
        # self._add_independent_var.clicked.connect(self._on_add_independent_var)
        # formLayout.addRow(self._add_independent_var)
        paramFormLayout = QFormLayout()

        self._param_L = QLineEdit(self)
        paramFormLayout.addRow(_("Length"), self._param_L)
        self._param_VGS = QLineEdit(self)
        paramFormLayout.addRow(_("VGS"), self._param_VGS)
        self._param_VDS = QLineEdit(self)
        paramFormLayout.addRow(_("VDS"), self._param_VDS)
        self._param_VSB = QLineEdit(self)
        paramFormLayout.addRow(_("VSB"), self._param_VSB)
        self._param_VGB = QLineEdit(self)
        paramFormLayout.addRow(_("VGB"), self._param_VGB)
        self._param_GM_ID = QLineEdit(self)
        paramFormLayout.addRow(_("GM_ID"), self._param_GM_ID)
        self._param_ID_W = QLineEdit(self)
        paramFormLayout.addRow(_("ID_W"), self._param_ID_W)
        self._param_VDB = QLineEdit(self)
        paramFormLayout.addRow(_("VDB"), self._param_VDB)

        formLayout.addRow(_("where"), paramFormLayout)

        self._statusText = QLabel('', self)
        self._statusText.setTextInteractionFlags(Qt.TextSelectableByMouse)
        formLayout.addRow(self._statusText)

        self._lookup = QPushButton(_("Lookup"), parent=self)
        self._lookup.clicked.connect(self._on_lookup)
        formLayout.addRow(self._lookup)


        layout.addLayout(formLayout)


        self.setLayout(layout)

    def _update_lookup_ratio_1(self):
        is_ratio = self._lookup_ratio_12.currentIndex() >0
        self._lookup_ratio_1.setText(self._lookup_ratio_11.currentText()+('_' if is_ratio else '')+self._lookup_ratio_12.currentText())
    def _update_lookup_ratio_2(self):
        is_ratio = self._lookup_ratio_22.currentIndex() >0
        self._lookup_ratio_2.setText(self._lookup_ratio_21.currentText()+('_' if is_ratio else '')+self._lookup_ratio_22.currentText())

    def _on_select_lookup_file(self):
        file_name = QFileDialog.getOpenFileName(self, _("Select Lookup File"), "/", _("Lookup files (*.pkl);;All files (*)"))
        print(file_name)
        if (len(file_name[0]) > 0):
            self._lookup_file.setText(file_name[0])
            self.lookup = pygmid.Lookup(file_name[0])
            self._title.setText(f"Model info: {self.lookup['INFO']}")

    def _field_to_value(self, key:str, value: str, allowed_types=[tuple, int, float]):
        if not len(value) > 0:
            return None
        built = eval(value, {'__builtins__':None})
        if type(built) == tuple:
            if len(built) == 2:
                return np.arange(built[0], built[1])
            elif len(built) == 3:
                return  np.arange(built[0], built[1], built[2])
            else:
                raise TypeError("{value} is not a valid value for {key}: too short")
        elif type(built) == int or type(built) == float:
            return built
        else:
            raise TypeError("{value} is not a valid value for {key}: too short")

    def _on_lookup(self):
        with_defaults = {}
        no_defaults = {}
        L = self._field_to_value('L', self._param_L.text())
        VGS = self._field_to_value('VGS', self._param_VGS.text())
        VDS = self._field_to_value('VDS', self._param_VDS.text())
        VSB = self._field_to_value('VDS', self._param_VSB.text())
        VGB = self._field_to_value('VDS', self._param_VGB.text())
        GM_ID = self._field_to_value('VDS', self._param_GM_ID.text())
        ID_W = self._field_to_value('VDS', self._param_ID_W.text())
        VDB = self._field_to_value('VDS', self._param_VDB.text())
        if L is not None: with_defaults['L'] = L
        if VGS is not None: with_defaults['VGS'] = VGS
        if VDS is not None: with_defaults['VDS'] = VDS
        if VSB is not None: with_defaults['VSB'] = VSB
        if VGB is not None: no_defaults['VGB'] = VGB
        if GM_ID is not None: no_defaults['GM_ID'] = GM_ID
        if ID_W is not None: no_defaults['ID_W'] = ID_W
        if VDB is not None: no_defaults['VDB'] = VDB
        # {
        #     'L'     :   params.get('L', min(self.lookup['L'])),
        #     'VGS'   :   params.get('VGS', self.lookup['VGS']),
        #     'VDS'   :   params.get('VDS', max(self.lookup['VDS'])/2),
        #     'VSB'   :   params.get('VSB', 0.0),
        #     'METHOD':   params.get('METHOD', 'pchip'),
        #     'VGB'   :   params.get('VGB', None),
        #     'GM_ID' :   params.get('GM_ID', None),
        #     'ID_W'  :   params.get('ID_W', None),
        #     'VDB'   :   params.get('VDB', None)
        # }
        
        ratio1 = self._lookup_ratio_1.text()
        ratio2 = self._lookup_ratio_2.text()
        if len(ratio2) > 0:
            ratio2_val = self._field_to_value(ratio2, self._lookup_ratio_2_value.text())
            data = self.lookup.look_up(
                ratio1, 
                **{ratio2: ratio2_val},
                **no_defaults,
                L=with_defaults.get('L', min(self.lookup['L'])),
                VGS=with_defaults.get('VGS', self.lookup['VGS']),
                VDS=with_defaults.get('VDS', max(self.lookup['VDS'])/2),
                VSB=with_defaults.get('VSB', 0.0),
            )
            self.set_value('lookup', self.lookup)
            self.set_value('data', data)
            self._statusText.setText("Loaded `lookup` and generated `data` into console. Try `plt.plot(lookup['<x var>'], data.T) ` for a nice plot!")
        else:
            data = self.lookup.look_up(
                ratio1,
                **no_defaults,
                L=with_defaults.get('L', min(self.lookup['L'])),
                VGS=with_defaults.get('VGS', self.lookup['VGS']),
                VDS=with_defaults.get('VDS', max(self.lookup['VDS'])/2),
                VSB=with_defaults.get('VSB', 0.0),
            )
            self.set_value('lookup', self.lookup)
            self.set_value('data', data)
            self._statusText.setText("Loaded `lookup` and generated `data` into console. Try `plt.plot(lookup['<x var>'], data.T) ` for a nice plot!")
