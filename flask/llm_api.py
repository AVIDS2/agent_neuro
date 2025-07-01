from flask import request, jsonify
from openai import OpenAI
from prompt_api import get_system_prompt, get_complete_prompt

# 通义千问配置
API_KEY = "sk-3b21b83ea5044298a708d0c706292db1"
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
MODEL = "qwen-turbo-latest"

# 创建OpenAI客户端
client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)

def chat_completion():
    """调用通义千问模型API - 普通文本输入"""
    try:
        data = request.get_json()
        messages = data.get('messages', [])
        
        if not messages:
            return jsonify({'success': False, 'message': '请输入有效的消息内容'})
        
        # 强制使用Neuro-sama的系统提示词
        messages = [msg for msg in messages if msg.get('role') != 'system']
        messages.insert(0, {'role': 'system', 'content': get_system_prompt()})
        
        # 调用通义千问API
        completion = client.chat.completions.create(
            model=MODEL,
            messages=messages,
        )
        
        # 返回结果
        return jsonify({
            'success': True,
            'data': completion.model_dump(),
            'timestamp': completion.created
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'API调用错误: {str(e)}'})

def chat_stream():
    """调用通义千问模型API - 流式输出"""
    try:
        data = request.get_json()
        messages = data.get('messages', [])
        
        if not messages:
            return jsonify({'success': False, 'message': '请输入有效的消息内容'})
        
        # 强制使用Neuro-sama的系统提示词
        messages = [msg for msg in messages if msg.get('role') != 'system']
        messages.insert(0, {'role': 'system', 'content': get_system_prompt()})
        
        # 调用通义千问API（流式）
        def generate():
            completion = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                stream=True,
                stream_options={"include_usage": True}
            )
            
            for chunk in completion:
                yield f"data: {chunk.model_dump_json()}\n\n"
                
        return generate(), {'Content-Type': 'text/event-stream'}
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'API调用错误: {str(e)}'})

def get_neuro_persona():
    """返回Neuro-sama的完整人格设定"""
    return jsonify(get_complete_prompt()) 