# NightMic 🎤
> 深夜游戏无声开麦神器 | 文字转语音虚拟麦克风工具

专为深夜、宿舍、安静环境下的游戏玩家打造，无需真实开麦，打字即可语音沟通。
玩家打造输入文字 → 实时转语音 → 虚拟麦克风输出极简、快捷、不打扰任何人

[![Windows](https://img.shields.io/badge/OS-Windows-blue.svg)](https://github.com/)
[![Python](https://img.shields.io/badge/Python-3.x-green.svg)](https://python.org/)
[![TTS](https://img.shields.io/badge/Voice-SAPI5-orange.svg)](https://github.com/)

---

## ✨ 功能亮点
- 🚀 **全局编辑框一键呼出 / 发送**，全屏游戏中也可秒开秒用，无需切窗口，输入完成自动发送并隐藏。
- 🎯 **自定义快捷键 + 播报内容**，支持单键与组合键配置，报点、指挥、提醒一键播报，响应迅速。
- 🔇 **完全静音操作**，全程无需开口发声，不打扰家人、室友与邻居，安静开黑 / 沟通。
- 🎮 **极简悬浮窗口**，半透明置顶，可拖动不挡屏。
- 📁 **外置 JSON 配置**，所有快捷键、播报文本均可通过配置文件自由修改，重启即生效。
- 🔗 **VB-Cable 虚拟麦克风**，全游戏/语音软件兼容
- 🛡️ **本地离线运行**，文字不联网，保护隐私
- 🚀 **轻量后台运行**，资源占用低，不卡顿游戏，稳定无冲突。

---

## 🚀 快速使用 
### 1. 安装虚拟声卡（必须）
下载并安装 **VB-Cable**：
https://vb-audio.com/Cable/
安装后 **重启电脑** 生效。

### 2. 下载并Releases版本并解压压缩包
https://github.com/coderSC0TT/night-mic/releases/tag/v1.1

### 3. 自定义配置与游戏内设置
在exe文件同级目录下config.json中可自定义快捷键以及快捷呼出内容。
将系统/游戏/语音软件的 麦克风选择为：CABLE Output

### 4. 运行exe文件
运行exe文件，先回车（默认）呼出聊天框后进入游戏可保证游戏时输入框聚焦成功，无需鼠标操作。





## ⚡ 如需DIY-源代码构建
### 1.克隆或下载此仓库到本地 确保你的 Python 版本在 3.8 及以上
### 2.安装必要的 Python 库：pip install sounddevice numpy pyttsx3 keyboard
### 3.运行程序main.py
