# Agent Neuro - AI虚拟主播语音系统

个人尝试复刻AI虚拟主播neuro，集成Azure AI Speech Studio实现高质量文本转语音功能。

## 🎯 功能特性

- 🎤 **实时语音播放** - 输入文本立即转换并播放语音
- 💾 **语音文件下载** - 将转换的语音保存为WAV文件
- 🔊 **高质量语音** - 使用Azure AI Speech Studio的Ashley语音
- 🎵 **音高调节** - 预设1.25倍音高，声音更加生动
- 🌐 **现代化界面** - 响应式Web界面，支持桌面和移动设备
- ⚡ **实时状态监控** - 服务状态实时检测和错误提示

## 🛠️ 技术栈

- **后端**: Python Flask
- **前端**: HTML5 + CSS3 + JavaScript
- **语音服务**: Azure AI Speech Studio
- **音频格式**: WAV

## 📋 系统要求

- Python 3.7+
- Windows/Linux/macOS
- 稳定的网络连接（用于访问Azure服务）

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置服务

语音服务配置已预设在代码中：
- **语音角色**: Ashley (en-US-AshleyNeural)
- **音高**: +25% (1.25倍)
- **服务区域**: East Asia
- **终结点**: https://eastasia.api.cognitive.microsoft.com/

### 3. 启动应用

#### Windows用户
```bash
start.bat
```

#### 其他系统
```bash
cd flask
python app.py
```

### 4. 访问应用

打开浏览器访问：http://localhost:5000

## 📖 使用指南

### 基本操作

1. **输入文本** - 在文本框中输入要转换的英文内容
2. **实时播放** - 点击"🔊 实时播放语音"按钮直接播放
3. **下载文件** - 点击"💾 下载语音文件"按钮保存WAV文件
4. **测试服务** - 点击"🔍 测试服务状态"检查Azure服务连接

### 快捷键

- `Ctrl + Enter` - 快速播放语音

### 支持的文本格式

- 主要支持英文文本
- 支持标点符号和数字
- 建议单次输入文本长度不超过1000字符

## 🔧 API接口

### POST /api/speak
实时播放语音
```json
{
  "text": "要转换的文本内容"
}
```

### POST /api/download
下载语音文件
```json
{
  "text": "要转换的文本内容"
}
```

### GET /api/test
测试服务状态

## 📁 项目结构

```
agent_neuro/
├── flask/
│   ├── app.py              # Flask主应用
│   └── __pycache__/        # Python缓存文件
├── templates/
│   └── index.html          # 前端界面
├── neuro_video/
│   └── neuro.wav          # 音频资源
├── whitecatfree_vts/      # VTS模型资源
├── requirements.txt        # Python依赖
├── start.bat              # Windows启动脚本
├── README.md              # 项目说明
└── LICENSE                # 开源许可
```

## 🎛️ 配置说明

### Azure Speech服务配置
- **密钥**: 已配置在代码中
- **区域**: eastasia
- **终结点**: https://eastasia.api.cognitive.microsoft.com/
- **语音**: en-US-AshleyNeural
- **SSML音高**: +25%

### 环境变量（可选）
如需更安全的配置方式，可将敏感信息设置为环境变量：
```bash
export AZURE_SPEECH_KEY="your_speech_key"
export AZURE_SPEECH_REGION="eastasia"
```

## 🔍 故障排除

### 常见问题

1. **语音播放失败**
   - 检查网络连接
   - 确认Azure服务密钥有效
   - 查看控制台错误信息

2. **依赖安装失败**
   - 更新pip: `pip install --upgrade pip`
   - 使用国内镜像: `pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`

3. **端口冲突**
   - 修改app.py中的端口号
   - 或终止占用5000端口的其他程序

### 调试模式

启用调试模式获取详细错误信息：
```python
app.run(debug=True)
```

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进项目！

## 📄 开源许可

本项目遵循MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [Azure Cognitive Services](https://azure.microsoft.com/services/cognitive-services/)
- [Flask](https://flask.palletsprojects.com/)
- Neuro-sama 虚拟主播的灵感来源

---

🎭 **Agent Neuro** - 让AI虚拟主播的声音更加生动！
