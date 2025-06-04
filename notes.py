import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QStatusBar,
                             QAction, QFileDialog, QMessageBox, QMenu, QFontDialog)
from PyQt5.QtGui import QIcon, QTextCursor, QTextListFormat, QFont
from PyQt5.QtCore import Qt

class SimpleNotes(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_file_path = None
        self.initUI()

    def initUI(self):
        self.text_area = QTextEdit()
        self.setCentralWidget(self.text_area)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Готово")

        self.create_menus()

        self.setGeometry(300, 300, 700, 500)
        self.update_window_title()
        self.show()

        self.text_area.document().modificationChanged.connect(self.set_window_modified_indicator)

    def update_window_title(self):
        title = "Простые Заметки"
        if self.current_file_path:
            import os
            file_name = os.path.basename(self.current_file_path)
            title = f"{file_name} - {title}"
        if self.isWindowModified():
            title += "*"
        self.setWindowTitle(title)

    def set_window_modified_indicator(self, modified):
        self.setWindowModified(modified)
        self.update_window_title()


    def create_menus(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu('&Файл')

        open_action = QAction(QIcon.fromTheme("document-open"), '&Открыть...', self)
        open_action.setShortcut("Ctrl+O")
        open_action.setStatusTip('Открыть существующий файл')
        open_action.triggered.connect(self.open_file_dialog)
        file_menu.addAction(open_action)

        save_action = QAction(QIcon.fromTheme("document-save"), '&Сохранить', self)
        save_action.setShortcut("Ctrl+S")
        save_action.setStatusTip('Сохранить текущий файл')
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        save_as_action = QAction(QIcon.fromTheme("document-save-as"), 'Сохранить &как...', self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.setStatusTip('Сохранить файл под новым именем')
        save_as_action.triggered.connect(self.save_file_as_dialog)
        file_menu.addAction(save_as_action)

        file_menu.addSeparator()

        exit_action = QAction(QIcon.fromTheme("application-exit"), '&Выход', self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip('Выйти из приложения')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        edit_menu = menubar.addMenu('&Правка')

        bold_action = QAction('&Жирный', self)
        bold_action.setShortcut("Ctrl+B")
        bold_action.setStatusTip('Сделать текст жирным')
        bold_action.triggered.connect(self.set_bold)
        edit_menu.addAction(bold_action)

        italic_action = QAction('&Курсив', self)
        italic_action.setShortcut("Ctrl+I")
        italic_action.setStatusTip('Сделать текст курсивом')
        italic_action.triggered.connect(self.set_italic)
        edit_menu.addAction(italic_action)

        increase_font_action = QAction('Увеличить &размер шрифта', self)
        increase_font_action.setShortcut("Ctrl++")
        increase_font_action.setStatusTip('Увеличить размер шрифта')
        increase_font_action.triggered.connect(self.increase_font_size)
        edit_menu.addAction(increase_font_action)

        decrease_font_action = QAction('Уменьшить р&азмер шрифта', self)
        decrease_font_action.setShortcut("Ctrl+-")
        decrease_font_action.setStatusTip('Уменьшить размер шрифта')
        decrease_font_action.triggered.connect(self.decrease_font_size)
        edit_menu.addAction(decrease_font_action)

        font_action = QAction('&Шрифт...', self)
        font_action.setStatusTip('Выбрать шрифт и его параметры')
        font_action.triggered.connect(self.choose_font)
        edit_menu.addAction(font_action)

        edit_menu.addSeparator()

        add_list_action = QAction('&Добавить маркированный список', self)
        add_list_action.setShortcut(Qt.CTRL + Qt.Key_L)
        add_list_action.setStatusTip('Вставить маркированный список или преобразовать выделение')
        add_list_action.triggered.connect(self.add_bullet_list)
        edit_menu.addAction(add_list_action)

    def set_bold(self):
        cursor = self.text_area.textCursor()
        if not cursor.hasSelection():
            char_format = cursor.charFormat()
            char_format.setFontWeight(QFont.Bold if char_format.fontWeight() == QFont.Normal else QFont.Normal)
            cursor.setCharFormat(char_format)
        else:
            format = cursor.charFormat()
            format.setFontWeight(QFont.Bold if format.fontWeight() == QFont.Normal else QFont.Normal)
            cursor.mergeCharFormat(format)
        self.status_bar.showMessage("Жирный стиль текста изменен")

    def set_italic(self):
        cursor = self.text_area.textCursor()
        if not cursor.hasSelection():
            char_format = cursor.charFormat()
            char_format.setFontItalic(not char_format.fontItalic())
            cursor.setCharFormat(char_format)
        else:
            format = cursor.charFormat()
            format.setFontItalic(not format.fontItalic())
            cursor.mergeCharFormat(format)
        self.status_bar.showMessage("Курсивный стиль текста изменен")

    def increase_font_size(self):
        cursor = self.text_area.textCursor()
        if not cursor.hasSelection():
            char_format = cursor.charFormat()
            new_size = char_format.fontPointSize() + 2
            if new_size > 0:
                char_format.setFontPointSize(new_size)
                cursor.setCharFormat(char_format)
        else:
            format = cursor.charFormat()
            new_size = format.fontPointSize() + 2
            if new_size > 0:
                format.setFontPointSize(new_size)
                cursor.mergeCharFormat(format)
        self.status_bar.showMessage(f"Размер шрифта увеличен до {new_size}pt")

    def decrease_font_size(self):
        cursor = self.text_area.textCursor()
        if not cursor.hasSelection():
            char_format = cursor.charFormat()
            new_size = char_format.fontPointSize() - 2
            if new_size > 0:
                char_format.setFontPointSize(new_size)
                cursor.setCharFormat(char_format)
        else:
            format = cursor.charFormat()
            new_size = format.fontPointSize() - 2
            if new_size > 0:
                format.setFontPointSize(new_size)
                cursor.mergeCharFormat(format)
        self.status_bar.showMessage(f"Размер шрифта уменьшен до {new_size}pt")

    def choose_font(self):
        current_font = self.text_area.currentFont()
        font, ok = QFontDialog.getFont(current_font, self)
        if ok:
            cursor = self.text_area.textCursor()
            if not cursor.hasSelection():
                self.text_area.setCurrentFont(font)
            else:
                format = cursor.charFormat()
                format.setFont(font)
                cursor.mergeCharFormat(format)
            self.status_bar.showMessage(f"Шрифт изменен на {font.family()}, {font.pointSize()}pt")


    def add_bullet_list(self):
        cursor = self.text_area.textCursor()
        list_format = QTextListFormat()
        list_format.setStyle(QTextListFormat.ListDisc)

        cursor.createList(list_format)
        self.status_bar.showMessage("Маркированный список добавлен/изменен")

    def open_file_dialog(self):
        if self.maybe_save():
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "",
                                                       "Текстовые файлы (*.txt);;Все файлы (*)", options=options)
            if file_path:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        self.text_area.setPlainText(f.read())
                    self.current_file_path = file_path
                    self.status_bar.showMessage(f"Файл открыт: {file_path}")
                    self.text_area.document().setModified(False)
                    self.update_window_title()
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось открыть файл:\n{e}")
                    self.status_bar.showMessage("Ошибка открытия файла")

    def save_file(self):
        if self.current_file_path:
            self._save_to_path(self.current_file_path)
        else:
            self.save_file_as_dialog()

    def save_file_as_dialog(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить файл как...", "",
                                                   "Текстовые файлы (*.txt);;Все файлы (*)", options=options)
        if file_path:
            if not file_path.endswith(('.txt')) and '.' not in file_path.split('/')[-1]:
                 file_path += '.txt'
            self._save_to_path(file_path)


    def _save_to_path(self, file_path):
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(self.text_area.toPlainText())
            self.current_file_path = file_path
            self.status_bar.showMessage(f"Файл сохранен: {file_path}")
            self.text_area.document().setModified(False)
            self.update_window_title()
            return True
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл:\n{e}")
            self.status_bar.showMessage("Ошибка сохранения файла")
            return False

    def maybe_save(self):
        if not self.text_area.document().isModified():
            return True

        ret = QMessageBox.warning(self, "Простые Заметки",
                                   "Документ был изменен.\n"
                                   "Хотите сохранить изменения?",
                                   QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)

        if ret == QMessageBox.Save:
            return self.save_file()
        elif ret == QMessageBox.Cancel:
            return False
        return True


    def closeEvent(self, event):
        if self.maybe_save():
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    notes_app = SimpleNotes()
    sys.exit(app.exec_())
зн