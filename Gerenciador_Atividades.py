import sqlite3
from PySide6.QtWidgets import QFileDialog, QMessageBox
from PySide6.QtCore import QDate
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from datetime import datetime
from Banco_Dados import CURSOS, dicionario_disciplinas, dicionario_de_cores


class GerenciamentoAtividades:
    def __init__(self):
        self.atividades = {}
        self.combo_curso = None
        self.entry_ementa = None
        self.entry_semestre = None
        self.entry_disciplina = None
        self.entry_codigo = None
        self.combo_tipo = None
        self.combo_sequencia = None
        self.calendar = None
        self.textbox = None
        self.conexao = sqlite3.connect('atividades.db')
        self.criar_tabela()
            
    def criar_tabela(self):
        cursor = self.conexao.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS atividades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT,
                tipo TEXT,
                sequencia TEXT,
                nome TEXT,
                turma TEXT
            )
        ''')
        self.conexao.commit()

    def adicionar_atividade(self, atividade):
        chave_unica = (atividade['data'], atividade['tipo'], atividade['sequencia'], atividade['nome'], atividade['turma'])
        self.atividades[chave_unica] = atividade
        cursor = self.conexao.cursor()
        cursor.execute('''
            INSERT INTO atividades (data, tipo, sequencia, nome, turma)
            VALUES (?, ?, ?, ?, ?)
        ''', (atividade['data'], atividade['tipo'], atividade['sequencia'], atividade['nome'], atividade['turma']))
        self.conexao.commit()

    def remover_atividade(self, atividade):
        chave_unica = (atividade['data'], atividade['tipo'], atividade['sequencia'], atividade['nome'], atividade['turma'])
        if chave_unica in self.atividades:
            del self.atividades[chave_unica]
            cursor = self.conexao.cursor()
            cursor.execute('''
                DELETE FROM atividades 
                WHERE data = ? AND tipo = ? AND sequencia = ? AND nome = ? AND turma = ?
            ''', chave_unica)
            self.conexao.commit()

    def listar_atividades(self):
        cursor = self.conexao.cursor()
        cursor.execute('SELECT data, tipo, sequencia, nome, turma FROM atividades')
        atividades_db = cursor.fetchall()
        self.atividades = {(a[0], a[1], a[2], a[3], a[4]): {'data': a[0], 'tipo': a[1], 'sequencia': a[2], 'nome': a[3], 'turma': a[4]} for a in atividades_db}
        return list(self.atividades.values())

    def buscar_atividade(self, atividade):
        chave_unica = (atividade['data'], atividade['tipo'], atividade['sequencia'], atividade['nome'], atividade['turma'])
        return self.atividades.get(chave_unica, None)

    def atualizar_atividade(self, atividade, novos_dados):
        chave_unica = (atividade['data'], atividade['tipo'], atividade['sequencia'], atividade['nome'], atividade['turma'])
        if chave_unica in self.atividades:
            self.atividades[chave_unica].update(novos_dados)
            cursor = self.conexao.cursor()
            cursor.execute('''
                UPDATE atividades
                SET data = ?, tipo = ?, sequencia = ?, turma = ?
                WHERE data = ? AND tipo = ? AND sequencia = ? AND nome = ? AND turma = ?
            ''', (novos_dados['data'], novos_dados['tipo'], novos_dados['sequencia'], novos_dados['turma'], atividade['data'], atividade['tipo'], atividade['sequencia'], atividade['nome'], atividade['turma']))
            self.conexao.commit()
            return True
        return False

    def submiter(self):
        data = self.calendar.selectedDate().toString('dd/MM/yyyy')
        tipo = self.combo_tipo.currentText()
        sequencia = self.combo_sequencia.currentText()
        nome = self.entry_disciplina.currentText()
        turma = self.entry_codigo.currentText()

        if tipo and sequencia and nome and turma:
            atividade = {
                'data': data,
                'tipo': tipo,
                'sequencia': sequencia,
                'nome': nome,
                'turma': turma
            }
            self.adicionar_atividade(atividade)
            self.update_textbox()
        else:
            QMessageBox.warning(None, "Erro", "Por favor, preencha todas as informações antes de adicionar a atividade.")

    def limpar_entradas(self):
        self.combo_curso.setCurrentIndex(0)
        self.entry_ementa.clear()
        self.entry_semestre.clear()
        self.entry_disciplina.clear()
        self.entry_codigo.setCurrentIndex(0)
        self.combo_tipo.setCurrentIndex(0)
        self.combo_sequencia.setCurrentIndex(0)
        self.calendar.setSelectedDate(QDate.currentDate())
        self.textbox.clear()
        cursor = self.conexao.cursor()
        cursor.execute('DELETE FROM atividades')
        self.conexao.commit()
        
    def limpar_ultima_entrada(self):
        cursor = self.conexao.cursor()
        cursor.execute('SELECT id FROM atividades ORDER BY id DESC LIMIT 1')
        resultado = cursor.fetchone()

        if resultado:
            ultima_id = resultado[0]
            cursor.execute('DELETE FROM atividades WHERE id = ?', (ultima_id,))
            self.conexao.commit()
            self.listar_atividades()
            self.update_textbox()
            QMessageBox.information(None, "Sucesso", "Última atividade removida com sucesso!")
            
        else:
            QMessageBox.warning(None, "Erro", "Nenhuma atividade para remover.")
        
    def exportar_para_pdf(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(None, "Salvar PDF", "", "PDF Files (*.pdf)")

        if not file_path:
            return

        if not file_path.endswith(".pdf"):
            file_path += ".pdf"

        doc = SimpleDocTemplate(
            file_path,
            pagesize=letter,
            rightMargin=0.5*cm,
            leftMargin=1*cm,
            topMargin=1*cm,
            bottomMargin=0.5*cm
        )
        styles = getSampleStyleSheet()
        styles['Normal'].fontSize = 10
        elements = []

        atividades = self.listar_atividades()
        atividades.sort(key=lambda x: datetime.strptime(x['data'], '%d/%m/%Y'))

        if not atividades:
            elements.append(Paragraph("", styles['Normal']))
            
        else:
            for atividade in atividades:
                if not (atividade['tipo'] and atividade['sequencia'] and atividade['nome'] and atividade['turma']):
                    continue

                nome_disciplina = atividade['nome']
                cor = None
                for coloracao, disciplinas in dicionario_disciplinas.items():
                    if nome_disciplina in disciplinas:
                        cor = dicionario_de_cores[coloracao]
                        break

                if cor:
                    nome_disciplina_formatado = f"<span color='{cor}'>{nome_disciplina}</span>"
                    underline_style = f"color='{cor}'"
                else:
                    nome_disciplina_formatado = nome_disciplina
                    underline_style = ""

                data_formatada = f"<b>{atividade['data']}</b>" if atividade['data'] else ""
                linha = f"<u {underline_style}>{data_formatada}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{atividade['tipo']} – {atividade['sequencia']}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{nome_disciplina_formatado}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{atividade['turma']}</u>"

                p = Paragraph(linha, styles['Normal'])
                elements.append(p)
                elements.append(Spacer(1, 24))

        doc.build(elements)
        QMessageBox.information(None, "Sucesso", "Atividades exportadas com sucesso para PDF!")

    def update_textbox(self):
        atividades = self.listar_atividades()
        atividades.sort(key=lambda x: datetime.strptime(x['data'], '%d/%m/%Y'))
        
        linhas_formatadas = []

        for atividade in atividades:
            if not (atividade['tipo'] and atividade['sequencia'] and atividade['nome'] and atividade['turma']):
                continue
                
            nome_disciplina = atividade['nome']
            cor = None
            for coloracao, disciplinas in dicionario_disciplinas.items():
                if nome_disciplina in disciplinas:
                    cor = dicionario_de_cores[coloracao]
                    break

            if cor:
                nome_disciplina_formatado = f"<span style='color: {cor};'>{nome_disciplina}</span>"
                underline_style = f"style='text-decoration-color: {cor};'"
            else:
                nome_disciplina_formatado = nome_disciplina
                underline_style = ""

            data_formatada = f"<b>{atividade['data']}</b>" if atividade['data'] else ""
            linha = f"<u {underline_style}>{data_formatada}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{atividade['tipo']} – {atividade['sequencia']}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{nome_disciplina_formatado}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{atividade['turma']}</u>"
            linha = linha.strip()
            linhas_formatadas.append(linha)

        texto_formatado = "<br><br>".join(linhas_formatadas)
        self.textbox.setHtml(texto_formatado)

    def update_ementa(self):
        selected_curso = self.combo_curso.currentText()
        ementas = CURSOS.get(selected_curso, {}).keys()
        self.entry_ementa.clear()
        self.entry_ementa.addItems([""] + list(ementas))

    def update_semestre(self):
        selected_curso = self.combo_curso.currentText()
        selected_ementa = self.entry_ementa.currentText()
        semestres = CURSOS.get(selected_curso, {}).get(selected_ementa, {}).keys()
        self.entry_semestre.clear()
        self.entry_semestre.addItems([""] + list(semestres))

    def update_disciplinas(self):
        selected_curso = self.combo_curso.currentText()
        selected_ementa = self.entry_ementa.currentText()
        selected_semestre = self.entry_semestre.currentText()
        disciplinas = CURSOS.get(selected_curso, {}).get(selected_ementa, {}).get(selected_semestre, [])
        self.entry_disciplina.clear()
        self.entry_disciplina.addItems([""] + disciplinas)

    def carregar_dados(self):
        self.listar_atividades()
        self.update_textbox()
