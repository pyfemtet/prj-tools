@echo off
setlocal enabledelayedexpansion

REM Release process.
REM
REM check test,
REM merge to release,
REM estimate version name
REM and add tag.
REM
REM Usage
REM =====
REM sample:
REM   .\tools\release
REM

REM move to project root
cd %~dp0\..

REM リリース中フラグがなければテスト終了処理
    if not exist ".release-processing" (
    REM テストを終了
    call .\tools\test-end.cmd

    REM テストが終了しなければ何もしない
    if errorlevel 1 (
        echo === Cancel release. ===
        GOTO :ERROR
    )
)

REM テストは終了したはずなのでリリース中フラグを立てる
echo "Release is processing. Remove this file to cancel release." > ".release-processing"

REM main ブランチであることを確認
for /f "tokens=*" %%b in ('git rev-parse --abbrev-ref HEAD') do set current_branch=%%b
if NOT "%current_branch%"=="main" (
    echo === Current branch is "%current_branch%". Please switch to "main" branch before release.===
    GOTO :ERROR
)

REM release ブランチに切り替え
git checkout release-1
if errorlevel 1 (
    echo === Failed to checkout release branch. ===
    GOTO :ERROR
)

REM main をマージ
git merge main --no-ff
if errorlevel 1 (
    echo Merge failed.
    GOTO :ERROR
)

REM タグを生成、付与
uv run python .\tools\_impl\create_tag.py

REM 切り戻し
git checkout %current_branch%
if errorlevel 1 (
    echo Failed to checkout back to %current_branch%.
    GOTO :ERROR
)

REM remove .release
del /q ".release-processing

endlocal

REM 通常の終了
exit /b 0

REM エラー終了
:ERROR
endlocal
exit /b 1
