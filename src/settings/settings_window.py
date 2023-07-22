from settings.settings_ui import Ui_Form
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget
from settings.settings import current_settings


class SettingsWindow(QWidget, Ui_Form):
    def __init__(self, parent):
        super().__init__()
        self.setVisible(True)
        self.p = parent
        self.setupUi(self)

        self._load_data()

        self.apply_button.clicked.connect(self.apply_event)
        self.save_button.clicked.connect(self.save_event)
        self.exit_button.clicked.connect(self.close)

    
    def _load_data(self):
        self.app_name_edit.setText(str(current_settings.get_program_name()))

        self.frame_x_edit.setText(str(current_settings.get_frame_pos()[0]))
        self.frame_y_edit.setText(str(current_settings.get_frame_pos()[1]))

        self.image_width_edit.setText(str(current_settings.get_image_width()))
        self.image_height_edit.setText(str(current_settings.get_image_height()))

        self.auto_height_checkbox.setChecked(current_settings.get_auto_height())

        self.opacity_slider.setValue(100 * current_settings.get_opacity())


    def apply_event(self):
        current_settings.set_opacity(float(self.opacity_slider.value()))

        try:
            current_settings.set_frame_pos(
                float(self.frame_x_edit.text()),
                float(self.frame_y_edit.text())
            )
        except Exception:
            print('Frame pos must be a number.')

        current_settings.set_program_name(self.app_name_edit.text())

        try:
            current_settings.set_image_width(float(self.image_width_edit.text()))
            current_settings.set_image_height(float(self.image_height_edit.text()))
        except Exception:
            print("Image info must be number.")

        current_settings.set_auto_height(self.auto_height_checkbox.isChecked())

        self.p.settings_updated()

    def save_event(self):
        current_settings.save_data()


    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        event.ignore()
        self.hide()
