import os
import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QComboBox, QPushButton, QCalendarWidget,
                               QTextBrowser, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy)
from PySide6 import QtGui
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from Gerenciador_Atividades import GerenciamentoAtividades
from Banco_Dados import lista_cursos, lista_turmas, lista_avaliacoes


class InterfaceGerenciadorAtividades(QMainWindow):
    def __init__(self):
        super().__init__()
        self.gerenciamento_atividades = GerenciamentoAtividades()

        base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, "icones")

        self.setWindowTitle("Cadastro de Atividades Avaliativas")
        icon_title_path = os.path.join(icon_path, "ReviewsManager.ico")
        self.setWindowIcon(QtGui.QIcon(icon_title_path))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.create_widgets()

    def center_on_screen(self):
        screen_geometry = QApplication.primaryScreen().geometry()
        center_point = screen_geometry.center()
        self.move(center_point - self.rect().center())

    def showEvent(self, event):
        self.center_on_screen()
        super().showEvent(event)

    def create_widgets(self):
        layout_horizontal_1 = QHBoxLayout()

        layout_vertical_1 = QVBoxLayout()

        self.label_curso = QLabel("Curso:")
        self.combo_curso = QComboBox()
        self.combo_curso.setMinimumWidth(300)
        self.combo_curso.setMaximumWidth(300)
        self.combo_curso.addItems(lista_cursos)
        self.combo_curso.currentTextChanged.connect(self.update_ementa)
        layout_vertical_1.addWidget(self.label_curso)
        layout_vertical_1.addWidget(self.combo_curso)

        self.label_ementa = QLabel("Ementa:")
        self.entry_ementa = QComboBox()
        self.entry_ementa.setMinimumWidth(300)
        self.entry_ementa.setMaximumWidth(300)
        self.entry_ementa.currentTextChanged.connect(self.update_semestre)
        layout_vertical_1.addWidget(self.label_ementa)
        layout_vertical_1.addWidget(self.entry_ementa)

        self.label_semestre = QLabel("Semestre:")
        self.entry_semestre = QComboBox()
        self.entry_semestre.setMinimumWidth(300)
        self.entry_semestre.setMaximumWidth(300)
        self.entry_semestre.currentTextChanged.connect(self.update_disciplinas)
        layout_vertical_1.addWidget(self.label_semestre)
        layout_vertical_1.addWidget(self.entry_semestre)

        self.label_disciplina = QLabel("Disciplina:")
        self.entry_disciplina = QComboBox()
        self.entry_disciplina.setMinimumWidth(300)
        self.entry_disciplina.setMaximumWidth(300)
        layout_vertical_1.addWidget(self.label_disciplina)
        layout_vertical_1.addWidget(self.entry_disciplina)

        self.label_codigo = QLabel("Turma da Disciplina:")
        self.entry_codigo = QComboBox()
        self.entry_codigo.setMinimumWidth(300)
        self.entry_codigo.setMaximumWidth(300)
        self.entry_codigo.addItems(lista_turmas)
        layout_vertical_1.addWidget(self.label_codigo)
        layout_vertical_1.addWidget(self.entry_codigo)

        self.label_tipo = QLabel("Tipo de Atividade Avaliativa:")
        self.combo_tipo = QComboBox()
        self.combo_tipo.setMinimumWidth(300)
        self.combo_tipo.setMaximumWidth(300)
        self.combo_tipo.addItems(lista_avaliacoes)
        layout_vertical_1.addWidget(self.label_tipo)
        layout_vertical_1.addWidget(self.combo_tipo)

        self.label_sequencia = QLabel("Sequência da Atividade:")
        self.combo_sequencia = QComboBox()
        self.combo_sequencia.setMinimumWidth(300)
        self.combo_sequencia.setMaximumWidth(300)
        self.combo_sequencia.addItems([""] + [str(i) for i in range(1, 11)])
        layout_vertical_1.addWidget(self.label_sequencia)
        layout_vertical_1.addWidget(self.combo_sequencia)

        self.label_data = QLabel("Defina a Data da Atividade:")
        self.calendar = QCalendarWidget()
        self.calendar.setMinimumWidth(300)
        self.calendar.setMaximumWidth(300)
        self.calendar.setMaximumHeight(200)
        layout_vertical_1.addWidget(self.label_data)
        layout_vertical_1.addWidget(self.calendar)

        layout_botaoes = QHBoxLayout()

        layout_sub_vertical_1 = QVBoxLayout()

        layout_sub_vertical_2 = QVBoxLayout()

        button_clear_ultima = self.create_button("Limpar Última Entrada")
        button_clear_ultima.clicked.connect(self.limpar_ultima_entrada)
        button_clear = self.create_button("Limpar Tudo")
        button_clear.clicked.connect(self.limpar_entradas)
        button_submiter = self.create_button("Registrar Definições")
        button_submiter.clicked.connect(self.submiter)
        button_export = self.create_button("Exportar para PDF")
        button_export.clicked.connect(self.exportar_para_pdf)

        layout_sub_vertical_1.addWidget(button_clear_ultima)
        layout_sub_vertical_1.addWidget(button_clear)
        layout_sub_vertical_2.addWidget(button_submiter)
        layout_sub_vertical_2.addWidget(button_export)
        layout_sub_vertical_1.setAlignment(button_clear_ultima, Qt.AlignmentFlag.AlignLeft)
        layout_sub_vertical_1.setAlignment(button_clear, Qt.AlignmentFlag.AlignLeft)
        layout_sub_vertical_2.setAlignment(button_submiter, Qt.AlignmentFlag.AlignRight)
        layout_sub_vertical_2.setAlignment(button_export, Qt.AlignmentFlag.AlignRight)

        layout_botaoes.addLayout(layout_sub_vertical_1)
        layout_botaoes.addLayout(layout_sub_vertical_2)
        layout_vertical_1.addLayout(layout_botaoes)
        layout_vertical_1.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout_horizontal_1.addLayout(layout_vertical_1)

        layout_vertical_2 = QVBoxLayout()

        self.label_banco_dados = QLabel("Caixa de Dados:")
        self.textbox = QTextBrowser()
        self.textbox.setMinimumWidth(600)
        layout_vertical_2.addWidget(self.label_banco_dados)
        layout_vertical_2.addWidget(self.textbox)
        layout_horizontal_1.addLayout(layout_vertical_2)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout_horizontal_1)

        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.gerenciamento_atividades.textbox = self.textbox
        self.gerenciamento_atividades.combo_curso = self.combo_curso
        self.gerenciamento_atividades.entry_codigo = self.entry_codigo
        self.gerenciamento_atividades.combo_tipo = self.combo_tipo
        self.gerenciamento_atividades.combo_sequencia = self.combo_sequencia
        self.gerenciamento_atividades.calendar = self.calendar
        self.gerenciamento_atividades.entry_disciplina = self.entry_disciplina
        self.gerenciamento_atividades.entry_ementa = self.entry_ementa
        self.gerenciamento_atividades.entry_semestre = self.entry_semestre

        self.update_textbox()

    def create_button(self, text):
        button = QPushButton(text)
        button.setMinimumWidth(14 * button.fontMetrics().horizontalAdvance('m'))
        button.setMaximumWidth(14 * button.fontMetrics().horizontalAdvance('m'))
        button.setFont(QFont('Arial', 9))
        return button

    def submiter(self):
        self.gerenciamento_atividades.submiter()

    def limpar_entradas(self):
        self.gerenciamento_atividades.limpar_entradas()

    def limpar_ultima_entrada(self):
        self.gerenciamento_atividades.limpar_ultima_entrada()

    def exportar_para_pdf(self):
        self.gerenciamento_atividades.exportar_para_pdf()

    def update_textbox(self):
        self.gerenciamento_atividades.update_textbox()

    def update_ementa(self):
        self.gerenciamento_atividades.update_ementa()

    def update_semestre(self):
        self.gerenciamento_atividades.update_semestre()

    def update_disciplinas(self):
        self.gerenciamento_atividades.update_disciplinas()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InterfaceGerenciadorAtividades()
    window.show()
    sys.exit(app.exec())
