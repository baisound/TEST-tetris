"""テトリスゲーム メインアプリケーション"""

import pygame
import sys
from game_engine import GameEngine

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
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
    
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