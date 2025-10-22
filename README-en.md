# COEIROINKv2-Galgame-texts-bridge
A bridge program written in Python for connecting Japanese visual novel engines and COEIROINKv2 AI voice generation.

# COEIROINK v2 Python Bridge Program

This is a Python bridge program designed for the "Text-to-Speech" feature in Galgames. It calls the COEIROINK v2 API to convert in-game text into high-quality speech WAV files in real time.

Of course, besides Galgames, you can use it in any scenario where text-to-speech is required via the command line.

## 🎮 Guide to Setting Up Text-to-Speech in Galgames

To use this program in Galgames that support external program calls, follow these steps:

1. In the Galgame settings, find the "External Application Call" option.
2. In the "External Application Call" field, enter the full path to your Python interpreter. For example:
    ```
    C:\Python39\python.exe
    ```
3. In the "Voice Parameters" field, enter the parameters in the following format:

    ```bash
    path/to/get_audio.py -t "%t" -o "%f" --speaker-uuid "d219f5ab-a50b-4d99-a26a-xxxxxxxx" --style-id xx --speed-scale xx
    ```

    * Replace `path/to/get_audio.py` with the actual path to the `get_audio.py` script on your machine.
    * Replace `d219f5ab-a50b-4d99-a26a-xxxxxxxx` with the UUID of the speaker you want to use.
    * Replace `xx` with the corresponding style ID, speed, and other parameter values.
    * `%t` will be automatically replaced by the game with the text to be read aloud.
    * `%f` will be automatically replaced by the game with the desired output WAV file path.

## ⚠️ Important Notes

**Please carefully read the following to ensure the program works correctly:**

* **Language Requirement:** This program relies on COEIROINK v2 for voice synthesis, which is optimized for Japanese. Therefore, **you must use the Japanese version of the game** to correctly synthesize audio.
* **Translation Patches:** **Translation patches are not supported.** Translation patches often modify the game's internal text encoding or content, causing the program to fail to recognize and pass the text to the API.
* **Steam Bilingual Version:** If you are playing a bilingual Galgame on Steam, **you must set the game's primary language to Japanese**, or the text-to-speech feature will not work properly.

## 📦 Preparation

1. **Install Python:** Ensure Python 3.6 or higher is installed on your system.
2. **Install Required Libraries:**
    ```bash
    pip install requests
    ```
3. **Run COEIROINK v2:** Before using this script, ensure the COEIROINK v2 application is running in the background (default listening on `http://127.0.0.1:50032`).

## 📖 Detailed Usage and Parameter Description

### Basic Usage

```bash
python get_audio.py -t "こんにちは" -o "hello.wav"
```

### Detailed Explanation of All Parameters

The table below lists all available command-line parameters, their default values, and detailed descriptions.

| Parameter | Short | Type | Default | Description |
|---|---|---|---|---|
| `--text` | `-t` | str | (Required) | The text to synthesize |
| `--output` | `-o` | str | (Required) | Path to the output WAV file |
| `--speaker-uuid` | | str | `3c37646f-3881-5374-2a83-149267990abc` | Unique identifier of the speaker. Default is Tsukuyomi-chan |
| `--style-id` | | int | `0` | Style ID of the speaker |
| `--speed-scale` | | float | `1.0` | Speed scale. Greater than 1.0 is faster, less than 1.0 is slower |
| `--pitch-scale` | | float | `0.0` | Pitch scale. Greater than 0.0 is higher, less than 0.0 is lower |
| `--intonation-scale` | | float | `1.0` | Intonation scale. Greater than 1.0 is more exaggerated, less than 1.0 is flatter |
| `--volume-scale` | | float | `1.0` | Volume scale |
| `--pre-phoneme-length` | | float | `0.1` | Silent time (seconds) before audio starts |
| `--post-phoneme-length` | | float | `0.5` | Silent time (seconds) after audio ends |
| `--output-sampling-rate` | | int | `24000` | Sampling rate of the output audio |
| `--api-url` | | str | `http://127.0.0.1:50032/` | URL of the COEIROINK v2 API |
| `--list-speakers` | | | (None) | Display a list of all available speakers, their UUIDs, and style IDs |

### Examples

1. **View All Available Speakers:**
    ```bash
    python get_audio.py --list-speakers
    ```

2. **Synthesize Speech with Specific Speaker and Parameters:**
    ```bash
    python get_audio.py -t "This is a test" -o "test.wav" --speaker-uuid "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" --style-id 2 --speed-scale 1.2 --pitch-scale 0.1
    ```

## 🔍 How to Get Speaker UUID and Style ID?

You can obtain them in the following ways:

1. **Using This Script:** Run the `python get_audio.py --list-speakers` command, and the program will print all available speaker information.
2. **Check the COEIROINK Installation Directory:** In the `COEIROINK_WIN_xxx\speaker_info\corresponding_speaker_folder\metas.json` file, you can find `speakerUuid` and `styleId` under `styles`.
3. **Access the API Documentation:** When COEIROINK v2 is running, visit `http://127.0.0.1:50032/docs` in your browser to view the interactive API documentation.

## 📝 Background and Acknowledgments

I am the author of [this post](https://tieba.baidu.com/p/8436241968?pid=147727092459#147727092459).

I was inspired by [this blog](https://blog.csdn.net/Sunlightqwq/article/details/141789130). However, I found the original solution mainly targeted VOICEVOX API or lacked direct connection to COEIROINK v2 with limited parameter settings, so I created this version using AI.
