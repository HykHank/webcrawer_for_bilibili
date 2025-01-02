import requests  
import re  
import json 
import os  
from moviepy.editor import VideoFileClip, AudioFileClip  


class Crawl:
    def __init__(self, cookies):
        # 初始化类时，设置基础URL和请求头
        __url = 'https://www.bilibili.com'  # B站首页地址
        __headers = {
            'User-Agent': 'Mozilla/50(Windows NT 11.0; win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
            'referer': __url,  # 引用页面为B站首页
            'Cookie': cookies  # 用户提供的Cookie，用于身份验证
        }
        self.__url = __url
        self.__headers = __headers


    # 获取B站首页的JSON响应
    def get_json(self):
        url = self.__url
        headers = self.__headers
        response = requests.get(url, headers=headers)  # 发送GET请求
        if response.status_code == 200:  # 如果请求成功
            return response.json()  # 返回JSON数据
        else:
            print('error')  # 请求失败时输出错误信息


    # 下载并处理视频和音频
    def get_video(self, url):
        headers = self.__headers
        for i in urls:
            url = i  # 遍历所有提供的视频URL
            response = requests.get(url=url, headers=headers)  # 获取视频页面HTML
            html = response.text

            # 使用正则表达式提取视频标题
            title = re.findall('title="(.*?)"', html)[0]
            print(title)  # 打印标题

            # 提取视频和音频信息的JSON数据
            info = re.findall('window.__playinfo__=(.*?)</script>', html)[0]
            json_data = json.loads(info)

            # 获取视频和音频的下载地址
            video_url = json_data['data']['dash']['video'][0]['baseUrl']
            print(video_url)

            audio_url = json_data['data']['dash']['audio'][0]['baseUrl']
            print(audio_url)

            # 下载视频内容
            video_content = requests.get(url=video_url, headers=headers).content

            # 下载音频内容
            audio_content = requests.get(url=audio_url, headers=headers).content

            # 清理标题中的非法字符
            title = re.sub(r'[^一-鿿぀-ヿㇰ-ㇿ\w\s]', '', title)

            # 保存视频文件
            with open('video\\' + '[画]' + title + '.mp4', mode='wb') as v:
                v.write(video_content)

            # 保存音频文件
            with open('video\\' + '[音]' + title + '.mp3', mode='wb') as a:
                a.write(audio_content)

            # 合并音视频
            video = VideoFileClip('video\\' + '[画]' + title + '.mp4')
            audio = AudioFileClip('video\\' + '[音]' + title + '.mp3')
            video_with_audio = video.set_audio(audio)
            video_with_audio.write_videofile('video\\' + '[音画]' + title + '.mp4', codec="libx264")



# 主程序入口
if __name__ == '__main__':
    # 输入B站视频的BV号
    bvid = input('请输入视频BV号,如有多个请用逗号分隔\n').split(',')
    urls = []  # 用于存储视频URL

    # 读取Cookie文件
    with open('cookie.txt', 'r') as cookie:
        cookies = cookie.read()

    # 创建Crawl实例
    c = Crawl(cookies)

    # 为每个BV号生成完整的URL
    for i in bvid:
        video_url = 'https://www.bilibili.com/video/' + i
        print('即将提取的视频链接为:', video_url)
        urls.append(video_url)

    # 开始提取视频
    print('开始提取')
    c.get_video(video_url)
