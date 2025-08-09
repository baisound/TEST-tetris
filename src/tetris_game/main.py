# -*- coding: utf-8 -*-
"""テトリスゲーム メインアプリケーション"""

import pygame
import sys
import os
from tetris_game.game_engine import GameEngine

# 初期化
pygame.init()

# ゲーム設定
GRID_WIDTH = 10
GRID_HEIGHT = 20
BLOCK_SIZE = 30
WINDOW_WIDTH = GRID_WIDTH * BLOCK_SIZE + 200
WINDOW_HEIGHT = GRID_HEIGHT * BLOCK_SIZE + 100

# 色定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
GRAY = (128, 128, 128)

SHAPE_COLORS = [BLACK, CYAN, YELLOW, PURPLE, GREEN, RED, BLUE, ORANGE]

class TetrisGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("テトリス")
        self.clock = pygame.time.Clock()
        self.tetris = GameEngine(GRID_WIDTH, GRID_HEIGHT)
        
        # Windows対応日本語フォント設定
        self.font = self.get_japanese_font(36)
        self.small_font = self.get_japanese_font(24)
    
    def get_japanese_font(self, size):
        """クロスプラットフォーム日本語フォントを取得"""
        # 1. バンドルされたフォントファイルを確認
        try:
            # PyInstallerでバンドルされたリソースパス
            if hasattr(sys, '_MEIPASS'):
                bundle_dir = sys._MEIPASS
            else:
                bundle_dir = os.path.dirname(os.path.abspath(__file__))
            
            # プロジェクトのassetsディレクトリも確認
            asset_paths = [
                os.path.join(bundle_dir, 'assets', 'fonts'),
                os.path.join(os.path.dirname(bundle_dir), 'assets', 'fonts'),
                os.path.join(os.path.dirname(os.path.dirname(bundle_dir)), 'assets', 'fonts'),
            ]
            
            for assets_dir in asset_paths:
                if os.path.exists(assets_dir):
                    for font_file in os.listdir(assets_dir):
                        if font_file.endswith(('.ttf', '.ttc', '.otf')):
                            try:
                                font_path = os.path.join(assets_dir, font_file)
                                font = pygame.font.Font(font_path, size)
                                # 日本語テスト
                                test_surface = font.render("テスト", True, (255, 255, 255))
                                if test_surface.get_width() > 0:
                                    return font
                            except:
                                continue
        except:
            pass
        
        # 2. システム固有フォント検索
        system_font_paths = []
        
        # Windows
        if os.name == 'nt':
            windows_fonts = os.path.join(os.environ.get('WINDIR', 'C:/Windows'), 'Fonts')
            font_candidates = [
                "meiryo.ttc",        # メイリオ
                "meiryob.ttc",       # メイリオ Bold  
                "msgothic.ttc",      # MSゴシック
                "NotoSansCJK-Regular.ttc",  # Noto Sans CJK
            ]
            system_font_paths = [(windows_fonts, f) for f in font_candidates]
        
        # macOS
        elif sys.platform == 'darwin':
            mac_fonts = '/System/Library/Fonts'
            font_candidates = [
                "ヒラギノ角ゴシック W3.ttc",
                "AppleGothic.ttf",
                "NotoSansCJK.ttc",
            ]
            system_font_paths = [(mac_fonts, f) for f in font_candidates]
        
        # Linux
        else:
            linux_font_dirs = ['/usr/share/fonts', '/usr/local/share/fonts']
            for font_dir in linux_font_dirs:
                if os.path.exists(font_dir):
                    for root, dirs, files in os.walk(font_dir):
                        for file in files:
                            if any(keyword in file.lower() for keyword in ['noto', 'deja', 'liberation']):
                                system_font_paths.append((root, file))
        
        # システムフォント試行
        for font_dir, font_name in system_font_paths:
            try:
                font_path = os.path.join(font_dir, font_name)
                if os.path.exists(font_path):
                    font = pygame.font.Font(font_path, size)
                    # 日本語テスト
                    test_surface = font.render("テスト", True, (255, 255, 255))
                    if test_surface.get_width() > 0:
                        return font
            except:
                continue
        
        # 3. pygame.font.SysFont検索
        try:
            system_fonts = pygame.font.get_fonts()
            # 日本語対応可能性の高いフォント
            japanese_fonts = [f for f in system_fonts if any(keyword in f.lower() for keyword in 
                            ['meiryo', 'gothic', 'mincho', 'noto', 'deja', 'liberation', 'arial'])]
            
            for font_name in japanese_fonts[:3]:  # 上位3つまでテスト
                try:
                    font = pygame.font.SysFont(font_name, size)
                    test_surface = font.render("テスト", True, (255, 255, 255))
                    if test_surface.get_width() > 0:
                        return font
                except:
                    continue
        except:
            pass
        
        # 4. 最後の手段: デフォルトフォント
        print(f"Warning: 日本語フォントが見つかりません。デフォルトフォントを使用します。")
        return pygame.font.Font(None, size)
    
    def draw_grid(self):
        for x in range(GRID_WIDTH + 1):
            pygame.draw.line(self.screen, GRAY, 
                           (x * BLOCK_SIZE, 0), 
                           (x * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE))
        
        for y in range(GRID_HEIGHT + 1):
            pygame.draw.line(self.screen, GRAY, 
                           (0, y * BLOCK_SIZE), 
                           (GRID_WIDTH * BLOCK_SIZE, y * BLOCK_SIZE))
    
    def draw_block(self, x, y, color):
        colors = [BLACK, CYAN, YELLOW, PURPLE, GREEN, RED, BLUE, ORANGE]
        rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(self.screen, colors[color], rect)
        pygame.draw.rect(self.screen, WHITE, rect, 2)
    
    def draw_piece(self, piece):
        shape = piece['shape'][piece['rotation']]
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell == '#':
                    self.draw_block(piece['x'] + x, piece['y'] + y, piece['color'])
    
    def draw_next_piece(self, piece):
        shape = piece['shape'][piece['rotation']]
        start_x = GRID_WIDTH * BLOCK_SIZE + 20
        start_y = 100
        
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell == '#':
                    colors = [BLACK, CYAN, YELLOW, PURPLE, GREEN, RED, BLUE, ORANGE]
                    rect = pygame.Rect(start_x + x * 20, start_y + y * 20, 20, 20)
                    pygame.draw.rect(self.screen, colors[piece['color']], rect)
                    pygame.draw.rect(self.screen, WHITE, rect, 1)
    
    def draw_info(self):
        info_x = GRID_WIDTH * BLOCK_SIZE + 20
        
        score_text = self.font.render(f"スコア: {self.tetris.score}", True, WHITE)
        self.screen.blit(score_text, (info_x, 20))
        
        level_text = self.font.render(f"レベル: {self.tetris.level}", True, WHITE)
        self.screen.blit(level_text, (info_x, 60))
        
        lines_text = self.small_font.render(f"ライン: {self.tetris.lines_cleared}", True, WHITE)
        self.screen.blit(lines_text, (info_x, 200))
        
        next_text = self.small_font.render("次のブロック:", True, WHITE)
        self.screen.blit(next_text, (info_x, 250))
        
        if self.tetris.game_over:
            game_over_text = self.font.render("ゲームオーバー", True, RED)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            self.screen.blit(game_over_text, text_rect)
            
            restart_text = self.small_font.render("Rキーでリスタート", True, WHITE)
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 40))
            self.screen.blit(restart_text, restart_rect)
    
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if self.tetris.game_over:
                if event.key == pygame.K_r:
                    self.tetris.reset_game()
            else:
                if event.key == pygame.K_LEFT:
                    self.tetris.move_piece(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    self.tetris.move_piece(1, 0)
                elif event.key == pygame.K_DOWN:
                    self.tetris.move_piece(0, 1)
                elif event.key == pygame.K_UP:
                    self.tetris.rotate_piece()
                elif event.key == pygame.K_SPACE:
                    self.tetris.hard_drop()
    
    def run(self):
        running = True
        
        while running:
            dt = self.clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    self.handle_input(event)
            
            self.tetris.update(dt)
            
            self.screen.fill(BLACK)
            
            # グリッドを描画
            for y in range(GRID_HEIGHT):
                for x in range(GRID_WIDTH):
                    if self.tetris.grid[y][x] != 0:
                        self.draw_block(x, y, self.tetris.grid[y][x])
            
            # 現在のピースを描画
            if not self.tetris.game_over:
                self.draw_piece(self.tetris.current_piece)
            
            self.draw_grid()
            self.draw_info()
            self.draw_next_piece(self.tetris.next_piece)
            
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

def main():
    """メインエントリーポイント"""
    game = TetrisGame()
    game.run()

if __name__ == "__main__":
    main()