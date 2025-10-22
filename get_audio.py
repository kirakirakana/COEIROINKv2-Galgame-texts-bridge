#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COEIROINK v2 API连接程序
通过命令行参数生成语音WAV文件
"""

import argparse
import json
import requests
import sys
import os
from urllib.parse import urljoin

def get_speakers(api_base_url):
    """获取可用话者列表"""
    try:
        response = requests.get(urljoin(api_base_url, "v1/speakers"))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"获取话者列表失败: {e}")
        return None

def synthesize_speech(api_base_url, text, output_file, speaker_uuid, style_id=0, 
                     speed_scale=1.0, pitch_scale=0.0, intonation_scale=1.0,
                     volume_scale=1.0, pre_phoneme_length=0.1, 
                     post_phoneme_length=0.5, output_sampling_rate=24000):
    """
    使用COEIROINK v2 API合成语音
    
    参数:
        api_base_url: COEIROINK API基础URL
        text: 要合成的文本
        output_file: 输出WAV文件路径
        speaker_uuid: 话者UUID
        style_id: 风格ID (默认0)
        speed_scale: 语速缩放 (默认1.0)
        pitch_scale: 音调缩放 (默认0.0)
        intonation_scale: 语调缩放 (默认1.0)
        volume_scale: 音量缩放 (默认1.0)
        pre_phoneme_length: 前音素长度 (默认0.1)
        post_phoneme_length: 后音素长度 (默认0.5)
        output_sampling_rate: 输出采样率 (默认24000)
    """
    # 构建请求体
    query = {
        "speakerUuid": speaker_uuid,
        "styleId": style_id,
        "text": text,
        "speedScale": speed_scale,
        "volumeScale": volume_scale,
        "prosodyDetail": [],
        "pitchScale": pitch_scale,
        "intonationScale": intonation_scale,
        "prePhonemeLength": pre_phoneme_length,
        "postPhonemeLength": post_phoneme_length,
        "outputSamplingRate": output_sampling_rate,
    }
    
    try:
        # 发送合成请求
        response = requests.post(
            urljoin(api_base_url, "v1/synthesis"),
            headers={"Content-Type": "application/json"},
            data=json.dumps(query),
        )
        response.raise_for_status()
        
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
        
        # 保存WAV文件
        with open(output_file, "wb") as f:
            f.write(response.content)
        
        print(f"语音文件已生成: {output_file}")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"API请求失败: {e}")
        return False
    except Exception as e:
        print(f"保存文件失败: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="COEIROINK v2 语音合成工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python get_audio.py -t "你好世界" -o "output.wav"
  python get_audio.py -t "こんにちは" -o "greeting.wav" --speaker-uuid "3c37646f-3881-5374-2a83-149267990abc" --speed-scale 1.2
  python get_audio.py --list-speakers
        """
    )
    
    # 基本参数
    parser.add_argument("-t", "--text", required=False, help="要合成的文本")
    parser.add_argument("-o", "--output", required=False, help="输出WAV文件路径")
    
    # 话者参数
    parser.add_argument("--speaker-uuid", default="3c37646f-3881-5374-2a83-149267990abc", 
                       help="话者UUID (默认: つくよみちゃん)")
    parser.add_argument("--style-id", type=int, default=0, 
                       help="风格ID (默认: 0)")
    
    # 语音参数
    parser.add_argument("--speed-scale", type=float, default=1.0, 
                       help="语速缩放 (默认: 1.0)")
    parser.add_argument("--pitch-scale", type=float, default=0.0, 
                       help="音调缩放 (默认: 0.0)")
    parser.add_argument("--intonation-scale", type=float, default=1.0, 
                       help="语调缩放 (默认: 1.0)")
    parser.add_argument("--volume-scale", type=float, default=1.0, 
                       help="音量缩放 (默认: 1.0)")
    parser.add_argument("--pre-phoneme-length", type=float, default=0.1, 
                       help="前音素长度 (默认: 0.1)")
    parser.add_argument("--post-phoneme-length", type=float, default=0.5, 
                       help="后音素长度 (默认: 0.5)")
    parser.add_argument("--output-sampling-rate", type=int, default=24000, 
                       help="输出采样率 (默认: 24000)")
    
    # API配置
    parser.add_argument("--api-url", default="http://127.0.0.1:50032/", 
                       help="COEIROINK API URL (默认: http://127.0.0.1:50032/)")
    
    # 工具命令
    parser.add_argument("--list-speakers", action="store_true", 
                       help="列出所有可用话者")
    
    args = parser.parse_args()
    
    # 列出话者
    if args.list_speakers:
        speakers = get_speakers(args.api_url)
        if speakers:
            print("可用话者:")
            for speaker in speakers:
                styles = ", ".join([f"{style['styleName']}(ID:{style['styleId']})" 
                                  for style in speaker.get('styles', [])])
                print(f"  {speaker['speakerName']} (UUID: {speaker['speakerUuid']})")
                print(f"    风格: {styles}")
        return
    
    # 检查必需参数
    if not args.text or not args.output:
        parser.error("必须指定 -t/--text 和 -o/--output 参数，或使用 --list-speakers 查看可用话者")
    
    # 执行语音合成
    success = synthesize_speech(
        api_base_url=args.api_url,
        text=args.text,
        output_file=args.output,
        speaker_uuid=args.speaker_uuid,
        style_id=args.style_id,
        speed_scale=args.speed_scale,
        pitch_scale=args.pitch_scale,
        intonation_scale=args.intonation_scale,
        volume_scale=args.volume_scale,
        pre_phoneme_length=args.pre_phoneme_length,
        post_phoneme_length=args.post_phoneme_length,
        output_sampling_rate=args.output_sampling_rate
    )
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()