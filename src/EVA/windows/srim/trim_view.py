from PyQt6.QtCore import pyqtSignal

from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QWidget,
    QLineEdit,
    QGridLayout,
    QComboBox,
    QTabWidget,
    QTableWidgetItem,
    QMenuBar,
    QFileDialog,
    QVBoxLayout,
    QFormLayout, QMessageBox
)
from EVA.widgets.plot.plot_widget import PlotWidget
from EVA.widgets.base.base_table import BaseTable
from EVA.core.app import get_config, get_app


class TrimView(QWidget):
    sim_button_clicked_s = pyqtSignal(dict)
    plot_whole_s = pyqtSignal(int, str)
    plot_comp_s = pyqtSignal(int, str)
    save_s = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("TRIM Simulations")
        self.setMinimumSize(1100, 600)

        # Load default directories from config
        config = get_config()
        default_SRIM_directory = config["SRIM"]["installation_directory"] # C:/SRIM2013
        default_SRIM_output_directory = config["SRIM"]["output_directory"] # C:/SRIM2013/SRIM Outputs

        # setting up buttons
        self.run_sim_button = QPushButton("Run Simulations")

        # Setting up defaults (to add load from file)
        self.SampleName = QLineEdit('Cu')
        self.SimType = QComboBox()
        self.SimType.addItem('Mono')
        self.SimType.addItem('Momentum Spread')
        self.Momentum = QLineEdit('27.0')
        self.MomentumSpread = QLineEdit('4.0')
        self.ScanType = QComboBox()
        self.ScanType.addItem('No')
        self.ScanType.addItem('Yes')
        self.MinMomentum = QLineEdit('21.0')
        self.MaxMomentum = QLineEdit('30.0')
        self.StepMomentum = QLineEdit('1.0')
        self.SRIMdir = QLineEdit(default_SRIM_directory)
        self.TRIMOutDir = QLineEdit(default_SRIM_output_directory)
        self.Stats = QLineEdit('100')

        self.bar = QMenuBar()
        #self.bar.setFixedHeight(25)

        file = self.bar.addMenu('File')

        self.file_load = file.addAction('Load SRIM Settings')
        self.file_save = file.addAction('Save SRIM Settings')

        # set up containers and layouts
        self.trim_settings_container = QWidget()
        self.trim_settings_layout = QFormLayout()

        # main layout to hold menu bar and page contents
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # content container to hold page contents
        self.content_layout = QGridLayout()
        self.content_container = QWidget()

        self.tab1_layout = QVBoxLayout()
        self.tab2_layout = QVBoxLayout()

        # size constraints
        self.trim_settings_container.setFixedWidth(600)

        # set up plot window
        self.plot = PlotWidget()

        # set up trim settings panel
        self.trim_settings_layout.addRow(QLabel('Sample Name'), self.SampleName)
        self.trim_settings_layout.addRow(QLabel('Simulation Type'), self.SimType)
        self.trim_settings_layout.addRow(QLabel('Momentum'), self.Momentum)
        self.trim_settings_layout.addRow(QLabel('Momentum Spread'), self.MomentumSpread)
        self.trim_settings_layout.addRow(QLabel('Scan Momentum'), self.ScanType)
        self.trim_settings_layout.addRow(QLabel('Min Momentum'), self.MinMomentum)
        self.trim_settings_layout.addRow(QLabel('Max Momentum'), self.MaxMomentum)
        self.trim_settings_layout.addRow(QLabel('Momentum Step'), self.StepMomentum)
        self.trim_settings_layout.addRow(QLabel('SRIM.exe directory'), self.SRIMdir)
        self.trim_settings_layout.addRow(QLabel('TRIM output directory'), self.TRIMOutDir)
        self.trim_settings_layout.addRow(QLabel('Stats for optimal Run'), self.Stats)

        self.trim_settings_layout.addRow(self.run_sim_button)

        # Initialize tab screen

        self.tabs = QTabWidget()
        self.tabs.setFixedWidth(600)

        self.tab1 = QWidget()
        self.tab2 = QWidget()

        # Add tabs
        self.tabs.addTab(self.tab1, "Layers")
        self.tabs.addTab(self.tab2, "Results")

        self.tab1.table_TRIMsetup = BaseTable(self.tab1)

        self.tab1.table_TRIMsetup.setShowGrid(True)
        self.tab1.table_TRIMsetup.setColumnCount(3)
        self.tab1.table_TRIMsetup.setRowCount(5)

        self.tab1.table_TRIMsetup.setHorizontalHeaderLabels(['Sample', 'Thickness (mm)', 'Density'])
        self.tab1.table_TRIMsetup.setItem(0, 0, QTableWidgetItem('Beamline Window'))
        self.tab1.table_TRIMsetup.setItem(0, 1, QTableWidgetItem('0.05'))
        self.tab1.table_TRIMsetup.setItem(1, 0, QTableWidgetItem('Air (compressed)'))
        self.tab1.table_TRIMsetup.setItem(1, 1, QTableWidgetItem('0.067'))
        self.tab1.table_TRIMsetup.setItem(2, 0, QTableWidgetItem('Al'))
        self.tab1.table_TRIMsetup.setItem(2, 1, QTableWidgetItem('0.05'))
        self.tab1.table_TRIMsetup.setItem(2, 2, QTableWidgetItem('2.7'))
        self.tab1.table_TRIMsetup.setItem(3, 0, QTableWidgetItem('Cu'))
        self.tab1.table_TRIMsetup.setItem(3, 1, QTableWidgetItem('0.5'))
        self.tab1.table_TRIMsetup.setItem(3, 2, QTableWidgetItem('6.7'))

        # adding tab1 components to layout
        self.tab1_layout.addWidget(self.tab1.table_TRIMsetup)
        self.tab1.setLayout(self.tab1_layout)

        self.tab2.table_PlotRes = BaseTable(self.tab2)

        self.tab2.table_PlotRes.setShowGrid(True)
        self.tab2.table_PlotRes.setColumnCount(5)
        self.tab2.table_PlotRes.setRowCount(100)


        self.tab2.table_PlotRes.setHorizontalHeaderLabels(
            ['Momentum', '% Component', 'Plot Results (Com)', 'Plot Results2',' Save Results'])

        # set up results table
        self.plot_comp_buttons = []
        self.plot_whole_buttons = []
        self.save_buttons = []

        # adding tab2 components to layout
        self.tab2_layout.addWidget(self.tab2.table_PlotRes)
        self.tab2.setLayout(self.tab2_layout)

        # set layouts to containers
        self.trim_settings_container.setLayout(self.trim_settings_layout)
        self.content_container.setLayout(self.content_layout)

        self.content_layout.addWidget(self.trim_settings_container, 0, 0)
        self.content_layout.addWidget(self.plot, 0, 1, 2, 1)
        self.content_layout.addWidget(self.tabs, 1, 0)

        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.bar)
        self.main_layout.addWidget(self.content_container)

    def get_table_data(self):
        table = self.tab1.table_TRIMsetup
        layers = []
        n_rows = table.rowCount()
        for i in range(n_rows):

            # skip current iteration if line empty
            if table.item(i, 0) is None or table.item(i, 0).text().strip() == "":
                continue

            sample_name = table.item(i, 0).text().strip()
            thickness = float(table.item(i, 1).text().strip())
            layer = {"name": sample_name, "thickness": thickness}

            if table.item(i, 2) is not None:
                layer["density"] = float(table.item(i, 2).text().strip())

            layers.append(layer)

        return layers

    def add_trimsetup_row(self):
        table = self.tab1.table_TRIMsetup
        current_count = table.rowCount()
        table.setRowCount(current_count+1)

    def set_table_data(self, table_data):
        table = self.tab1.table_TRIMsetup
        table.setRowCount(len(table_data)+1)
        for row, layer in enumerate(table_data):
            table.setItem(row, 0, QTableWidgetItem(layer["name"]))
            table.setItem(row, 1, QTableWidgetItem(str(layer["thickness"])))

            density = layer.get("density", None)
            if density is not None:
                table.setItem(row, 2, QTableWidgetItem(str(density)))

    # display results to table and set up connections
    def setup_results_table(self, momenta, components):
        table = self.tab2.table_PlotRes
        n_rows = len(momenta)

        self.tab2.table_PlotRes.setRowCount(n_rows)

        for row in range(n_rows):
            momentumstr = str(momenta[row])
            comp = components[row]

            table.setItem(row, 0, QTableWidgetItem(momentumstr))
            table.setItem(row, 1, QTableWidgetItem(comp))

            plot_whole_btn = QPushButton()
            plot_whole_btn.setText('Plot Whole' + str(row + 1))
            table.setCellWidget(row, 2, plot_whole_btn)

            plot_whole_btn.clicked.connect(
                lambda _, r=row, m=momentumstr: self.plot_whole_s.emit(r, m))

            plot_comp_btn = QPushButton()
            plot_comp_btn.setText('Plot Com' + str(row + 1))
            table.setCellWidget(row, 3, plot_comp_btn)

            plot_comp_btn.clicked.connect(
                lambda _, r=row, m=momentumstr: self.plot_comp_s.emit(r, m))

            save_btn = QPushButton()
            save_btn.setText('Save ' + str(row + 1))
            table.setCellWidget(row, 4, save_btn)

            save_btn.clicked.connect(
                lambda _, r=row: self.save_s.emit(r))


    def get_form_data(self):
        form_data = {
            "sample_name": self.SampleName.text(),
            "stats": float(self.Stats.text()),
            "srim_dir": self.SRIMdir.text(),
            "output_dir": self.TRIMOutDir.text(),
            "momentum": float(self.Momentum.text()),
            "sim_type": self.SimType.currentText(),
            "momentum_spread": float(self.MomentumSpread.text()),
            "min_momentum": float(self.MinMomentum.text()),
            "max_momentum": float(self.MaxMomentum.text()),
            "step_momentum": float(self.StepMomentum.text()),
            "scan_type": self.ScanType.currentText()
        }

        return form_data

    def set_form_data(self, form_data):
        self.SampleName.setText(form_data["sample_name"]),
        self.Stats.setText(str(form_data["stats"])),
        self.SRIMdir.setText(form_data["srim_dir"]),
        self.TRIMOutDir.setText(form_data["output_dir"]),
        self.Momentum.setText(str(form_data["momentum"])),
        self.SimType.setCurrentText(form_data["sim_type"]),
        self.MomentumSpread.setText(str(form_data["momentum_spread"])),
        self.MinMomentum.setText(str(form_data["min_momentum"])),
        self.MaxMomentum.setText(str(form_data["max_momentum"])),
        self.StepMomentum.setText(str(form_data["step_momentum"])),
        self.ScanType.setCurrentText(form_data["scan_type"])

    def closeEvent(self, event):
        # close window cleanly
        app = get_app()
        app.trim_window = None
        event.accept()

    def show_error_box(self, text, title="Error"):
        _ = QMessageBox.critical(self, title, text, QMessageBox.StandardButton.Ok)


    def request_save_file(self):
        return QFileDialog.getSaveFileName(self, caption="Save TRIM/SRIM Settings")[0]

    def request_load_file(self):
        return QFileDialog.getOpenFileName(self, caption = "Load TRIM/SRIM Settings")[0]

    def file_save(self,SampleName, SimType, Momentum, MomentumSpread, ScanType, MinMomentum, MaxMomentum,
                   StepMomentum, SRIMdir, TRIMOutDir, Stats):
        print('in save file')
        save_file = QFileDialog.getSaveFileName(self, caption = "Save TRIM/SRIM Settings")
        print(save_file[0])
        file2 = open(save_file[0], "w")
        file2.writelines('Sample Name\n')
        out = SampleName.text()+'\n'
        file2.writelines(out)
        file2.writelines('SimType\n')
        out = SimType.currentText()+'\n'
        file2.writelines(out)
        file2.writelines('Momentum\n')
        out = Momentum.text()+'\n'
        file2.writelines(out)
        file2.writelines('Momentum Spread\n')
        out = MomentumSpread.text()+'\n'
        file2.writelines(out)
        file2.writelines('Scan Momentum\n')
        out = ScanType.currentText()+'\n'
        file2.writelines(out)
        file2.writelines('Min Momentum\n')
        out = MinMomentum.text()+'\n'
        file2.writelines(out)
        file2.writelines('Max Momentum\n')
        out = MaxMomentum.text()+'\n'
        file2.writelines(out)
        file2.writelines('Momentum Step\n')
        out = StepMomentum.text()+'\n'
        file2.writelines(out)
        file2.writelines('SRIM.exe dir\n')
        out = SRIMdir.text()+'\n'
        file2.writelines(out)
        file2.writelines('Output dir\n')
        out = TRIMOutDir.text()+'\n'
        file2.writelines(out)
        file2.writelines('Stats\n')
        out = Stats.text()+'\n'
        file2.writelines(out)
        file2.writelines('Sample\n')

        for j in range(10):
            line = ''
            for i in range(5):
                print(j,i)
                try:
                    line += self.tab1.table_TRIMsetup.item(j, i).text()+','
                except:
                    line +=','

            file2.writelines(line+'\n')
        file2.close()

    def file_load(self,SampleName, SimType, Momentum, MomentumSpread, ScanType, MinMomentum, MaxMomentum,
                   StepMomentum, SRIMdir, TRIMOutDir, Stats):
        print('in load file')
        load_file = QFileDialog.getOpenFileName(self, caption = "Load TRIM/SRIM Settings")
        print(load_file[0])
        file2 = open(load_file[0], "r")
        ignore = file2.readline()
        print(ignore)
        SampleName.setText(file2.readline().strip())
        print(SampleName.text())
        ignore = file2.readline()
        SimType.setCurrentText(file2.readline().strip())
        ignore = file2.readline()
        Momentum.setText(file2.readline().strip())
        ignore = file2.readline()
        MomentumSpread.setText(file2.readline().strip())
        ignore = file2.readline()
        ScanType.setCurrentText(file2.readline().strip())
        ignore = file2.readline()
        MinMomentum.setText(file2.readline().strip())
        ignore = file2.readline()
        MaxMomentum.setText(file2.readline().strip())
        ignore = file2.readline()
        StepMomentum.setText(file2.readline().strip())
        ignore = file2.readline()
        SRIMdir.setText(file2.readline().strip())
        ignore = file2.readline()
        TRIMOutDir.setText(file2.readline().strip())
        ignore = file2.readline()
        Stats.setText(file2.readline().strip())
        ignore = file2.readline()

        line = []

        for j in range(10):
            line = file2.readline().split(',')
            print(line)
            for i in range(5):
                print(j,i)
                try:
                    self.tab1.table_TRIMsetup.setItem(j, i, QTableWidgetItem(line[i]))
                except:
                    print('load finished')

        file2.close()
