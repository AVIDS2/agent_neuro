@echo off
echo 启动 Agent Neuro 语音服务...
echo.
echo 正在检查Python环境...
python --version
if %errorlevel% neq 0 (
    echo 错误: Python未安装或未添加到PATH
    pause
    exit /b 1
)

echo.
echo 正在安装依赖包...
pip install -r requirements.txt

echo.
echo 启动Flask应用...
cd flask
python app.py

pause
