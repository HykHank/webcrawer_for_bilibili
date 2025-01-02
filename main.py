import requests

import re

import json

import os

from moviepy.editor import VideoFileClip, AudioFileClip\


class Crawl:
    __url = 'https://www.bilibili.com'
    __headers = {
                    'User-Agent':'Mozilla/50(Windows NT 11.0; win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
                    'referer':__url,
                    'Cookie':""
                }
        
    def get_json(self):
        url = self.__url
        headers = self.__headers
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print('error')
    def get_video(self,url):
        headers = self.__headers
        for i in urls:
            url = i
            response = requests.get(url=url, headers=headers)
            html = response.text
            title = re.findall('title="(.*?)"', html)[0]
            print(title)

            info = re.findall('window.__playinfo__=(.*?)</script>', html)[0]
            json_data = json.loads(info)

            video_url = json_data['data']['dash']['video'][0]['baseUrl']
            print(video_url)

            audio_url = json_data['data']['dash']['audio'][0]['baseUrl']
            print(audio_url)
            video_content = requests.get(url=video_url, headers=headers).content

            audio_content = requests.get(url=audio_url, headers=headers).content
            title = re.sub(r'[^\u4e00-\u9fff\u3040-\u30ff\u31f0-\u31ff\w\s]', '', title)

            with open('video\\' + '[画]' + title + '.mp4', mode='wb') as v:
                v.write(video_content)
            with open('video\\' + '[音]' + title + '.mp3', mode='wb') as a:
                a.write(audio_content)
            video = VideoFileClip('video\\' + '[画]' + title + '.mp4')
            audio = AudioFileClip('video\\' + '[音]' + title + '.mp3')
            video_with_audio = video.set_audio(audio)
            video_with_audio.write_videofile('video\\' + '[音画]' + title + '.mp4', codec="libx264")
if __name__ == '__main__':
    bvid = input('请输入视频BV号,如有多个请用逗号分隔\n').split(',')
    urls = []
    c = Crawl()
    for i in bvid:
        video_url = 'https://www.bilibili.com/video/'+i
        print('即将提取的视频链接为:',video_url)
        urls.append(video_url)
    comp = re.compile('[^A-Z^a-z^0-9^\u4e00-\u9fa5]')
    print('开始提取')
    c.get_video(video_url)