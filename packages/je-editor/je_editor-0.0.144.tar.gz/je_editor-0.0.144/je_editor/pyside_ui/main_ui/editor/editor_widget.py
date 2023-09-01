import os
import pathlib

from PySide6 import QtGui
from PySide6.QtCore import Qt, QFileInfo, QDir
from PySide6.QtWidgets import QWidget, QGridLayout, QSplitter, QScrollArea, QFileSystemModel, QTreeView

from je_editor.pyside_ui.code.auto_save.auto_save_thread import SaveThread
from je_editor.pyside_ui.code.plaintext_code_edit.code_edit_plaintext import CodeEditor
from je_editor.pyside_ui.code.textedit_code_result.code_record import CodeRecord
from je_editor.pyside_ui.main_ui.save_user_setting.user_setting_file import user_setting_dict, \
    write_user_setting
from je_editor.utils.file.open.open_file import read_file


class EditorWidget(QWidget):

    def __init__(self):
        super().__init__()
        # Init variable
        self.auto_save_thread = None
        self.current_file = None
        self.tree_view_scroll_area = None
        self.project_treeview = None
        self.project_treeview_model = None
        # UI
        self.grid_layout = QGridLayout(self)
        self.setWindowTitle("JEditor")
        # Splitter
        self.edit_splitter = QSplitter()
        self.edit_splitter.setOrientation(Qt.Orientation.Vertical)
        self.edit_splitter.setChildrenCollapsible(False)
        # code edit and code result plaintext
        self.code_edit = CodeEditor()
        self.code_result = CodeRecord()
        self.code_edit_scroll_area = QScrollArea()
        self.code_edit_scroll_area.setWidgetResizable(True)
        self.code_edit_scroll_area.setViewportMargins(0, 0, 0, 0)
        self.code_edit_scroll_area.setWidget(self.code_edit)
        self.code_result_scroll_area = QScrollArea()
        self.code_result_scroll_area.setWidgetResizable(True)
        self.code_result_scroll_area.setViewportMargins(0, 0, 0, 0)
        self.code_result_scroll_area.setWidget(self.code_result)
        self.grid_layout.setRowStretch(0, 10)
        self.grid_layout.setColumnStretch(1, 10)
        self.edit_splitter.addWidget(self.code_edit_scroll_area)
        self.edit_splitter.addWidget(self.code_result_scroll_area)
        self.edit_splitter.setStretchFactor(0, 7)
        self.grid_layout.addWidget(self.edit_splitter, 0, 1)
        # current file
        self.current_file = None
        if self.current_file is not None and self.auto_save_thread is None:
            self.auto_save_thread = SaveThread(
                self.current_file,
                self.code_edit.toPlainText()
            )
            self.auto_save_thread.start()
        # Treeview
        self.set_project_treeview()

    def set_project_treeview(self) -> None:
        self.grid_layout.setColumnStretch(0, 4)
        self.project_treeview_model = QFileSystemModel()
        self.project_treeview_model.setRootPath(QDir.currentPath())
        self.project_treeview = QTreeView()
        self.project_treeview.setModel(self.project_treeview_model)
        self.project_treeview.setRootIndex(
            self.project_treeview_model.index(os.getcwd())
        )
        self.tree_view_scroll_area = QScrollArea()
        self.tree_view_scroll_area.setWidgetResizable(True)
        self.tree_view_scroll_area.setViewportMargins(0, 0, 0, 0)
        self.tree_view_scroll_area.setWidget(self.project_treeview)
        self.grid_layout.addWidget(self.tree_view_scroll_area, 0, 0, 0, 1)
        self.project_treeview.clicked.connect(
            self.treeview_click
        )

    def treeview_click(self) -> None:
        clicked_item: QFileSystemModel = self.project_treeview.selectedIndexes()[0]
        file_info: QFileInfo = self.project_treeview.model().fileInfo(clicked_item)
        path = pathlib.Path(file_info.absoluteFilePath())
        if path.is_file():
            file, file_content = read_file(str(path))
            self.code_edit.setPlainText(
                file_content
            )
            self.current_file = file
            if self.auto_save_thread is None:
                self.auto_save_thread = SaveThread(
                    self.current_file,
                    self.code_edit.toPlainText()
                )
                self.auto_save_thread.start()
            if self.auto_save_thread is not None:
                self.auto_save_thread.file = self.current_file

    def closeEvent(self, event: QtGui.QCloseEvent):
        super().closeEvent()
        user_setting_dict.update({"last_file": str(self.current_file)})
        write_user_setting()
