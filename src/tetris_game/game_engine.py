"""テトリスゲームエンジンモジュール"""

import random
from typing import List, Dict, Any, Optional, Tuple


class GameEngine:
    """テトリスのゲームロジックを管理するクラス"""
    
    # テトリスブロックの形状定義
    TETRIS_SHAPES = [
        # I字ブロック
        [
            ['.....',
             '..#..',
             '..#..',
             '..#..',
             '..#..'],
            ['.....',
             '.....',
             '####.',
             '.....',
             '.....']
        ],
        # O字ブロック
        [
            ['.....',
             '.....',
             '.##..',
             '.##..',
             '.....']
        ],
        # T字ブロック
        [
            ['.....',
             '.....',
             '.#...',
             '###..',
             '.....'],
            ['.....',
             '.....',
             '.#...',
             '.##..',
             '.#...'],
            ['.....',
             '.....',
             '.....',
             '###..',
             '.#...'],
            ['.....',
             '.....',
             '.#...',
             '##...',
             '.#...']
        ],
        # S字ブロック
        [
            ['.....',
             '.....',
             '.##..',
             '##...',
             '.....'],
            ['.....',
             '.#...',
             '.##..',
             '..#..',
             '.....']
        ],
        # Z字ブロック
        [
            ['.....',
             '.....',
             '##...',
             '.##..',
             '.....'],
            ['.....',
             '..#..',
             '.##..',
             '.#...',
             '.....']
        ],
        # J字ブロック
        [
            ['.....',
             '.#...',
             '.#...',
             '##...',
             '.....'],
            ['.....',
             '.....',
             '#....',
             '###..',
             '.....'],
            ['.....',
             '.##..',
             '.#...',
             '.#...',
             '.....'],
            ['.....',
             '.....',
             '###..',
             '..#..',
             '.....']
        ],
        # L字ブロック
        [
            ['.....',
             '..#..',
             '..#..',
             '.##..',
             '.....'],
            ['.....',
             '.....',
             '###..',
             '#....',
             '.....'],
            ['.....',
             '##...',
             '.#...',
             '.#...',
             '.....'],
            ['.....',
             '.....',
             '..#..',
             '###..',
             '.....']
        ]
    ]
    
    def __init__(self, grid_width: int = 10, grid_height: int = 20):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.grid: List[List[int]] = [[0 for _ in range(grid_width)] for _ in range(grid_height)]
        self.current_piece: Optional[Dict[str, Any]] = None
        self.next_piece: Optional[Dict[str, Any]] = None
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.fall_time = 0
        self.fall_speed = 500  # ミリ秒
        self.game_over = False
        
        # 初期ピースを生成
        self.current_piece = self.get_new_piece()
        self.next_piece = self.get_new_piece()
    
    def get_new_piece(self) -> Dict[str, Any]:
        """新しいテトリスピースを生成"""
        shape_index = random.randint(0, len(self.TETRIS_SHAPES) - 1)
        return {
            'shape': self.TETRIS_SHAPES[shape_index],
            'rotation': 0,
            'x': self.grid_width // 2 - 2,
            'y': 0,
            'color': shape_index + 1
        }
    
    def is_valid_position(self, piece: Dict[str, Any], dx: int = 0, dy: int = 0, rotation: Optional[int] = None) -> bool:
        """ピースの位置が有効かチェック"""
        if rotation is None:
            rotation = piece['rotation']
        
        shape = piece['shape'][rotation]
        
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell == '#':
                    new_x = piece['x'] + x + dx
                    new_y = piece['y'] + y + dy
                    
                    if (new_x < 0 or new_x >= self.grid_width or 
                        new_y >= self.grid_height or
                        (new_y >= 0 and self.grid[new_y][new_x] != 0)):
                        return False
        return True
    
    def place_piece(self, piece: Dict[str, Any]) -> None:
        """ピースをグリッドに配置"""
        shape = piece['shape'][piece['rotation']]
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell == '#':
                    grid_x = piece['x'] + x
                    grid_y = piece['y'] + y
                    if grid_y >= 0:
                        self.grid[grid_y][grid_x] = piece['color']
    
    def clear_lines(self) -> int:
        """完成したラインをクリアしてスコアを更新"""
        lines_to_clear = []
        for y in range(self.grid_height):
            if all(self.grid[y][x] != 0 for x in range(self.grid_width)):
                lines_to_clear.append(y)
        
        for y in lines_to_clear:
            del self.grid[y]
            self.grid.insert(0, [0 for _ in range(self.grid_width)])
        
        lines_cleared = len(lines_to_clear)
        self.lines_cleared += lines_cleared
        self.score += lines_cleared * 100 * self.level
        self.level = self.lines_cleared // 10 + 1
        self.fall_speed = max(50, 500 - (self.level - 1) * 50)
        
        return lines_cleared
    
    def move_piece(self, dx: int, dy: int) -> bool:
        """ピースを移動"""
        if self.current_piece and self.is_valid_position(self.current_piece, dx, dy):
            self.current_piece['x'] += dx
            self.current_piece['y'] += dy
            return True
        return False
    
    def rotate_piece(self) -> bool:
        """ピースを回転"""
        if not self.current_piece:
            return False
            
        original_rotation = self.current_piece['rotation']
        new_rotation = (original_rotation + 1) % len(self.current_piece['shape'])
        
        if self.is_valid_position(self.current_piece, rotation=new_rotation):
            self.current_piece['rotation'] = new_rotation
            return True
        return False
    
    def hard_drop(self) -> None:
        """ピースを一気に落下"""
        if self.current_piece:
            while self.move_piece(0, 1):
                pass
    
    def update(self, dt: int) -> None:
        """ゲーム状態を更新"""
        if self.game_over or not self.current_piece:
            return
        
        self.fall_time += dt
        
        if self.fall_time >= self.fall_speed:
            if not self.move_piece(0, 1):
                self.place_piece(self.current_piece)
                self.clear_lines()
                
                self.current_piece = self.next_piece
                self.next_piece = self.get_new_piece()
                
                if not self.is_valid_position(self.current_piece):
                    self.game_over = True
            
            self.fall_time = 0
    
    def reset_game(self) -> None:
        """ゲームをリセット"""
        self.grid = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        self.current_piece = self.get_new_piece()
        self.next_piece = self.get_new_piece()
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.fall_time = 0
        self.fall_speed = 500
        self.game_over = False
    
    def get_game_state(self) -> Dict[str, Any]:
        """現在のゲーム状態を取得"""
        return {
            'grid': self.grid,
            'current_piece': self.current_piece,
            'next_piece': self.next_piece,
            'score': self.score,
            'level': self.level,
            'lines_cleared': self.lines_cleared,
            'game_over': self.game_over
        }