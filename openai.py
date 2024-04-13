import aiohttp
import asyncio
import aiofiles
import base64
import requests
import json
import cv2
import numpy as np
from config import *


async def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


async def fetch_openai_completion(prompt, question):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": f"You are a helpful assistant.\n\n"
                           f"{prompt}\n\n",
            },
            {
                "role": "user",
                "content": f"{question}"
            }
        ]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=json.dumps(data)) as response:
            if response.status == 200:
                response_json = await response.json()
                return response_json['choices'][0]['message']['content']
            else:
                raise Exception(f"API Request failed with status code {response.status}")
                return "Technical problems, please try again later."


async def download_image(url, file_path_down):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                async with aiofiles.open(file_path_down, 'wb') as f:
                    content = await response.read()
                    await f.write(content)


async def img_openai_generation(prompt):
    url = "https://api.openai.com/v1/images/generations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }
    data = {
        "model": "dall-e-3",
        "prompt": f"{prompt}",
        "n": 1,
        "size": "1024x1024"
  }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=json.dumps(data)) as response:
            try:
                if response.status == 200:
                    response_json = await response.json()
                    img_describe = response_json['data'][0]['revised_prompt']
                    img_url = response_json['data'][0]['url']
                    img_name = img_url.replace('https://', '/').split('/')[5].split('?')[0]
                    file_path_down = image_dir_path + img_name
                    await download_image(img_url, file_path_down)
                    return img_describe, img_name
                else:
                    return "Technical problems, please try again later.", 'error.png'
            except:
                return "Technical problems, please try again later.", 'error.png'


async def image_to_text_openai(file_path):
    base64_image = await encode_image(file_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What’s in this image?"

                    },
                    {
                        "type": "image_url",
                        "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }
    async with aiohttp.ClientSession() as session:
        async with session.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload) as response:
            if response.status == 200:
                response_json = await response.json()
                img_description = response_json['choices'][0]['message']['content']
                return img_description
