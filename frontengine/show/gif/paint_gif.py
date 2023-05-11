import os
from pathlib import Path

from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QMovie, QPainter, QIcon
from PySide6.QtWidgets import QWidget, QLabel, QMessageBox

from frontengine.utils.multi_language.language_wrapper import language_wrapper


class GifWidget(QWidget):

    def __init__(self, gif_image_path: str,
                 speed: int = 100, opacity: float = 0.2
                 ):
        super().__init__()
        self.setWindowFlag(
            Qt.WindowType.WindowTransparentForInput |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.gif_label = QLabel()
        self.gif_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.opacity = opacity
        self.gif_path = Path(gif_image_path)
        if self.gif_path.exists() and self.gif_path.is_file():
            print(f"Origin file {str(self.gif_path)}")
            self.movie = QMovie(str(self.gif_path))
            self.movie.setSpeed(speed)
            self.movie.frameChanged.connect(self.repaint)
            self.gif_label.setMovie(self.movie)
            self.movie.start()
        else:
            message_box = QMessageBox(self)
            message_box.setText(
                language_wrapper.language_word_dict.get("paint_gif_message_box_text")
            )
            message_box.show()
        # Set Icon
        self.icon_path = Path(os.getcwd() + "/je_driver_icon.ico")
        if self.icon_path.exists() and self.icon_path.is_file():
            self.setWindowIcon(QIcon(str(self.icon_path)))

    def paintEvent(self, event) -> None:
        current_gif_frame = self.movie.currentPixmap()
        painter = QPainter(self)
        painter.setOpacity(self.opacity)
        painter.drawPixmap(
            QRect(
                self.x(), self.y(), self.width(), self.height()
            ),
            current_gif_frame
        )
        painter.restore()
