"""PyQt6 を使用した高機能GUIサンプル"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QSlider, QComboBox, QGroupBox, QTabWidget
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPalette, QColor

class PyQtTetrisLauncher(QMainWindow):
    """PyQt6を使用したテトリスランチャー"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_timer()
    
    def init_ui(self):
        """UI初期化"""
        self.setWindowTitle("テトリスゲームランチャー (PyQt6)")
        self.setGeometry(100, 100, 500, 400)
        
        # ダークテーマ設定
        self.set_dark_theme()
        
        # 中央ウィジェット
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # メインレイアウト
        main_layout = QVBoxLayout(central_widget)
        
        # タイトル
        title_label = QLabel("テトリスゲーム")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        main_layout.addWidget(title_label)
        
        # タブウィジェット
        tab_widget = QTabWidget()
        main_layout.addWidget(tab_widget)
        
        # ゲームタブ
        game_tab = self.create_game_tab()
        tab_widget.addTab(game_tab, "ゲーム")
        
        # 設定タブ
        settings_tab = self.create_settings_tab()
        tab_widget.addTab(settings_tab, "設定")
        
        # 統計タブ
        stats_tab = self.create_stats_tab()
        tab_widget.addTab(stats_tab, "統計")
    
    def create_game_tab(self) -> QWidget:
        """ゲームタブ作成"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # ゲームコントロール
        game_group = QGroupBox("ゲームコントロール")
        game_layout = QVBoxLayout(game_group)
        
        start_button = QPushButton("ゲーム開始")
        start_button.setMinimumHeight(50)
        start_button.clicked.connect(self.start_game)
        game_layout.addWidget(start_button)
        
        pause_button = QPushButton("一時停止")
        pause_button.setMinimumHeight(40)
        game_layout.addWidget(pause_button)
        
        layout.addWidget(game_group)
        
        # 終了ボタン
        quit_button = QPushButton("終了")
        quit_button.setMinimumHeight(40)
        quit_button.clicked.connect(self.close)
        layout.addWidget(quit_button)
        
        return widget
    
    def create_settings_tab(self) -> QWidget:
        """設定タブ作成"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 音声設定
        audio_group = QGroupBox("音声設定")
        audio_layout = QVBoxLayout(audio_group)
        
        volume_label = QLabel("音量: 50%")
        audio_layout.addWidget(volume_label)
        
        volume_slider = QSlider(Qt.Orientation.Horizontal)
        volume_slider.setRange(0, 100)
        volume_slider.setValue(50)
        volume_slider.valueChanged.connect(
            lambda v: volume_label.setText(f"音量: {v}%")
        )
        audio_layout.addWidget(volume_slider)
        
        layout.addWidget(audio_group)
        
        # ゲーム設定
        game_group = QGroupBox("ゲーム設定")
        game_layout = QVBoxLayout(game_group)
        
        difficulty_label = QLabel("難易度:")
        game_layout.addWidget(difficulty_label)
        
        difficulty_combo = QComboBox()
        difficulty_combo.addItems(["簡単", "普通", "難しい", "エキスパート"])
        difficulty_combo.setCurrentText("普通")
        game_layout.addWidget(difficulty_combo)
        
        layout.addWidget(game_group)
        
        return widget
    
    def create_stats_tab(self) -> QWidget:
        """統計タブ作成"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        stats_group = QGroupBox("ゲーム統計")
        stats_layout = QVBoxLayout(stats_group)
        
        # 統計情報
        stats_data = [
            ("総プレイ回数:", "0 回"),
            ("最高スコア:", "0 点"),
            ("総プレイ時間:", "0 時間"),
            ("ライン消去数:", "0 ライン")
        ]
        
        for label, value in stats_data:
            row_layout = QHBoxLayout()
            row_layout.addWidget(QLabel(label))
            row_layout.addWidget(QLabel(value))
            row_layout.addStretch()
            stats_layout.addLayout(row_layout)
        
        layout.addWidget(stats_group)
        
        # リセットボタン
        reset_button = QPushButton("統計をリセット")
        layout.addWidget(reset_button)
        
        return widget
    
    def set_dark_theme(self):
        """ダークテーマ設定"""
        palette = QPalette()
        
        # ダークカラー設定
        palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))
        
        self.setPalette(palette)
    
    def setup_timer(self):
        """タイマー設定"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # 1秒間隔
    
    def update_time(self):
        """時間更新（統計用）"""
        pass
    
    def start_game(self):
        """ゲーム開始"""
        print("PyQt6からゲームを開始します...")
        import subprocess
        try:
            subprocess.run(["python", "src/tetris_game/main.py"])
        except Exception as e:
            print(f"ゲーム開始エラー: {e}")

def main():
    app = QApplication(sys.argv)
    launcher = PyQtTetrisLauncher()
    launcher.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()