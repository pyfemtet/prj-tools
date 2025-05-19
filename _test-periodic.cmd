REM 定期テスト

REM move to project root
cd %~dp0\..

REM テスト開始
call .\tools\test-start.cmd

REM テスト実行
call .\tools\test-run-automated.cmd

REM テスト終了
call .\tools\test-end.cmd -f
