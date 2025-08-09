# テトリスゲーム

Pythonで作成されたテトリスのデスクトップクライアントです。複数のGUIフレームワーク対応、CI/CD完備、テスト駆動開発に対応した現代的なプロジェクト構成。

## Claude Code 実行リソースの確認
npx ccusage@latest

## 必要な環境

- Python 3.8以上
- 仮想環境（推奨）

## 環境構築とトラブルシューティング

### 1. pipがインストールされていない場合

**症状**: `pip: command not found` エラー

**Ubuntu/Debian系での解決方法:**
```bash
# 管理者権限がある場合
sudo apt update
sudo apt install python3-pip python3-venv

# 管理者権限がない場合（推奨）
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 -m venv tetris_venv --without-pip
source tetris_venv/bin/activate
python3 get-pip.py
```

**CentOS/RHEL系での解決方法:**
```bash
# 管理者権限がある場合
sudo yum install python3-pip python3-venv
# または
sudo dnf install python3-pip python3-venv

# 管理者権限がない場合
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 -m venv tetris_venv --without-pip
source tetris_venv/bin/activate
python3 get-pip.py
```

**macOS（Homebrew）:**
```bash
brew install python3
# pipは自動的にインストールされます
```

**Windows:**
```bash
# Python公式インストーラーを使用してください
# pipは自動的にインストールされます
```

### 2. python3-venvがない場合

**症状**: `The virtual environment was not created successfully because ensurepip is not available`

**解決方法:**
```bash
# Ubuntu/Debian
sudo apt install python3.12-venv
# または使用しているPythonバージョンに合わせて
sudo apt install python3-venv

# CentOS/RHEL
sudo yum install python3-venv
```

### 3. 外部管理環境エラー（Modern Python環境）

**症状**: `error: externally-managed-environment`

**推奨解決方法（仮想環境使用）:**
```bash
# 仮想環境を作成（推奨）
python3 -m venv tetris_venv
source tetris_venv/bin/activate  # Linux/Mac
# または tetris_venv\Scripts\activate  # Windows

# 以後、仮想環境内で作業
pip install pygame==2.5.2 pyinstaller==6.3.0
```

**一時的解決方法（非推奨）:**
```bash
# システム破壊リスクあり - 本番環境では使用禁止
pip install --break-system-packages pygame==2.5.2 pyinstaller==6.3.0
```

## インストール

### 基本インストール（仮想環境推奨）

```bash
# 1. リポジトリをクローン
git clone <repository-url>
cd python-first

# 2. 仮想環境作成とアクティベート
python3 -m venv tetris_venv
source tetris_venv/bin/activate  # Linux/Mac
# または tetris_venv\Scripts\activate.bat  # Windows

# 3. 最小限の依存関係をインストール
pip install pygame==2.5.2 pyinstaller==6.3.0

# 4. 全依存関係をインストール（オプション）
pip install -r requirements.txt
```

### 開発環境セットアップ

```bash
# 開発用依存関係も含めてインストール
pip install -r requirements.txt
pip install -r requirements-dev.txt

# または pyproject.toml使用
pip install -e ".[dev,gui,build]"
```

## ゲームの実行

### メインゲーム（pygame版）
```bash
# 仮想環境内で実行
source tetris_venv/bin/activate
python src/tetris_game/main.py
```

### 代替GUIランチャー
```bash
# CustomTkinterランチャー
python src/frameworks/tkinter_example.py

# PyQt6ランチャー（追加インストール必要）
pip install PyQt6==6.6.1
python src/frameworks/pyqt_example.py
```

## 操作方法

- **←/→キー**: ブロックを左右に移動
- **↓キー**: ブロックを高速落下
- **↑キー**: ブロックを回転
- **スペースキー**: ブロックを一気に落下
- **Rキー**: ゲームオーバー時にリスタート

## ゲーム機能

- 7種類のテトリミノ（I、O、T、S、Z、J、L字ブロック）
- ライン消去とスコアシステム
- レベルアップによる落下速度の変化
- 次のブロック表示
- ゲームオーバー判定とリスタート機能

## EXE化（実行ファイル作成）

### 自動ビルド

**Linux/Mac:**
```bash
chmod +x scripts/build_exe.sh
source tetris_venv/bin/activate
./scripts/build_exe.sh
```

**Windows:**
```batch
# 通常ビルド
cd scripts
.\build_exe.bat

# デバッグビルド（詳細ログ付き）
cd scripts
.\build_exe_debug.bat
```

### 手動ビルド

```bash
# Linux/Mac
source tetris_venv/bin/activate
cd scripts
pyinstaller tetris.spec
ls -la dist/
```

```batch
# Windows
cd scripts
call ..\tetris_venv\Scripts\activate.bat
pyinstaller tetris.spec
dir dist\
```

### ビルドエラーの対処法

**依存関係不足エラー:**
```bash
# pygame, pyinstallerが必要
source tetris_venv/bin/activate
pip install pygame==2.5.2 pyinstaller==6.3.0
```

**パス関連エラー:**
```bash
# scriptsディレクトリから実行すること
cd scripts
source ../tetris_venv/bin/activate
pyinstaller tetris.spec
```

**成功確認:**
```bash
# ビルド成功時
file scripts/dist/tetris  # Linux実行ファイルを確認
ls -lh scripts/dist/tetris  # ファイルサイズ確認（約18MB）
```

## テスト・品質管理

```bash
# 仮想環境で開発用パッケージをインストール
source tetris_venv/bin/activate
pip install -r requirements-dev.txt

# テスト実行
pytest tests/ -v

# カバレッジ付きテスト
pytest tests/ --cov=src --cov-report=html

# コードフォーマット
black src/ tests/
isort src/ tests/

# 型チェック
mypy src/

# リント
flake8 src/ tests/
```

## CI/CD自動化

GitHub Actionsで以下が自動実行されます：

1. **プッシュ時**: リント→型チェック→テスト→カバレッジ
2. **メインブランチマージ時**: Windows EXE自動生成・アーティファクト保存
3. **テスト合格後のみプッシュ許可**

## プロジェクト構造

```
python-first/
├── src/                      # ソースコード
│   ├── tetris_game/         # メインゲーム
│   └── frameworks/          # 追加GUIフレームワーク
├── tests/                   # テストスイート
├── scripts/                 # ビルドスクリプト
├── .github/workflows/       # CI/CD
└── tetris_venv/            # 仮想環境（ローカル作成）
```

## よくある問題と解決法

### 問題1: ModuleNotFoundError
```bash
# 仮想環境がアクティベートされていない
source tetris_venv/bin/activate
```

### 問題2: pygame音声エラー
```bash
# 音声デバイスがない環境
export SDL_AUDIODRIVER=dummy
python src/tetris_game/main.py
```

### 問題3: Display エラー（GUI環境なし）
```bash
# ヘッドレス環境では実行不可
# GUIが必要なアプリケーションです
```

### 問題4: Permission denied（Linux/Mac）
```bash
chmod +x scripts/build_exe.sh
chmod +x scripts/dist/tetris
```

### 問題5: Windows文字化け
```batch
# コマンドプロンプトの文字エンコーディング設定
chcp 65001

# または PowerShellを使用
# [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

### 問題6: tetris.spec not found（Windows）
```batch
# scriptsディレクトリから実行すること
cd scripts
.\build_exe.bat

# 現在のディレクトリ確認
echo %CD%

# PowerShellの場合
Get-Location
```

### 問題7: Windows実行権限
```batch
# コマンドプロンプトの場合
cd scripts
.\build_exe.bat

# PowerShellの場合（実行ポリシー確認）
Get-ExecutionPolicy
# 必要に応じて一時的に変更
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 問題8: ビルドが通らない場合のデバッグ

#### デバッグビルド実行
```batch
# 詳細ログ付きビルド
cd scripts
.\build_exe_debug.bat

# ログファイル確認
# build_debug_YYYYMMDD_HHMMSS.log が生成される
```

#### よくあるビルドエラーと原因
```
1. "']' は認識されていません" 
   → バッチファイルの文字エンコーディング問題
   → 解決: chcp 65001 でUTF-8設定

2. "option(s) not allowed: --collect-all"
   → 既存.specファイルと--collect-allの併用不可
   → 解決: .spec内でcollect_submodulesを設定

3. "Spec file not found"
   → 実行ディレクトリが間違っている
   → 解決: cd scripts で正しいディレクトリに移動

4. "No module named 'game_engine'"
   → hiddenimportsまたはpathex設定問題
   → 解決: tetris_simple.spec で基本設定テスト
```

#### 段階的デバッグ手順
```batch
# 1. シンプル版でテスト
pyinstaller tetris_simple.spec

# 2. コンソール版で実行エラー確認  
pyinstaller --console --onefile ../src/tetris_game/main.py

# 3. 詳細ログでビルドエラー特定
pyinstaller --log-level=DEBUG tetris.spec
```

### 問題9: EXE実行時のエラー

#### ModuleNotFoundError（モジュール未発見）
```batch
# game_engineモジュールが見つからない場合
# 1. tetris.specのhiddenimportsを確認
hiddenimports=['pygame', 'pygame._sdl2', 'tetris_game.game_engine'],

# 2. .specファイル内でcollect設定（推奨）
collect_submodules=['tetris_game'],
collect_data=['tetris_game'],

# 3. 手動で全モジュール収集（.specファイルなしの場合）
pyinstaller --collect-all tetris_game --onefile src/tetris_game/main.py
```

#### pygame初期化エラー
```batch
# 音声デバイスがない環境
set SDL_AUDIODRIVER=dummy
scripts\dist\tetris.exe

# または環境変数を永続設定
setx SDL_AUDIODRIVER dummy
```

#### pathspec関連エラー
```batch
# 相対パスの問題の場合
# tetris.spec内のパスを絶対パスに修正
```

#### DLL読み込みエラー
```batch
# Visual C++ Redistributableが必要
# https://aka.ms/vs/17/release/vc_redist.x64.exe
```

#### 日本語文字化け
```batch
# Windowsでの日本語表示問題
# 1. システムフォント確認
dir "%WINDIR%\Fonts" | find "meiryo"
dir "%WINDIR%\Fonts" | find "msgothic"

# 2. フォントが見つからない場合の対処
# メイリオやMSゴシックがない場合は以下をインストール:
# - Windows Updates確認
# - 言語パック追加インストール

# 3. 代替フォント使用
# assets/fonts/ に日本語対応TTFファイルを配置
# 例: NotoSansCJK-Regular.ttf
```

## 注意事項

- **推奨**: 必ず仮想環境を使用してください
- **GUI必須**: ディスプレイのない環境では動作しません  
- **仮想環境**: `tetris_venv/`は`.gitignore`で管理外です
- **ビルド環境**: Linux版実行ファイルが生成されます（Windows版はWindows環境で実行）

## サポート情報

- Python バージョン: 3.8以上推奨（テスト済み: 3.12.3）
- プラットフォーム: Linux, macOS, Windows
- 必須ライブラリ: pygame 2.5.2, pyinstaller 6.3.0
- 仮想環境推奨サイズ: ~200MB（全依存関係含む）