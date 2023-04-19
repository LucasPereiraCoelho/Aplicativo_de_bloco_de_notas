from PySide6.QtWidgets import *
from datetime import datetime
from Notepad.model.notepad import Notepad
from Notepad.controller.notepad_dao import DataBase


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(500, 700)

        self.setWindowTitle('Bloco de Notas')

        self.lbl_id = QLabel('ID')
        self.txt_id = QLineEdit()
        self.txt_id.setMaximumSize(40, 100)
        self.lbl_note_name = QLabel('Título')
        self.txt_note_name = QLineEdit()
        self.lbl_note_date = QLabel('Data')
        self.txt_note_date = QLineEdit()
        self.lbl_priority = QLabel('Prioridade')
        #Criado melhoria adicionando a opção de prioridade das notas.
        self.cb_priority = QComboBox()
        self.cb_priority.addItems(['Não informado', 'Prioridade', 'Não prioridade'])
        self.lbl_note_text = QLabel('Texto')
        self.txt_note_text = QTextEdit()
        self.btn_save = QPushButton('Salvar')
        self.btn_remove = QPushButton('Remover')
        self.note_table = QTableWidget()
        self.note_table.setColumnCount(5)
        self.note_table.setHorizontalHeaderLabels(['ID', 'Nome', 'Data', 'Prioridade', 'Texto'])
        self.note_table.setSelectionMode(QAbstractItemView.NoSelection)
        self.note_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_id)
        layout.addWidget(self.txt_id)
        layout.addWidget(self.lbl_note_name)
        layout.addWidget(self.txt_note_name)
        layout.addWidget(self.lbl_priority)
        layout.addWidget(self.cb_priority)
        layout.addWidget(self.lbl_note_text)
        layout.addWidget(self.txt_note_text)
        layout.addWidget(self.note_table)
        layout.addWidget(self.btn_save)
        layout.addWidget(self.btn_remove)

        self.container = QWidget()
        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setCentralWidget(self.container)
        self.container.setLayout(layout)

        self.btn_remove.setVisible(False)
        self.txt_id.setReadOnly(True)
        self.btn_save.clicked.connect(self.save_note)
        self.btn_remove.clicked.connect(self.delete_note)
        self.note_table.cellDoubleClicked.connect(self.load_data)
        self.fill_note_table()

    def save_note(self):
        db = DataBase()

        new_note = Notepad(
            note_name=self.txt_note_name.text(),
            note_date=datetime.today().date(),
            note_priority=self.cb_priority.currentText(),
            note_text=self.txt_note_text.toPlainText()

        )
        if self.btn_save.text() == 'Salvar':
            retorno = db.create_note(new_note)

            if retorno == 'Ok':
                msg = QMessageBox()
                msg.setWindowTitle('Cadastro realizado')
                msg.setText('Cadastro realizado com sucesso')
                msg.exec()
                self.clear()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle('Erro ao cadastrar')
                msg.setText(f'Erro ao cadastrar a nota')
                msg.exec()
        elif self.btn_save.text() == 'Atualizar':
            retorno = db.update_note(self.txt_id.text(), new_note)
            if retorno == 'Ok':
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle('Nota atualizada')
                msg.setText('Nota atualizada com sucesso')
                msg.exec()
                self.clear()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle('Erro ao atualizar')
                msg.setText('Erro ao atualizar a nota')
                msg.exec()

        self.fill_note_table()
        self.txt_id.setReadOnly(True)

    def fill_note_table(self):
        self.note_table.setRowCount(0)
        db = DataBase()
        note_list = db.read_notes()
        self.note_table.setRowCount(len(note_list))

        for line, note in enumerate(note_list):
            for column, value in enumerate(note):
                self.note_table.setItem(line, column, QTableWidgetItem(str(value)))

    def load_data(self, row):
        self.txt_id.setText(self.note_table.item(row, 0).text())
        self.txt_note_name.setText(self.note_table.item(row, 1).text())
        self.txt_note_date.setText(self.note_table.item(row, 2).text())
        priority_map = {'Não informado': 0, 'Prioridade': 1, 'Não prioridade': 2}
        self.cb_priority.setCurrentIndex(priority_map.get(self.note_table.item(row, 3).text(), 0))
        self.txt_note_text.setText(self.note_table.item(row, 4).text())
        self.btn_save.setText('Atualizar')
        self.btn_remove.setVisible(True)
        self.txt_id.setReadOnly(True)

    def delete_note(self):

        msg = QMessageBox()
        msg.setWindowTitle('Remover Nota')
        msg.setText('Essa nota será removido')
        msg.setInformativeText(f'Você deseja remover o bloco de notas de nome {self.txt_note_name.text()} ?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.button(QMessageBox.Yes).setText('Sim')
        msg.button(QMessageBox.No).setText('Não')
        answer = msg.exec()

        if answer == QMessageBox.Yes:
            db = DataBase()
            db_delete = db.delete_note(self.txt_id.text())

            if db_delete == 'Ok':
                nv_msg = QMessageBox()
                nv_msg.setWindowTitle('Remover nota')
                nv_msg.setText('Nota removida com sucesso')
                nv_msg.exec()
                self.clear()
            else:
                nv_msg = QMessageBox()
                nv_msg.setWindowTitle('Remover Nota')
                nv_msg.setText('Erro ao remover nota')
                nv_msg.exec()
        self.txt_id.setReadOnly(True)
        self.fill_note_table()

    def clear(self):
        for widget in self.container.children():
            if isinstance(widget, QLineEdit) or isinstance(widget, QTextEdit):
                widget.clear()
            elif isinstance(widget, QComboBox):
                widget.setCurrentIndex(0)
        self.btn_remove.setVisible(False)
        self.btn_save.setText('Salvar')

        self.txt_id.setReadOnly(True)
        self.fill_note_table()
