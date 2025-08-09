"""ゲームエンジンのテスト"""

import pytest
import sys
import os

# srcディレクトリをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from tetris_game.game_engine import GameEngine


class TestGameEngine:
    """GameEngineクラスのテスト"""
    
    def setup_method(self):
        """各テストメソッドの前に実行される初期化"""
        self.engine = GameEngine(10, 20)
    
    def test_init(self):
        """初期化テスト"""
        assert self.engine.grid_width == 10
        assert self.engine.grid_height == 20
        assert self.engine.score == 0
        assert self.engine.level == 1
        assert self.engine.game_over == False
        assert len(self.engine.grid) == 20
        assert len(self.engine.grid[0]) == 10
    
    def test_get_new_piece(self):
        """新しいピース生成テスト"""
        piece = self.engine.get_new_piece()
        
        assert 'shape' in piece
        assert 'rotation' in piece
        assert 'x' in piece
        assert 'y' in piece
        assert 'color' in piece
        
        assert piece['rotation'] == 0
        assert piece['x'] == 3  # (10 // 2) - 2 = 3
        assert piece['y'] == 0
        assert 1 <= piece['color'] <= 7
    
    def test_is_valid_position_initial(self):
        """初期位置の有効性テスト"""
        assert self.engine.current_piece is not None
        assert self.engine.is_valid_position(self.engine.current_piece)
    
    def test_move_piece_valid(self):
        """有効な移動テスト"""
        original_x = self.engine.current_piece['x']
        success = self.engine.move_piece(1, 0)  # 右に移動
        
        assert success == True
        assert self.engine.current_piece['x'] == original_x + 1
    
    def test_move_piece_invalid(self):
        """無効な移動テスト（壁を超える）"""
        # 左端まで移動
        for _ in range(10):
            self.engine.move_piece(-1, 0)
        
        # さらに左に移動を試行（失敗するはず）
        success = self.engine.move_piece(-1, 0)
        assert success == False
    
    def test_rotate_piece(self):
        """ピース回転テスト"""
        original_rotation = self.engine.current_piece['rotation']
        success = self.engine.rotate_piece()
        
        # 回転可能な形状の場合
        if len(self.engine.current_piece['shape']) > 1:
            assert success == True
            expected_rotation = (original_rotation + 1) % len(self.engine.current_piece['shape'])
            assert self.engine.current_piece['rotation'] == expected_rotation
        else:
            # O字ブロック（回転しない）の場合
            assert self.engine.current_piece['rotation'] == original_rotation
    
    def test_hard_drop(self):
        """ハードドロップテスト"""
        original_y = self.engine.current_piece['y']
        self.engine.hard_drop()
        
        # Y座標が増加しているはず
        assert self.engine.current_piece['y'] > original_y
    
    def test_clear_lines_empty_grid(self):
        """空のグリッドでのライン消去テスト"""
        cleared = self.engine.clear_lines()
        assert cleared == 0
        assert self.engine.score == 0
        assert self.engine.lines_cleared == 0
    
    def test_clear_lines_full_line(self):
        """満杯ラインの消去テスト"""
        # 最下段を満杯にする
        bottom_row = self.engine.grid_height - 1
        for x in range(self.engine.grid_width):
            self.engine.grid[bottom_row][x] = 1
        
        cleared = self.engine.clear_lines()
        assert cleared == 1
        assert self.engine.lines_cleared == 1
        assert self.engine.score == 100  # 1ライン × 100 × レベル1
        
        # 最下段が空になっているはず
        assert all(cell == 0 for cell in self.engine.grid[bottom_row])
    
    def test_game_state(self):
        """ゲーム状態取得テスト"""
        state = self.engine.get_game_state()
        
        required_keys = ['grid', 'current_piece', 'next_piece', 'score', 'level', 'lines_cleared', 'game_over']
        for key in required_keys:
            assert key in state
    
    def test_reset_game(self):
        """ゲームリセットテスト"""
        # ゲーム状態を変更
        self.engine.score = 1000
        self.engine.level = 5
        self.engine.lines_cleared = 50
        self.engine.game_over = True
        self.engine.grid[0][0] = 1
        
        # リセット実行
        self.engine.reset_game()
        
        # 初期状態に戻っているかチェック
        assert self.engine.score == 0
        assert self.engine.level == 1
        assert self.engine.lines_cleared == 0
        assert self.engine.game_over == False
        assert self.engine.grid[0][0] == 0
        assert self.engine.current_piece is not None
        assert self.engine.next_piece is not None

    def test_level_progression(self):
        """レベル進行テスト"""
        # 10ライン消去でレベル2になるはず
        self.engine.lines_cleared = 10
        self.engine.clear_lines()  # レベル計算を更新
        
        # lines_clearedは変わらないが、レベル計算が実行される
        expected_level = self.engine.lines_cleared // 10 + 1
        assert self.engine.level == expected_level

class TestGameEngineIntegration:
    """統合テスト"""
    
    def test_full_game_cycle(self):
        """完全なゲームサイクルテスト"""
        engine = GameEngine(10, 20)
        
        # 初期状態の確認
        assert not engine.game_over
        assert engine.current_piece is not None
        
        # 複数回の更新をシミュレート
        for _ in range(100):
            engine.update(100)  # 100ms経過をシミュレート
            if engine.game_over:
                break
        
        # ゲーム状態が一貫していることを確認
        state = engine.get_game_state()
        assert isinstance(state['score'], int)
        assert isinstance(state['level'], int)
        assert isinstance(state['lines_cleared'], int)

if __name__ == "__main__":
    pytest.main([__file__])