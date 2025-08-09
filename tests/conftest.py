"""pytest設定ファイル"""

import pytest
import sys
import os

# テスト実行時にsrcディレクトリをPYTHONPATHに追加
@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """テスト環境のセットアップ"""
    src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
    if src_path not in sys.path:
        sys.path.insert(0, src_path)

@pytest.fixture
def sample_grid():
    """テスト用のサンプルグリッド"""
    return [[0 for _ in range(10)] for _ in range(20)]

@pytest.fixture
def filled_bottom_row():
    """最下段が満杯のグリッド"""
    grid = [[0 for _ in range(10)] for _ in range(20)]
    # 最下段を満杯にする
    for x in range(10):
        grid[19][x] = 1
    return grid