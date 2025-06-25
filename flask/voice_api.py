import azure.cognitiveservices.speech as speechsdk
import os
import tempfile
import threading
import time
from datetime import datetime
from flask import jsonify, request, send_file
import re

# Azure Speech Service 配置
SPEECH_KEY = "24uT6bJ1GDcNiDgNuqObEL3DUdSIaSeiXylXZRA6sCVmxPdur9wQJQQJ99BFAC3pKaRXJ3w3AAAYACOGyCUc"
SPEECH_REGION = "eastasia"
SPEECH_ENDPOINT = "https://eastasia.api.cognitive.microsoft.com/"

# 过滤Emoji的函数
def remove_emojis(text):
    """移除文本中的emoji表情符号"""
    # emoji表情符号的Unicode范围
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F700-\U0001F77F"  # alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002702-\U000027B0"  # Dingbats
        "\U000024C2-\U0001F251"  # Enclosed characters
        "]+", 
        flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)

class SpeechService:
    def __init__(self):
        self.speech_config = speechsdk.SpeechConfig(
            subscription=SPEECH_KEY, 
            region=SPEECH_REGION
        )
        # 设置语音为Ashley，音高为1.25
        self.speech_config.speech_synthesis_voice_name = "en-US-AshleyNeural"
        
    def text_to_speech_file(self, text, output_file):
        """将文本转换为语音文件"""
        try:
            # 过滤emoji
            text = remove_emojis(text)
            
            # 创建音频配置
            audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file)
            
            # 创建语音合成器
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=self.speech_config, 
                audio_config=audio_config
            )
            
            # 使用SSML来设置音高
            ssml = f"""
            <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
                <voice name="en-US-AshleyNeural">
                    <prosody pitch="+25%">
                        {text}
                    </prosody>
                </voice>
            </speak>
            """
            
            # 合成语音
            result = synthesizer.speak_ssml_async(ssml).get()
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                return True, "语音合成成功"
            else:
                return False, f"语音合成失败: {result.reason}"
                
        except Exception as e:
            return False, f"错误: {str(e)}"
    
    def text_to_speech_stream(self, text):
        """将文本转换为语音流（实时播放）"""
        try:
            # 过滤emoji
            text = remove_emojis(text)
            
            # 创建默认音频输出配置（直接播放）
            audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
            
            # 创建语音合成器
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=self.speech_config, 
                audio_config=audio_config
            )
            
            # 使用SSML来设置音高
            ssml = f"""
            <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
                <voice name="en-US-AshleyNeural">
                    <prosody pitch="+25%">
                        {text}
                    </prosody>
                </voice>
            </speak>
            """
            
            # 合成并播放语音
            result = synthesizer.speak_ssml_async(ssml).get()
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                return True, "语音播放成功"
            else:
                return False, f"语音播放失败: {result.reason}"
                
        except Exception as e:
            return False, f"错误: {str(e)}"

# 创建语音服务实例
speech_service = SpeechService()

# 语音API路由函数
def speak():
    """文本转语音API - 实时播放"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'success': False, 'message': '请输入要转换的文本'})
        
        # 在后台线程中播放语音，避免阻塞请求
        def play_speech():
            speech_service.text_to_speech_stream(text)
        
        thread = threading.Thread(target=play_speech)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True, 
            'message': '开始播放语音',
            'text': text,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'服务器错误: {str(e)}'})

def download_speech():
    """文本转语音API - 下载文件"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'success': False, 'message': '请输入要转换的文本'})
        
        # 创建临时文件
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        temp_file.close()
        
        success, message = speech_service.text_to_speech_file(text, temp_file.name)
        
        if success:
            return send_file(
                temp_file.name,
                as_attachment=True,
                download_name=f'speech_{int(time.time())}.wav',
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

def test_service():
    """测试Azure Speech服务连接"""
    try:
        # 简单的连接测试
        test_text = "Hello, this is a test."
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        temp_file.close()
        
        success, message = speech_service.text_to_speech_file(test_text, temp_file.name)
        
        # 清理测试文件
        try:
            os.unlink(temp_file.name)
        except:
            pass
            
        return jsonify({
            'success': success,
            'message': message,
            'service': 'Azure Speech Service',
            'voice': 'en-US-AshleyNeural',
            'pitch': '+25%'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'服务测试失败: {str(e)}'}) 