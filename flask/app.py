from flask import Flask, render_template
import os
from voice_api import speak, download_speech, test_service
from llm_api import chat_completion, chat_stream
from combined_api import text_to_speech_stream, text_to_speech_download

app = Flask(__name__, template_folder='../templates')

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/chat')
def chat():
    """聊天页面"""
    return render_template('chat.html')

@app.route('/combined')
def combined():
    """文本语音结合页面"""
    return render_template('combined.html')

@app.route('/api/speak', methods=['POST'])
def api_speak():
    """文本转语音API - 实时播放"""
    return speak()

@app.route('/api/download', methods=['POST'])
def api_download():
    """文本转语音API - 下载文件"""
    return download_speech()

@app.route('/api/test', methods=['GET'])
def api_test():
    """测试Azure Speech服务连接"""
    return test_service()

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """通义千问API - 普通文本输入"""
    return chat_completion()

@app.route('/api/chat/stream', methods=['POST'])
def api_chat_stream():
    """通义千问API - 流式输出"""
    return chat_stream()

@app.route('/api/combined/speak', methods=['POST'])
def api_combined_speak():
    """结合API - 文本输入到语音输出(播放)"""
    return text_to_speech_stream()

@app.route('/api/combined/download', methods=['POST'])
def api_combined_download():
    """结合API - 文本输入到语音输出(下载)"""
    return text_to_speech_download()

if __name__ == '__main__':
    print("启动 Agent Neuro 语音服务...")
    print("访问 http://localhost:5000 来使用服务")
    app.run(debug=True, host='0.0.0.0', port=5000)
