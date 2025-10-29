# COEIROINKv2-Galgame-texts-bridge
A bridge program written by python for connecting the Japanese visual novel engine and COEIROINKv2 AI voice generation

[日本語版はこちら](./README-ja.md)  
[English version here](./README-en.md)

# COEIROINK v2 Python连接程序 

这是一个专为Galgame的「テキスト読み上げ機能」（文本朗读功能）设计的Python连接程序。它通过调用COEIROINK v2的API，将游戏中的文本实时转换为高质量的语音WAV文件。

当然，除了Galgame，你也可以将它用于任何需要通过命令行进行文本转语音的场景。

## 🎮 Galgame文本朗读功能设置指南
我在贴吧写了一个详细的无脑中文教程可以试试按照这个教程一步步去设置哦
https://tieba.baidu.com/p/10167834101

要在支持外部程序调用的Galgame中使用本程序，请按照以下步骤设置：

1.  在Galgame的设置中，找到「外部アプリケーション呼び出し」（外部应用程序调用）选项。
2.  在「外部アプリケーション呼び出し」字段，填入你的Python解释器的完整路径。例如：
    ```
    C:\Python39\python.exe
    ```
3.  在「音声パラメータ」（音声设置）字段，填入以下格式的参数：

    ```bash
    path/to/get_audio.py -t "%t" -o "%f" --speaker-uuid "d219f5ab-a50b-4d99-a26a-xxxxxxxx" --style-id xx --speed-scale xx
    ```

    *   将 `path/to/get_audio.py` 替换为你本机 `get_audio.py` 脚本的实际路径。
    *   将 `d219f5ab-a50b-4d99-a26a-xxxxxxxx` 替换为你想要使用的话者UUID。
    *   将 `xx` 替换为对应的风格ID、语速等参数值。
    *   `%t` 会被游戏自动替换为当前需要朗读的文本。
    *   `%f` 会被游戏自动替换为期望输出的WAV文件路径。

## ⚠️ 重要注意事项

**请务必仔细阅读以下内容，以确保程序正常工作：**

*   **语言要求：** 本程序依赖COEIROINK v2进行语音合成，而COEIROINK v2主要针对日语进行优化。因此，**务必使用游戏的日语原版**才能正确合成音频。
*   **汉化补丁：** **不支持任何翻译补丁**。因为翻译补丁通常会修改游戏内部的文本编码或内容，导致程序无法正确识别和传递文本给API。
*   **Steam双语版：** 如果你在Steam上玩支持双语切换的Galgame，**必须将游戏的主语言设置为日语**，否则文本朗读功能将无法正常工作。

## 📦 准备工作

1.  **安装Python**：确保你的系统已安装Python 3.6或更高版本。
2.  **安装依赖库**：
    ```bash
    pip install requests
    ```
3.  **运行COEIROINK v2**：在使用本脚本前，请确保COEIROINK v2应用程序已经在后台启动并运行（默认监听 `http://127.0.0.1:50032`）。

## 📖 详细用法与参数说明

### 基本用法

```bash
python get_audio.py -t "こんにちは" -o "hello.wav"
```

### 所有参数详解

下表列出了所有可用的命令行参数、它们的默认值以及详细说明。

| 参数 | 简写 | 类型 | 默认值 | 说明 |
|---|---|---|---|---|
| `--text` | `-t` | str | (必需) | 要合成的文本内容 (合成するテキスト) |
| `--output` | `-o` | str | (必需) | 输出WAV文件的路径 (出力WAVファイルのパス) |
| `--speaker-uuid` | | str | `3c37646f-3881-5374-2a83-149267990abc` | 话者的唯一标识符 (話者のUUID)。默认为つくよみちゃん |
| `--style-id` | | int | `0` | 话者的风格ID (話者のスタイルID) |
| `--speed-scale` | | float | `1.0` | 语速缩放比例。大于1.0更快，小于1.0更慢 (話速スケール) |
| `--pitch-scale` | | float | `0.0` | 音调缩放比例。大于0.0更高，小于0.0更低 (ピッチスケール) |
| `--intonation-scale` | | float | `1.0` | 语调起伏的强度。大于1.0更夸张，小于1.0更平淡 (イントネーションスケール) |
| `--volume-scale` | | float | `1.0` | 音量缩放比例 (音量スケール) |
| `--pre-phoneme-length` | | float | `0.1` | 音频开始前的无声时间（秒） (音声開始前の無音時間) |
| `--post-phoneme-length` | | float | `0.5` | 音频结束后的无声时间（秒） (音声終了後の無音時間) |
| `--output-sampling-rate` | | int | `24000` | 输出音频的采样率 (出力音声のサンプリングレート) |
| `--api-url` | | str | `http://127.0.0.1:50032/` | COEIROINK v2 API的地址 (COEIROINK v2 APIのURL) |
| `--list-speakers` | | | (无) | 显示所有可用的话者列表及其UUID和风格ID (利用可能な話者一覧を表示) |

### 使用示例

1.  **查看所有可用话者**：
    ```bash
    python get_audio.py --list-speakers
    ```

2.  **使用指定话者和参数合成语音**：
    ```bash
    python get_audio.py -t "これはテストです" -o "test.wav" --speaker-uuid "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" --style-id 2 --speed-scale 1.2 --pitch-scale 0.1
    ```

## 🔍 如何获取话者UUID和风格ID？

你可以通过以下三种方式获取：

1.  **使用本脚本**：运行 `python get_audio.py --list-speakers` 命令，程序会打印出所有可用的话者信息。
2.  **查看COEIROINK安装目录**：在 `COEIROINK_WIN_xxx\speaker_info\对应话者文件夹\metas.json` 文件中可以找到 `speakerUuid` 和 `styles` 下的 `styleId`。
3.  **访问API文档**：在COEIROINK v2运行时，用浏览器访问 `http://127.0.0.1:50032/docs` 可以查看交互式API文档。

## 📝 创作背景与致谢

我是 [https://tieba.baidu.com/p/8436241968?pid=147727092459#147727092459](https://tieba.baidu.com/p/8436241968?pid=147727092459#147727092459) 的作者。

我参考了 [https://blog.csdn.net/Sunlightqwq/article/details/141789130](https://blog.csdn.net/Sunlightqwq/article/details/141789130) 这对我启发很大。但发现原方案主要针对VOICEVOX API或无法直接连接到COEIROINK v2且设置参数较少，所以用AI制作了这个版本。

---
