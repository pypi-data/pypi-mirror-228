import base64
import os
from io import BytesIO
from pydub import AudioSegment
import streamlit as st
from audio_recorder_streamlit import audio_recorder
import openai
import json
import requests

openaikey = os.getenv("openai_api_key")
API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

def r_t(wavename,openaikey):
    audio_bytes = audio_recorder(
        text="点击麦克风图标以开始录音", energy_threshold=4000, pause_threshold=10.0
    )

    if audio_bytes:
        st.audio(data=audio_bytes, format="audio/wav")
        audio_file_path = wavename
        with open(audio_file_path, "wb") as f:
            f.write(audio_bytes)

        openai.api_key = openaikey

        openai.proxy = {
            "http": "http://192.168.32.17:7890",
            "https": "http://192.168.32.17:7890"
        }

        try:
            with open(audio_file_path, "rb") as f:
                response = openai.Audio.transcribe("whisper-1", f)
                result = response["text"]
                st.write(result)

            return audio_file_path, result
        except Exception as e:
            result = {"error": str(e)}
            st.write(result)
            return None, str(e)

    return None, "没有录到音频"


# audio_file_path, transcript = r_and_t("1.wav")

#if audio_file_path:
#    st.write(f"录音文件路径：{audio_file_path}")
#    st.write(f"最终识别的文本：{transcript}")
#else:
#    st.write(transcript)




API_URL = "https://inscode-api.csdn.net/api/v1/gpt/"
INSCODE_API_KEY = os.getenv("INSCODE_API_KEY")

def s_q(prompt, question):
    body = {
        "messages": [{"role": "user", "content": prompt + question}],
        "apikey": INSCODE_API_KEY,
    }
    response = requests.post(API_URL, json=body)
    
    if response.status_code == 200:
        if response.text:
            try:
                response_parts = response.text.strip().split("\n")[:-1]
                full_response = ""
                for part in response_parts:
                    if part.startswith("data:"):
                        json_part = json.loads(part[5:])
                        content = json_part["choices"][0]["delta"].get("content", "")
                        full_response += content
                return full_response
            except json.JSONDecodeError as e:
                print("Unable to parse JSON-formatted data returned by the API:")
                print(response.text)
                print("Error details:", str(e))
                return None
        else:
            print("The API did not return any results.")
            return None
    else:
        print("Error:", response.status_code, response.text)
        return None






def ocr(image, api_key, secret_key):
    """
    调用百度OCR API识别图片中的文字
    :param image: 图片的二进制数据
    :param api_key: 百度API的API key
    :param secret_key: 百度API的Secret key
    :return: 识别结果
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": api_key, "client_secret": secret_key}
    response = requests.post(url, params=params)

    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        return None
    
    access_token = response.json().get("access_token")

    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'image': base64.b64encode(image).decode(), "access_token": access_token}
    response = requests.post(url, headers=headers, data=data)

    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        return None

    result = json.loads(response.text)
    if 'words_result' in result and result['words_result']:
        text = '\n'.join([w['words'] for w in result['words_result']])
        return text
    else:
        return "无法识别图片文字"


