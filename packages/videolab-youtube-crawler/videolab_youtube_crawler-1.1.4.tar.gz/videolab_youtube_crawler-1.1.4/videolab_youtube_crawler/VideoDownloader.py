import asyncio
import os
from concurrent.futures import ProcessPoolExecutor

import pandas as pd
from yt_dlp import YoutubeDL

from videolab_youtube_crawler.CrawlerObject import _CrawlerObject

# choco install ffmpeg

"""Download MP4 file from YouTube"""


class VideoDownloader(_CrawlerObject):

    def __init__(self):
        self.failed_videos_due_to_unavailability = []
        self.failed_without_reason = []
        self.PPE = ProcessPoolExecutor()
        super().__init__()

    def download_videos_in_list(self, video_list_workfile=f"DATA/list_video.csv", audio=False, **kwargs):
        """
        Download MP4 file from the list_video workfile
        :param audio:
        :param video_list_workfile: File to process
        :param kwargs:
        :return:
        """
        qual = kwargs.get('quality', 'worst')
        if qual == 'worst':
            self.quality = 'wv+wa'
        else:
            self.quality = 'bv+ba'
        core = kwargs.get("core", 5)
        batch=kwargs.get("batch", 10)
        video_column = kwargs.get('video_id', 'videoId')
        self.video_data_dir = kwargs.get('video_data_dir', self.data_video_stream)
        df = pd.read_csv(video_list_workfile)
        video_list = list(df[video_column])
        asyncio.run(self._download_video_list(video_list, self.video_data_dir, audio, core, batch))

    async def _download_video_list(self, video_list, video_data_dir, audio, core, batch=10):
        vids = [[]]
        for video_id in video_list:
            vid = video_id[1:]
            dir1 = f"{video_data_dir}/{vid}/{vid}.mp4"
            dir2 = f"{video_data_dir}/{vid}/{vid}.mp4.mkv"
            if not self._isCrawled(dir1) and not self._isCrawled(dir2):
                print(f"Crawling a video mp4 for {vid}....")
                try:
                    os.mkdir(f"{video_data_dir}/{vid}")
                    pass
                except OSError:
                    pass
                if len(vids[-1]) == batch:
                    vids.append([])
                vids[-1].append(vid)
            else:
                print(f"Skip {vid}, video stream already crawled")
            if len(vids) == core and len(vids[-1]) == batch:
                await self._download_list_async(vids, video_data_dir, audio)
                vids = [[]]
        for b in vids:
            if len(b) > 0:
                await self._download_list_async([b], video_data_dir, audio)

    async def _download_list_async(self, sublist, video_data_dir, audio):
        URLs = [[f'https://www.youtube.com/watch?v={video_id}' for video_id in batch] for batch in sublist]
        ydl_opts = {
            'format': self.quality,
            'progress_hooks': [my_hook],
            'throttled-rate': '2000K',
            'outtmpl': f'{video_data_dir}/%(id)s/%(id)s.mp4'
        }
        if audio:
            ydl_opts['keepvideo'] = True
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        try:
            loop = asyncio.get_event_loop()
            futs = [loop.run_in_executor(None, YoutubeDL(ydl_opts).download, url) for url in URLs]
            await asyncio.gather(*futs)
        except:
            print('Video collect failed', URLs)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now post-processing ...')
