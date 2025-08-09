@echo off
setlocal enabledelayedexpansion

echo 🎮 テトリスゲームのEXE化を開始します...
echo.

:: Python環境確認
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Pythonがインストールされていません。
    echo    https://python.org からダウンロードしてください。
    pause
    exit /b 1
)

echo ✅ Pythonが見つかりました
python --version

:: pip確認
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pipがインストールされていません。
    echo    Python公式インストーラーでpipを含めてインストールしてください。
    pause
    exit /b 1
)

echo ✅ pipが見つかりました

:: 仮想環境確認・作成
if not exist "..\tetris_venv" (
    echo 📦 仮想環境を作成中...
    python -m venv ..\tetris_venv
    if errorlevel 1 (
        echo ❌ 仮想環境の作成に失敗しました。
        pause
        exit /b 1
    )
)

:: 仮想環境をアクティベート
echo 📦 仮想環境をアクティベート中...
call ..\tetris_venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ 仮想環境のアクティベートに失敗しました。
    pause
    exit /b 1
)

:: 最小限の依存関係をインストール
echo 📥 依存関係をインストール中...
pip install pygame==2.5.2 pyinstaller==6.3.0
if errorlevel 1 (
    echo ❌ 依存関係のインストールに失敗しました。
    echo    インターネット接続を確認してください。
    pause
    exit /b 1
)

echo ✅ 依存関係のインストール完了

:: PyInstallerでEXE化
echo 🔨 PyInstallerでビルド中...
pyinstaller tetris.spec
if errorlevel 1 (
    echo ❌ ビルドに失敗しました。
    pause
    exit /b 1
)

:: 結果確認
if exist "dist\tetris.exe" (
    for %%F in (dist\tetris.exe) do set FILE_SIZE=%%~zF
    echo.
    echo 🎉 EXE化が正常に完了しました！
    echo 📁 生成されたファイル: scripts\dist\tetris.exe
    echo 📊 ファイルサイズ: !FILE_SIZE! bytes
    echo.
    echo 🚀 実行方法:
    echo    dist\tetris.exe をダブルクリック
    echo    または: .\scripts\dist\tetris.exe
) else (
    echo ❌ 実行ファイルの生成に失敗しました。
    pause
    exit /b 1
)

echo.
echo ✅ ビルドプロセス完了！
echo.
pause