"""CustomTkinter を使用したモダンなGUIサンプル"""

import customtkinter as ctk
from typing import Optional

class ModernTetrisLauncher:
    """テトリスゲームランチャーのGUI"""
    
    def __init__(self):
        self.window: Optional[ctk.CTk] = None
        self.setup_ui()
    
    def setup_ui(self):
        """UI初期化"""
        # ダークモードとテーマ設定
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.window = ctk.CTk()
        self.window.geometry("400x300")
        self.window.title("テトリスゲームランチャー")
        
        # メインフレーム
        main_frame = ctk.CTkFrame(self.window)
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # タイトル
        title_label = ctk.CTkLabel(
            main_frame, 
            text="テトリスゲーム",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)
        
        # ゲーム開始ボタン
        start_button = ctk.CTkButton(
            main_frame,
            text="ゲーム開始",
            font=ctk.CTkFont(size=16),
            height=40,
            command=self.start_game
        )
        start_button.pack(pady=10)
        
        # 設定ボタン
        settings_button = ctk.CTkButton(
            main_frame,
            text="設定",
            font=ctk.CTkFont(size=16),
            height=40,
            command=self.open_settings
        )
        settings_button.pack(pady=10)
        
        # 終了ボタン
        quit_button = ctk.CTkButton(
            main_frame,
            text="終了",
            font=ctk.CTkFont(size=16),
            height=40,
            fg_color="red",
            hover_color="darkred",
            command=self.window.quit
        )
        quit_button.pack(pady=10)
    
    def start_game(self):
        """ゲーム開始"""
        print("ゲームを開始します...")
        # ここでメインのテトリスゲームを呼び出す
        import subprocess
        try:
            subprocess.run(["python", "src/tetris_game/main.py"])
        except Exception as e:
            print(f"ゲーム開始エラー: {e}")
    
    def open_settings(self):
        """設定画面を開く"""
        settings_window = SettingsWindow(self.window)
    
    def run(self):
        """アプリケーション実行"""
        if self.window:
            self.window.mainloop()

class SettingsWindow:
    """設定画面"""
    
    def __init__(self, parent):
        self.setup_ui(parent)
    
    def setup_ui(self, parent):
        """設定UI初期化"""
        self.window = ctk.CTkToplevel(parent)
        self.window.geometry("300x250")
        self.window.title("設定")
        
        # 設定フレーム
        settings_frame = ctk.CTkFrame(self.window)
        settings_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # 音量設定
        volume_label = ctk.CTkLabel(settings_frame, text="音量")
        volume_label.pack(pady=5)
        
        volume_slider = ctk.CTkSlider(settings_frame, from_=0, to=100)
        volume_slider.set(50)
        volume_slider.pack(pady=5)
        
        # 難易度設定
        difficulty_label = ctk.CTkLabel(settings_frame, text="難易度")
        difficulty_label.pack(pady=5)
        
        difficulty_menu = ctk.CTkOptionMenu(
            settings_frame, 
            values=["簡単", "普通", "難しい"]
        )
        difficulty_menu.pack(pady=5)
        
        # 保存ボタン
        save_button = ctk.CTkButton(
            settings_frame,
            text="保存",
            command=self.save_settings
        )
        save_button.pack(pady=20)
    
    def save_settings(self):
        """設定を保存"""
        print("設定を保存しました")
        self.window.destroy()

if __name__ == "__main__":
    app = ModernTetrisLauncher()
    app.run()