import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                             QGridLayout, QWidget, QLabel, QLineEdit, QPushButton,
                             QTextEdit, QGroupBox, QFrame, QMessageBox, QTabWidget)
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QFont, QRegExpValidator, QPalette, QColor, QPixmap
import math


class EnergyCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_validators()
        self.setup_connections()

    def init_ui(self):
        self.setWindowTitle("Dimensionnement Énergétique - MARIA NACHID")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QGroupBox {
                font-weight: bold;
                font-size: 12px;
                border: 2px solid #cccccc;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #2c3e50;
            }
            QLabel {
                font-size: 11px;
                color: #2c3e50;
                font-weight: 500;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                font-size: 11px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #3498db;
                background-color: #ecf0f1;
            }
            QPushButton {
                padding: 10px 20px;
                border: none;
                border-radius: 6px;
                font-size: 12px;
                font-weight: bold;
                color: white;
            }
            QPushButton#calculateBtn {
                background-color: #3498db;
            }
            QPushButton#calculateBtn:hover {
                background-color: #2980b9;
            }
            QPushButton#clearBtn {
                background-color: #27ae60;
            }
            QPushButton#clearBtn:hover {
                background-color: #229954;
            }
            QPushButton#closeBtn {
                background-color: #e74c3c;
            }
            QPushButton#closeBtn:hover {
                background-color: #c0392b;
            }
            QTextEdit {
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                padding: 5px;
                font-size: 11px;
                background-color: #ecf0f1;
            }
        """)

        # Widget principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Titre
        title_label = QLabel("Dimensionnement Énergétique")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
                padding: 20px;
                background-color: #ecf0f1;
                border-radius: 10px;
                margin-bottom: 20px;
            }
        """)
        main_layout.addWidget(title_label)

        # Créer les onglets
        tab_widget = QTabWidget()
        main_layout.addWidget(tab_widget)

        # Onglet des paramètres d'entrée
        input_tab = QWidget()
        tab_widget.addTab(input_tab, "Paramètres d'entrée")

        # Layout pour l'onglet d'entrée
        input_layout = QHBoxLayout()
        input_tab.setLayout(input_layout)

        # Créer les groupes d'entrée
        self.create_input_groups(input_layout)

        # Onglet des résultats
        output_tab = QWidget()
        tab_widget.addTab(output_tab, "Résultats")

        # Layout pour l'onglet de sortie
        output_layout = QVBoxLayout()
        output_tab.setLayout(output_layout)

        # Créer les groupes de sortie
        self.create_output_groups(output_layout)

        # Boutons
        self.create_buttons(main_layout)

    def create_input_groups(self, parent_layout):
        # Groupe 1: Caractéristiques du véhicule
        vehicle_group = QGroupBox("Caractéristiques du véhicule")
        vehicle_layout = QGridLayout()

        # Entrées du véhicule
        self.masse_edit = self.create_input_field(vehicle_layout, "Masse (kg)", 0)
        self.surface_edit = self.create_input_field(vehicle_layout, "Surface (m²)", 1)
        self.dpneu_edit = self.create_input_field(vehicle_layout, "Dpneu (m)", 2)
        self.cx_edit = self.create_input_field(vehicle_layout, "Cx", 3)
        self.cir_roul_edit = self.create_input_field(vehicle_layout, "Circonférence roulement", 4)

        vehicle_group.setLayout(vehicle_layout)
        parent_layout.addWidget(vehicle_group)

        # Groupe 2: Paramètres de conduite
        driving_group = QGroupBox("Paramètres de conduite")
        driving_layout = QGridLayout()

        self.vmav_edit = self.create_input_field(driving_layout, "Vitesse véhicule (km/h)", 0)
        self.vit_vent_edit = self.create_input_field(driving_layout, "Vitesse vent (km/h)", 1)
        self.acc_edit = self.create_input_field(driving_layout, "Accélération (m/s²)", 2)
        self.pente_edit = self.create_input_field(driving_layout, "Pente (%)", 3)
        self.f_edit = self.create_input_field(driving_layout, "Coefficient roulement", 4)

        driving_group.setLayout(driving_layout)
        parent_layout.addWidget(driving_group)

        # Groupe 3: Paramètres batterie
        battery_group = QGroupBox("Paramètres batterie")
        battery_layout = QGridLayout()

        self.autonomie_edit = self.create_input_field(battery_layout, "Autonomie (km)", 0)
        self.vbat_edit = self.create_input_field(battery_layout, "Tension batterie (V)", 1)
        self.r_char_dechar_edit = self.create_input_field(battery_layout, "Rendement charge/décharge (%)", 2)

        battery_group.setLayout(battery_layout)
        parent_layout.addWidget(battery_group)

    def create_input_field(self, layout, label_text, row):
        label = QLabel(label_text)
        edit = QLineEdit()
        edit.setPlaceholderText(f"Entrez {label_text.lower()}")

        layout.addWidget(label, row, 0)
        layout.addWidget(edit, row, 1)

        return edit

    def create_output_groups(self, parent_layout):
        # Groupe des forces
        forces_group = QGroupBox("Forces calculées")
        forces_layout = QGridLayout()

        self.res_air_output = self.create_output_field(forces_layout, "Force aérodynamique (N)", 0)
        self.res_roul_output = self.create_output_field(forces_layout, "Force résistance roulement (N)", 1)
        self.fpente_output = self.create_output_field(forces_layout, "Force d'inclinaison (N)", 2)
        self.facc_output = self.create_output_field(forces_layout, "Force d'accélération (N)", 3)

        forces_group.setLayout(forces_layout)
        parent_layout.addWidget(forces_group)

        # Groupe des puissances
        power_group = QGroupBox("Puissances et capacité")
        power_layout = QGridLayout()

        self.pui_mot_output = self.create_output_field(power_layout, "Puissance moteur (kW)", 0)
        self.pui_emb_output = self.create_output_field(power_layout, "Puissance embarquée (kWh)", 1)
        self.cbat_output = self.create_output_field(power_layout, "Capacité batterie (Ah)", 2)

        power_group.setLayout(power_layout)
        parent_layout.addWidget(power_group)

    def create_output_field(self, layout, label_text, row):
        label = QLabel(label_text)
        output = QTextEdit()
        output.setMaximumHeight(40)
        output.setReadOnly(True)

        layout.addWidget(label, row, 0)
        layout.addWidget(output, row, 1)

        return output

    def create_buttons(self, parent_layout):
        button_layout = QHBoxLayout()

        self.calculate_btn = QPushButton("Calculer")
        self.calculate_btn.setObjectName("calculateBtn")
        self.calculate_btn.setMinimumWidth(120)

        self.clear_btn = QPushButton("Effacer")
        self.clear_btn.setObjectName("clearBtn")
        self.clear_btn.setMinimumWidth(120)

        self.close_btn = QPushButton("Fermer")
        self.close_btn.setObjectName("closeBtn")
        self.close_btn.setMinimumWidth(120)

        button_layout.addStretch()
        button_layout.addWidget(self.calculate_btn)
        button_layout.addWidget(self.clear_btn)
        button_layout.addWidget(self.close_btn)
        button_layout.addStretch()

        parent_layout.addLayout(button_layout)

    def setup_validators(self):
        # Validateur pour les nombres décimaux
        float_validator = QRegExpValidator(QRegExp(r'^[0-9]*\.?[0-9]*$'))

        # Appliquer les validateurs à tous les champs d'entrée
        input_fields = [
            self.masse_edit, self.surface_edit, self.dpneu_edit, self.cx_edit,
            self.cir_roul_edit, self.vmav_edit, self.vit_vent_edit, self.acc_edit,
            self.pente_edit, self.f_edit, self.autonomie_edit, self.vbat_edit,
            self.r_char_dechar_edit
        ]

        for field in input_fields:
            field.setValidator(float_validator)

    def setup_connections(self):
        self.calculate_btn.clicked.connect(self.calculate)
        self.clear_btn.clicked.connect(self.clear_fields)
        self.close_btn.clicked.connect(self.close)

        # Navigation avec Enter
        input_fields = [
            self.masse_edit, self.surface_edit, self.dpneu_edit, self.cx_edit,
            self.cir_roul_edit, self.vmav_edit, self.vit_vent_edit, self.acc_edit,
            self.pente_edit, self.f_edit, self.autonomie_edit, self.vbat_edit,
            self.r_char_dechar_edit
        ]

        for i, field in enumerate(input_fields):
            if i < len(input_fields) - 1:
                field.returnPressed.connect(input_fields[i + 1].setFocus)
            else:
                field.returnPressed.connect(self.calculate_btn.setFocus)

    def get_float_value(self, field):
        """Récupère la valeur flottante d'un champ avec gestion d'erreur"""
        try:
            text = field.text().strip()
            if not text:
                return 0.0
            return float(text)
        except ValueError:
            return 0.0

    def calculate(self):
        try:
            # Récupération des valeurs
            m = self.get_float_value(self.masse_edit)
            s = self.get_float_value(self.surface_edit)
            c = self.get_float_value(self.cx_edit)
            vm = self.get_float_value(self.vmav_edit)
            vv = self.get_float_value(self.vit_vent_edit)
            ff = self.get_float_value(self.f_edit)
            p = self.get_float_value(self.pente_edit)
            ac = self.get_float_value(self.acc_edit)
            aut = self.get_float_value(self.autonomie_edit)
            rcd = self.get_float_value(self.r_char_dechar_edit)
            vb = self.get_float_value(self.vbat_edit)

            # Validation des valeurs critiques
            if vm == 0:
                QMessageBox.warning(self, "Erreur", "La vitesse du véhicule ne peut pas être zéro.")
                return

            if vb == 0:
                QMessageBox.warning(self, "Erreur", "La tension de la batterie ne peut pas être zéro.")
                return

            # Calculs
            # Force aérodynamique
            v_relative = (vm - vv) * 1000 / 3600  # Conversion km/h en m/s
            rair = 0.5 * 1.225 * s * c * v_relative * v_relative

            # Force de résistance au roulement
            rroulement = m * 9.81 * ff

            # Force d'inclinaison
            fp = m * 9.81 * p / 100

            # Force d'accélération
            fa = m * ac

            # Puissance moteur (kW)
            pmo = (fa + rroulement + rair + fp) * vm / 3600

            # Puissance embarquée (kWh)
            if vm != 0:
                pemb = pmo * aut * rcd / (100 * vm)
            else:
                pemb = 0

            # Capacité batterie (Ah)
            cb = pemb * 1000 / vb

            # Affichage des résultats avec arrondi
            self.res_air_output.setText(f"{rair:.2f}")
            self.res_roul_output.setText(f"{rroulement:.2f}")
            self.fpente_output.setText(f"{fp:.2f}")
            self.facc_output.setText(f"{fa:.2f}")
            self.pui_mot_output.setText(f"{pmo:.2f}")
            self.pui_emb_output.setText(f"{pemb:.2f}")
            self.cbat_output.setText(f"{cb:.2f}")

        except Exception as e:
            QMessageBox.critical(self, "Erreur de calcul", f"Une erreur s'est produite lors du calcul:\n{str(e)}")

    def clear_fields(self):
        # Effacer tous les champs d'entrée
        input_fields = [
            self.masse_edit, self.surface_edit, self.dpneu_edit, self.cx_edit,
            self.cir_roul_edit, self.vmav_edit, self.vit_vent_edit, self.acc_edit,
            self.pente_edit, self.f_edit, self.autonomie_edit, self.vbat_edit,
            self.r_char_dechar_edit
        ]

        for field in input_fields:
            field.clear()

        # Effacer tous les champs de sortie
        output_fields = [
            self.res_air_output, self.res_roul_output, self.fpente_output,
            self.facc_output, self.pui_mot_output, self.pui_emb_output,
            self.cbat_output
        ]

        for field in output_fields:
            field.clear()

        # Remettre le focus sur le premier champ
        self.masse_edit.setFocus()


def main():
    app = QApplication(sys.argv)

    # Style de l'application
    app.setStyle('Fusion')

    # Palette de couleurs
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(240, 240, 240))
    palette.setColor(QPalette.WindowText, Qt.black)
    palette.setColor(QPalette.Base, Qt.white)
    palette.setColor(QPalette.AlternateBase, QColor(245, 245, 245))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.black)
    palette.setColor(QPalette.Text, Qt.black)
    palette.setColor(QPalette.Button, QColor(240, 240, 240))
    palette.setColor(QPalette.ButtonText, Qt.black)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

    # Créer et afficher la fenêtre
    window = EnergyCalculator()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()