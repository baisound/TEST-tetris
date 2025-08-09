@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo テトリスゲームのEXE化を開始します...
echo.

:: Python環境確認
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Pythonがインストールされていません。
    echo         https://python.org からダウンロードしてください。
    pause
    exit /b 1
)

echo [OK] Pythonが見つかりました
python --version

:: pip確認
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pipがインストールされていません。
    echo         Python公式インストーラーでpipを含めてインストールしてください。
    pause
    exit /b 1
)

echo [OK] pipが見つかりました

:: 仮想環境確認・作成
if not exist "..\tetris_venv" (
    echo [INFO] 仮想環境を作成中...
    python -m venv ..\tetris_venv
    if errorlevel 1 (
        echo [ERROR] 仮想環境の作成に失敗しました。
        pause
        exit /b 1
    )
)

:: 仮想環境をアクティベート
echo [INFO] 仮想環境をアクティベート中...
call ..\tetris_venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] 仮想環境のアクティベートに失敗しました。
    pause
    exit /b 1
)

:: 最小限の依存関係をインストール
echo [INFO] 依存関係をインストール中...
pip install pygame==2.5.2 pyinstaller==6.3.0
if errorlevel 1 (
    echo [ERROR] 依存関係のインストールに失敗しました。
    echo         インターネット接続を確認してください。
    pause
    exit /b 1
)

echo [OK] 依存関係のインストール完了

:: tetris.specファイルの存在確認
if not exist "tetris.spec" (
    echo [ERROR] tetris.spec ファイルが見つかりません。
    echo         scripts ディレクトリから実行していることを確認してください。
    echo         現在のディレクトリ: %CD%
    echo.
    echo [INFO] 利用可能なファイル:
    dir /b
    pause
    exit /b 1
)

:: PyInstallerでEXE化
echo [INFO] PyInstallerでビルド中...
pyinstaller --collect-all tetris_game tetris.spec
if errorlevel 1 (
    echo [ERROR] ビルドに失敗しました。
    pause
    exit /b 1
)

:: 結果確認
if exist "dist\tetris.exe" (
    for %%F in (dist\tetris.exe) do set FILE_SIZE=%%~zF
    echo.
    echo [SUCCESS] EXE化が正常に完了しました！
    echo [INFO] 生成されたファイル: scripts\dist\tetris.exe
    echo [INFO] ファイルサイズ: !FILE_SIZE! bytes
    echo.
    echo [INFO] 実行方法:
    echo         dist\tetris.exe をダブルクリック
    echo         または: .\scripts\dist\tetris.exe
) else (
    echo [ERROR] 実行ファイルの生成に失敗しました。
    pause
    exit /b 1
)

echo.
echo [SUCCESS] ビルドプロセス完了！
echo.
pause