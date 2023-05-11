from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QGridLayout, QWidget, QPushButton, QTextEdit

from frontengine.ui.color.global_color import error_color, output_color
from frontengine.ui.setting.gif.gif_setting_ui import GIFSettingUI
from frontengine.ui.setting.image.image_setting_ui import ImageSettingUI
from frontengine.ui.setting.sound_player.sound_player_setting_ui import SoundPlayerSettingUI
from frontengine.ui.setting.text.text_setting_ui import TextSettingUI
from frontengine.ui.setting.video.video_setting_ui import VideoSettingUI
from frontengine.ui.setting.web.web_setting_ui import WEBSettingUI
from frontengine.utils.redirect_manager.redirect_manager_class import redirect_manager_instance


class ControlCenterUI(QWidget):

    def __init__(
            self,
            video_setting_ui: VideoSettingUI,
            image_setting_ui: ImageSettingUI,
            web_setting_ui: WEBSettingUI,
            gif_setting_ui: GIFSettingUI,
            sound_player_setting_ui: SoundPlayerSettingUI,
            text_setting_ui: TextSettingUI
    ):
        super().__init__()
        # Layout
        self.grid_layout = QGridLayout()
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        # UI instance
        self.video_setting_ui = video_setting_ui
        self.image_setting_ui = image_setting_ui
        self.web_setting_ui = web_setting_ui
        self.gif_setting_ui = gif_setting_ui
        self.sound_player_setting_ui = sound_player_setting_ui
        self.text_setting_ui = text_setting_ui
        # Close button
        self.clear_video_button = QPushButton("Close all video")
        self.clear_video_button.clicked.connect(self.clear_video)
        self.clear_image_button = QPushButton("Close all image")
        self.clear_image_button.clicked.connect(self.clear_image)
        self.clear_gif_button = QPushButton("Close all gif")
        self.clear_gif_button.clicked.connect(self.clear_gif)
        self.clear_web_button = QPushButton("Close all web")
        self.clear_web_button.clicked.connect(self.clear_web)
        self.clear_sound_button = QPushButton("Close all sound")
        self.clear_sound_button.clicked.connect(self.clear_sound)
        self.clear_text_button = QPushButton("Close all text")
        self.clear_text_button.clicked.connect(self.clear_text)
        self.clear_all_button = QPushButton("Close all")
        self.clear_all_button.clicked.connect(self.clear_all)
        # Log panel
        self.log_panel = QTextEdit()
        self.log_panel.setLineWrapMode(self.log_panel.LineWrapMode.NoWrap)
        self.log_panel.setReadOnly(True)
        # Add to layout
        self.grid_layout.addWidget(self.clear_video_button, 0, 0)
        self.grid_layout.addWidget(self.clear_image_button, 1, 0)
        self.grid_layout.addWidget(self.clear_gif_button, 2, 0)
        self.grid_layout.addWidget(self.clear_web_button, 3, 0)
        self.grid_layout.addWidget(self.clear_sound_button, 4, 0)
        self.grid_layout.addWidget(self.clear_text_button, 5, 0)
        self.grid_layout.addWidget(self.clear_all_button, 6, 0)
        self.grid_layout.addWidget(self.log_panel, 0, 1, 7, 10)
        self.setLayout(self.grid_layout)
        # Redirect
        self.redirect_timer = QTimer(self)
        self.redirect_timer.setInterval(1)
        self.redirect_timer.timeout.connect(self.redirect)
        self.redirect_timer.start()
        redirect_manager_instance.set_redirect(self, True)

    def clear_video(self):
        self.video_setting_ui.video_widget_list.clear()

    def clear_image(self):
        self.image_setting_ui.image_widget_list.clear()

    def clear_gif(self):
        self.gif_setting_ui.gif_widget_list.clear()

    def clear_web(self):
        self.web_setting_ui.web_widget_list.clear()

    def clear_sound(self):
        self.sound_player_setting_ui.sound_widget_list.clear()

    def clear_text(self):
        self.text_setting_ui.text_widget_list.clear()

    def clear_all(self):
        self.video_setting_ui.video_widget_list.clear()
        self.image_setting_ui.image_widget_list.clear()
        self.web_setting_ui.web_widget_list.clear()
        self.gif_setting_ui.gif_widget_list.clear()
        self.sound_player_setting_ui.sound_widget_list.clear()
        self.text_setting_ui.text_widget_list.clear()

    def redirect(self):
        if not redirect_manager_instance.std_out_queue.empty():
            output_message = redirect_manager_instance.std_out_queue.get_nowait()
            output_message = str(output_message).strip()
            if output_message:
                self.log_panel.append(output_message)
        self.log_panel.setTextColor(error_color)
        if not redirect_manager_instance.std_err_queue.empty():
            error_message = redirect_manager_instance.std_err_queue.get_nowait()
            error_message = str(error_message).strip()
            if error_message:
                self.log_panel.append(error_message)
        self.log_panel.setTextColor(output_color)
