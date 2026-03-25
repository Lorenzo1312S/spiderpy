import sys
import os
import random

try:
    from PyQt6.QtWidgets import QApplication, QLabel
    from PyQt6.QtCore import Qt, QTimer, QPoint
    from PyQt6.QtGui import QPixmap, QGuiApplication
except ImportError as e:
    raise RuntimeError("PyQt6 non installato. Esegui: python spider_runner.py setup") from e


class SpiderWindow(QLabel):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        def resource_path(relative_path: str) -> str:
            if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
                basedir = sys._MEIPASS
            else:
                basedir = os.path.dirname(os.path.abspath(__file__))
            return os.path.join(basedir, relative_path)

        self.frames = []
        assets_dir = resource_path("assets")
        for i in range(4):
            frame_path = os.path.join(assets_dir, f"spider_{i}.png")
            if os.path.exists(frame_path):
                self.frames.append(QPixmap(frame_path))

        # Ridimensiona i frame per mantenere un ragno "compatto" (veloce da disegnare)
        TARGET_SIZE = 113  # pixel (~3cm a 96dpi)
        self.frames = [
            f.scaled(
                TARGET_SIZE,
                TARGET_SIZE,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.FastTransformation,
            )
            for f in self.frames
        ]

        if not self.frames:
            raise RuntimeError("Nessun frame trovato in assets/spider_*.png")

        self.current_frame = 0
        self.setPixmap(self.frames[self.current_frame])

        screen = QGuiApplication.primaryScreen().availableGeometry()
        self.screen_rect = screen
        self.resize(self.frames[0].width(), self.frames[0].height())

        start_x = random.randint(0, max(0, screen.width() - self.width()))
        start_y = random.randint(0, max(0, screen.height() - self.height()))
        self.move(start_x, start_y)

        self.dx = random.choice([-3, -2, 2, 3])
        self.dy = random.choice([-3, -2, 2, 3])

        self.move_timer = QTimer()
        self.move_timer.timeout.connect(self.move_spider)
        self.move_timer.start(30)

        self.anim_timer = QTimer()
        self.anim_timer.timeout.connect(self.next_frame)
        self.anim_timer.start(120)

    def next_frame(self):
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.setPixmap(self.frames[self.current_frame])

    def move_spider(self):
        x = self.x() + self.dx
        y = self.y() + self.dy

        if x <= self.screen_rect.left() or x + self.width() >= self.screen_rect.right():
            self.dx = -self.dx
            x = max(self.screen_rect.left(), min(x, self.screen_rect.right() - self.width()))
        if y <= self.screen_rect.top() or y + self.height() >= self.screen_rect.bottom():
            self.dy = -self.dy
            y = max(self.screen_rect.top(), min(y, self.screen_rect.bottom() - self.height()))

        self.move(QPoint(x, y))


def main():
    app = QApplication(sys.argv)
    spider = SpiderWindow()
    spider.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()