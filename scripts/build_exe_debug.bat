@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo テトリスゲーム EXE化デバッグビルド
echo ========================================
echo.

:: デバッグログファイル作成
set LOG_FILE=build_debug_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%.log
echo デバッグログファイル: %LOG_FILE% > %LOG_FILE%
echo ビルド開始時刻: %date% %time% >> %LOG_FILE%

:: 環境情報収集
echo [STEP 1/10] 環境情報を収集中...
echo ---------------------------------------- >> %LOG_FILE%
echo 環境情報: >> %LOG_FILE%
echo OS: %OS% >> %LOG_FILE%
echo PATH: %PATH% >> %LOG_FILE%
echo PYTHONPATH: %PYTHONPATH% >> %LOG_FILE%
echo 現在のディレクトリ: %CD% >> %LOG_FILE%

:: Python環境確認
echo [STEP 2/10] Python環境を確認中...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Pythonがインストールされていません。 >> %LOG_FILE%
    echo [ERROR] Pythonがインストールされていません。
    echo         https://python.org からダウンロードしてください。
    pause
    exit /b 1
) else (
    echo [OK] Pythonが見つかりました >> %LOG_FILE%
    python --version >> %LOG_FILE%
    echo [OK] Pythonが見つかりました
    python --version
)

:: pip環境確認
echo [STEP 3/10] pip環境を確認中...
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pipがインストールされていません。 >> %LOG_FILE%
    echo [ERROR] pipがインストールされていません。
    echo         Python公式インストーラーでpipを含めてインストールしてください。
    pause
    exit /b 1
) else (
    echo [OK] pipが見つかりました >> %LOG_FILE%
    pip --version >> %LOG_FILE%
    echo [OK] pipが見つかりました
)

:: ファイル構造確認
echo [STEP 4/10] ファイル構造を確認中...
echo ---------------------------------------- >> %LOG_FILE%
echo 現在のディレクトリ内容: >> %LOG_FILE%
dir >> %LOG_FILE%
echo. >> %LOG_FILE%

echo [INFO] 現在のディレクトリ: %CD%
echo [INFO] 利用可能なファイル:
dir /b

:: 重要ファイルの存在確認
echo [STEP 5/10] 重要ファイルの存在確認...
echo ---------------------------------------- >> %LOG_FILE%

set FILES_MISSING=0

if not exist "tetris.spec" (
    echo [ERROR] tetris.spec が見つかりません >> %LOG_FILE%
    echo [ERROR] tetris.spec が見つかりません
    set FILES_MISSING=1
) else (
    echo [OK] tetris.spec が見つかりました >> %LOG_FILE%
    echo [OK] tetris.spec が見つかりました
)

if not exist "..\src\tetris_game\main.py" (
    echo [ERROR] main.py が見つかりません >> %LOG_FILE%
    echo [ERROR] main.py が見つかりません
    set FILES_MISSING=1
) else (
    echo [OK] main.py が見つかりました >> %LOG_FILE%
    echo [OK] main.py が見つかりました
)

if not exist "..\src\tetris_game\game_engine.py" (
    echo [ERROR] game_engine.py が見つかりません >> %LOG_FILE%
    echo [ERROR] game_engine.py が見つかりません
    set FILES_MISSING=1
) else (
    echo [OK] game_engine.py が見つかりました >> %LOG_FILE%
    echo [OK] game_engine.py が見つかりました
)

if !FILES_MISSING! equ 1 (
    echo [ERROR] 必要なファイルが不足しています。ビルドを中断します。
    echo [ERROR] ファイル不足によりビルド中断 >> %LOG_FILE%
    pause
    exit /b 1
)

:: 仮想環境確認・作成
echo [STEP 6/10] 仮想環境を確認中...
if not exist "..\tetris_venv" (
    echo [INFO] 仮想環境を作成中...
    echo 仮想環境作成開始 >> %LOG_FILE%
    python -m venv ..\tetris_venv >> %LOG_FILE% 2>&1
    if errorlevel 1 (
        echo [ERROR] 仮想環境の作成に失敗しました。 >> %LOG_FILE%
        echo [ERROR] 仮想環境の作成に失敗しました。
        pause
        exit /b 1
    )
) else (
    echo [OK] 仮想環境が存在します >> %LOG_FILE%
    echo [OK] 仮想環境が存在します
)

:: 仮想環境をアクティベート
echo [STEP 7/10] 仮想環境をアクティベート中...
echo 仮想環境アクティベート開始 >> %LOG_FILE%
call ..\tetris_venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] 仮想環境のアクティベートに失敗しました。 >> %LOG_FILE%
    echo [ERROR] 仮想環境のアクティベートに失敗しました。
    pause
    exit /b 1
)

:: インストール済みパッケージ確認
echo [STEP 8/10] インストール済みパッケージを確認中...
echo ---------------------------------------- >> %LOG_FILE%
echo インストール済みパッケージ: >> %LOG_FILE%
pip list >> %LOG_FILE%

:: 依存関係をインストール
echo [STEP 9/10] 依存関係をインストール中...
echo 依存関係インストール開始 >> %LOG_FILE%
pip install pygame==2.5.2 pyinstaller==6.3.0 >> %LOG_FILE% 2>&1
if errorlevel 1 (
    echo [ERROR] 依存関係のインストールに失敗しました。 >> %LOG_FILE%
    echo [ERROR] 依存関係のインストールに失敗しました。
    echo         インターネット接続を確認してください。
    pause
    exit /b 1
)

echo [OK] 依存関係のインストール完了

:: tetris.spec内容確認
echo [STEP 10/10] tetris.spec内容確認...
echo ---------------------------------------- >> %LOG_FILE%
echo tetris.spec内容: >> %LOG_FILE%
type tetris.spec >> %LOG_FILE%

:: PyInstallerでEXE化（詳細ログ付き）
echo [INFO] PyInstallerでビルド中（詳細ログ出力）...
echo ---------------------------------------- >> %LOG_FILE%
echo PyInstallerビルド開始: %date% %time% >> %LOG_FILE%

pyinstaller --log-level=DEBUG --workpath=build_debug --distpath=dist_debug tetris.spec >> %LOG_FILE% 2>&1
set BUILD_RESULT=%errorlevel%

echo PyInstallerビルド終了: %date% %time% >> %LOG_FILE%
echo PyInstallerリターンコード: %BUILD_RESULT% >> %LOG_FILE%

if %BUILD_RESULT% neq 0 (
    echo [ERROR] ビルドに失敗しました。 >> %LOG_FILE%
    echo [ERROR] ビルドに失敗しました。
    echo.
    echo [INFO] デバッグ情報:
    echo         - ログファイル: %LOG_FILE%
    echo         - ビルドログ: build_debug\
    echo         - エラーコード: %BUILD_RESULT%
    echo.
    echo [INFO] よくあるエラーと対処法:
    echo         1. ModuleNotFoundError → hiddenimports確認
    echo         2. Path関連エラー → pathex設定確認  
    echo         3. 権限エラー → 管理者権限で実行
    echo         4. メモリ不足 → 不要なプログラム終了
    pause
    exit /b 1
)

:: 結果確認
if exist "dist_debug\tetris.exe" (
    for %%F in (dist_debug\tetris.exe) do set FILE_SIZE=%%~zF
    echo.
    echo [SUCCESS] EXE化が正常に完了しました！ >> %LOG_FILE%
    echo [SUCCESS] EXE化が正常に完了しました！
    echo [INFO] 生成されたファイル: scripts\dist_debug\tetris.exe
    echo [INFO] ファイルサイズ: !FILE_SIZE! bytes
    echo [INFO] ログファイル: %LOG_FILE%
    echo.
    echo [INFO] 実行方法:
    echo         dist_debug\tetris.exe をダブルクリック
    echo         または: .\scripts\dist_debug\tetris.exe
) else (
    echo [ERROR] 実行ファイルの生成に失敗しました。 >> %LOG_FILE%
    echo [ERROR] 実行ファイルの生成に失敗しました。
    echo         詳細は %LOG_FILE% を確認してください。
    pause
    exit /b 1
)

echo.
echo [SUCCESS] デバッグビルドプロセス完了！
echo [INFO] 全ログは %LOG_FILE% に保存されました。
echo.
pause