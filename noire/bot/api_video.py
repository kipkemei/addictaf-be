# -*- coding: utf-8 -*-
import copy
import json
import math
import os
import re
import shutil
import subprocess
import time

from django.conf import settings
from requests_toolbelt import MultipartEncoder


def downloadVideo(self, media_id, filename, media=False):
    if not media:
        self.mediaInfo(media_id)
        media = self.LastJson['items'][0]
    filename = '{0}_{1}.mp4'.format(media['user']['username'], media_id) if not filename else '{0}.mp4'.format(filename)
    try:
        clips = media['video_versions']
    except Exception:
        return False
    if os.path.exists(self.videosDir + filename):
        return os.path.abspath(self.videosDir + filename)
    # Download small video
    response = self.s.get(clips[-1]['url'], stream=True)
    if response.status_code == 200:
        with open(self.smVideosDir + filename, 'wb') as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f)
    # Download Hd video
    try:response = self.s.get(clips[1]['url'], stream=True)
    except KeyError: response = self.s.get(clips[1]['url'], stream=True)
    if response.status_code == 200:
        with open(self.videosDir + filename, 'wb') as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f)
        return os.path.abspath(self.videosDir + filename)

def getVideoInfo(filename):
    res = {}
    try:
        terminalResult = subprocess.Popen(["ffprobe", filename],
                                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for x in terminalResult.stdout.readlines():
            # Duration: 00:00:59.51, start: 0.000000, bitrate: 435 kb/s
            m = re.search(r'duration: (\d\d:\d\d:\d\d\.\d\d),', str(x), flags=re.IGNORECASE)
            if m is not None:
                res['duration'] = m.group(1)
            # Video: h264 (Constrained Baseline) (avc1 / 0x31637661), yuv420p, 480x268
            m = re.search(r'video:\s.*\s(\d+)x(\d+)\s', str(x), flags=re.IGNORECASE)
            if m is not None:
                res['width'] = m.group(1)
                res['height'] = m.group(2)
    finally:
        if 'width' not in res:
            print("ERROR: 'ffprobe' not found, pls install 'ffprobe' with one of following methods")
            print("   sudo apt-get install ffmpeg")
            print("or sudo apt-get install -y libav-tools")
    return res


def uploadVideo(self, video, thumbnail, caption=None, upload_id=None):
    print('a')
    if upload_id is None:
        upload_id = str(int(time.time() * 1000))
    data = {
        'upload_id': upload_id,
        '_csrftoken': self.token,
        'media_type': '2',
        '_uuid': self.uuid,
    }
    print('b')

    m = MultipartEncoder(data, boundary=self.uuid)
    self.s.headers.update({'X-IG-Capabilities': '3Q4=',
                                 'X-IG-Connection-Type': 'WIFI',
                                 'Host': 'i.instagram.com',
                                 'Cookie2': '$Version=1',
                                 'Accept-Language': 'en-US',
                                 'Accept-Encoding': 'gzip, deflate',
                                 'Content-type': m.content_type,
                                 'Connection': 'keep-alive',
                                 'User-Agent': settings.NOIRE['USER_AGENT']})
    print('c')

    response = self.s.post(settings.NOIRE['API_URL'] + "upload/video/", data=m.to_string())
    # print('d')

    if response.status_code == 200:
        body = json.loads(response.text)
        upload_url = body['video_upload_urls'][3]['url']
        upload_job = body['video_upload_urls'][3]['job']
        print('e')
        with open(video, 'rb') as video_bytes:
            videoData = video_bytes.read()
        print('f')
        # solve issue #85 TypeError: slice indices must be integers or None or have an __index__ method
        request_size = int(math.floor(len(videoData) / 4))
        lastRequestExtra = (len(videoData) - (request_size * 3))

        headers = copy.deepcopy(self.s.headers)
        self.s.headers.update({'X-IG-Capabilities': '3Q4=',
                                     'X-IG-Connection-Type': 'WIFI',
                                     'Cookie2': '$Version=1',
                                     'Accept-Language': 'en-US',
                                     'Accept-Encoding': 'gzip, deflate',
                                     'Content-type': 'application/octet-stream',
                                     'Session-ID': upload_id,
                                     'Connection': 'keep-alive',
                                     'Content-Disposition': 'attachment; filename="video.mov"',
                                     'job': upload_job,
                                     'Host': 'upload.instagram.com',
                                     'User-Agent': settings.NOIRE['USER_AGENT']})
        print('g')
        for i in range(0, 4):
            start = i * request_size
            if i == 3:
                end = i * request_size + lastRequestExtra
            else:
                end = (i + 1) * request_size
            length = lastRequestExtra if i == 3 else request_size
            print('h')
            content_range = "bytes {start}-{end}/{lenVideo}".format(start=start, end=(end - 1),
                                                                    lenVideo=len(videoData)).encode('utf-8')

            self.s.headers.update({'Content-Length': str(end - start), 'Content-Range': content_range, })
            print('h')

            response = self.s.post(upload_url, data=videoData[start:start + length])
            print('i')
        self.s.headers = headers

        if response.status_code == 200:
            print('j')
            if self.configureVideo(upload_id, video, thumbnail, caption):
                print('k')
                self.expose()
                print('l')
                return True
    return False


def configureVideo(self, upload_id, video, thumbnail, caption=''):
    clipInfo = getVideoInfo(video)
    self.uploadPhoto(photo=thumbnail, caption=caption, upload_id=upload_id)
    data = json.dumps({
        'upload_id': upload_id,
        'source_type': 3,
        'poster_frame_index': 0,
        'length': 0.00,
        'audio_muted': False,
        'filter_type': 0,
        'video_result': 'deprecated',
        'clips': {
            'length': clipInfo['duration'],
            'source_type': '3',
            'camera_position': 'back',
        },
        'extra': {
            'source_width': clipInfo['width'],
            'source_height': clipInfo['height'],
        },
        'device': settings.NOIRE['DEVICE_SETTINTS'],
        '_csrftoken': self.token,
        '_uuid': self.uuid,
        '_uid': self.user_id,
        'caption': caption,
    })
    return self.SendRequest('media/configure/?video=1', self.generateSignature(data))
