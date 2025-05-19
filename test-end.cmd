@echo off

REM
REM Sample:
REM   .\tools\test-end.cmd     # テスト終了処理を実行
REM   .\tools\test-end.cmd -f  # テスト failed を許容して
REM                            #   .test-running を削除
REM                            #   ただし終了コードは 1
REM

REM move to project root
cd %~dp0\..

REM オプション判定
set FORCE_DELETE_RUNNING=0
if /i "%1"=="-f" set FORCE_DELETE_RUNNING=1

REM テスト実行中フラグがなければ何もしない
if not exist ".test-running" (
    echo Test is not running. Start `test-start.cmd` first.
    GOTO :ERROR
)

REM 実際の処理
uv run python ".\tools\_impl\test_done.py" ".test-running"

if errorlevel 1 (
    echo === Test Failed. ===

    if %FORCE_DELETE_RUNNING% EQU 1 (
        REM .test-running を削除
        del /q ".test-running"
    )

    GOTO :ERROR
)

REM .test-running を削除
del /q ".test-running"


REM 通常の終了
exit /b 0

REM エラー終了
:ERROR
exit /b 1
