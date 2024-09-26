@echo off
REM 文字コードをUTF-8に指定（日本語パスがある場合のみ必要）
chcp 65001

REM 仮想環境をActivateするためのバッチファイルを起動
CALL "C:\Users\XXX\anaconda3\Scripts\activate.bat"

REM 仮想環境Transformerをアクティブにする
CALL conda activate YYY

REM Pythonスクリプトを非表示で実行
start /min "" "C:\Users\XXX\anaconda3\envs\YYY\pythonw.exe" "F:\other\pomodoro\main.py"

REM 終了後にConda環境を非アクティブ化
CALL conda deactivate