# テトリスゲーム

Pythonで作成されたテトリスのデスクトップクライアントです。

## 必要な環境

- Python 3.6以上
- pygame 2.5.2

## インストール

```bash
pip install -r requirements.txt
```

## ゲームの実行

```bash
python tetris.py
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

## EXE化（Windows実行ファイル作成）

WindowsでPythonがインストールされていない環境でも実行できるEXEファイルを作成できます。

### Windows環境での手順

1. **依存関係の確認**
   ```bash
   pip install -r requirements.txt
   ```

2. **自動EXE化**
   ```bash
   build_exe.bat
   ```

3. **手動EXE化**
   ```bash
   pyinstaller tetris.spec
   ```

4. **実行**
   - `dist/tetris.exe` が生成されます
   - このファイルをダブルクリックして実行

### Linux/Mac環境での手順

```bash
chmod +x build_exe.sh
./build_exe.sh
```

### EXE化の特徴

- **単一ファイル**: すべての依存関係が含まれた単体のEXEファイル
- **コンソール非表示**: GUI専用アプリケーションとして動作
- **配布可能**: PythonがインストールされていないWindows環境でも実行可能

## 注意事項

- Docker環境で実行する場合は、GUIアプリケーションの実行に必要な設定が必要です
- EXE化にはWindows環境またはWine環境が推奨されます
- pygame の依存関係やディスプレイの設定を確認してください