#!/bin/bash
echo "テトリスゲームのEXE化を開始します..."

# 依存関係をインストール
echo "依存関係をインストール中..."
pip install -r requirements.txt

# PyInstallerでEXE化
echo "PyInstallerでEXE化中..."
pyinstaller tetris.spec

# 完了メッセージ
echo ""
echo "EXE化が完了しました！"
echo "生成されたファイル: dist/tetris.exe"
echo ""
echo "実行するには dist/tetris.exe をダブルクリックしてください。"
echo ""