from flask import request, jsonify
import threading
import tempfile
import os
import time
from datetime import datetime

# 导入语音服务和文本模型
from voice_api import speech_service
from llm_api import client, MODEL
from prompt_api import get_system_prompt

def text_to_speech_stream():
    """
    从文本模型到语音服务的结合API - 实时流式处理
    文本输入 -> 文本模型生成回复 -> 语音合成并播放
    """
    try:
        data = request.get_json()
        messages = data.get('messages', [])
        
        if not messages:
            return jsonify({'success': False, 'message': '请输入有效的消息内容'})
            
        # 强制使用Neuro-sama的系统提示词
        messages = [msg for msg in messages if msg.get('role') != 'system']
        messages.insert(0, {'role': 'system', 'content': get_system_prompt()})
        
        # 调用通义千问API获取文本回复
        completion = client.chat.completions.create(
            model=MODEL,
            messages=messages,
        )
        
        # 获取AI回复文本
        ai_response = completion.choices[0].message.content
        
        # 在后台线程中播放语音，避免阻塞请求
        def play_speech():
            speech_service.text_to_speech_stream(ai_response)
        
        thread = threading.Thread(target=play_speech)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True, 
            'text': ai_response,
            'message': '正在播放AI回复的语音',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'服务器错误: {str(e)}'})

def text_to_speech_download():
    """
    从文本模型到语音服务的结合API - 下载音频文件
    文本输入 -> 文本模型生成回复 -> 语音合成并下载
    """
    try:
        ai_response = request.args.get('text')
        if not ai_response:
             # 尝试从JSON中获取数据
            data = request.get_json()
            if data and 'messages' in data:
                messages = data.get('messages', [])
            else:
                return jsonify({'success': False, 'message': '未找到有效的文本内容'})
            
            if not messages:
                return jsonify({'success': False, 'message': '请输入有效的消息内容'})

            # 强制使用Neuro-sama的系统提示词
            messages = [msg for msg in messages if msg.get('role') != 'system']
            messages.insert(0, {'role': 'system', 'content': get_system_prompt()})
            
            # 调用通义千问API获取文本回复
            completion = client.chat.completions.create(
                model=MODEL,
                messages=messages,
            )
            # 获取AI回复文本
            ai_response = completion.choices[0].message.content
        
        # 创建临时文件
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        temp_file.close()
        
        # 将文本转换为语音文件
        success, message = speech_service.text_to_speech_file(ai_response, temp_file.name)
        
        if success:
            from flask import send_file
            return send_file(
                temp_file.name,
                as_attachment=True,
                download_name=f'ai_speech_{int(time.time())}.wav',
                mimetype='audio/wav'
            )
        else:
            # 清理临时文件
            try:
                os.unlink(temp_file.name)
            except:
                pass
            return jsonify({'success': False, 'message': message})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'服务器错误: {str(e)}'}) 