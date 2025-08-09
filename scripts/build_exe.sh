#!/bin/bash

# エラーハンドリング設定
set -e  # エラー時に即座に終了
trap 'echo "❌ ビルド処理中にエラーが発生しました。"; exit 1' ERR

echo "🎮 テトリスゲームのEXE化を開始します..."
echo ""

# Python環境確認
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3がインストールされていません。"
    echo "   Ubuntu: sudo apt install python3"
    echo "   CentOS: sudo yum install python3"
    exit 1
fi

echo "✅ Python3が見つかりました: $(python3 --version)"

# pip確認とインストール
if ! command -v pip &> /dev/null && ! python3 -m pip --version &> /dev/null; then
    echo "⚠️  pipが見つかりません。インストールします..."
    
    # get-pip.pyをダウンロード
    if ! curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py; then
        echo "❌ pip インストーラーのダウンロードに失敗しました。"
        exit 1
    fi
    
    # 仮想環境作成
    echo "📦 仮想環境を作成中..."
    if ! python3 -m venv ../tetris_venv --without-pip; then
        echo "❌ 仮想環境の作成に失敗しました。"
        echo "   sudo apt install python3-venv をお試しください。"
        exit 1
    fi
    
    # 仮想環境内でpipをインストール
    echo "🔧 仮想環境内でpipをインストール中..."
    source ../tetris_venv/bin/activate
    if ! python3 get-pip.py; then
        echo "❌ pipのインストールに失敗しました。"
        exit 1
    fi
    rm get-pip.py
else
    echo "✅ pipが見つかりました"
    
    # 仮想環境が既に存在するかチェック
    if [ -d "../tetris_venv" ]; then
        echo "📦 既存の仮想環境を使用します"
        source ../tetris_venv/bin/activate
    else
        echo "📦 新しい仮想環境を作成中..."
        if ! python3 -m venv ../tetris_venv; then
            echo "❌ 仮想環境の作成に失敗しました。"
            exit 1
        fi
        source ../tetris_venv/bin/activate
    fi
fi

# 最小限の依存関係をインストール
echo "📥 依存関係をインストール中..."
if ! pip install pygame==2.5.2 pyinstaller==6.3.0; then
    echo "❌ 依存関係のインストールに失敗しました。"
    echo "   インターネット接続を確認してください。"
    exit 1
fi

echo "✅ 依存関係のインストール完了"

# PyInstallerでビルド
echo "🔨 PyInstallerでビルド中..."
if ! pyinstaller tetris.spec; then
    echo "❌ ビルドに失敗しました。"
    exit 1
fi

# 結果確認
if [ -f "dist/tetris" ]; then
    FILE_SIZE=$(ls -lh dist/tetris | awk '{print $5}')
    echo ""
    echo "🎉 EXE化が正常に完了しました！"
    echo "📁 生成されたファイル: scripts/dist/tetris"
    echo "📊 ファイルサイズ: $FILE_SIZE"
    echo ""
    echo "🚀 実行方法:"
    echo "   ./scripts/dist/tetris"
    echo ""
    echo "🔍 ファイル詳細:"
    file dist/tetris
else
    echo "❌ 実行ファイルの生成に失敗しました。"
    exit 1
fi

echo ""
echo "✅ ビルドプロセス完了！"