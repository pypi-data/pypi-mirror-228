from youtube_transcript_api import YouTubeTranscriptApi
from videolab_youtube_crawler.CrawlerObject import _CrawlerObject
import pandas as pd
from configparser import ConfigParser
import json
import os
import asyncio

NUMERR_FLAG = -1
STRERR_FLAG = "unknown"

CONFIG = "config.ini"
config = ConfigParser(allow_no_value=True)
config.read(CONFIG)


class SubtitleCrawler(_CrawlerObject):

    def crawl_subtitles_in_list(self, **kwargs):
        filename = kwargs.get("videos_to_collect", f"DATA/list_video.csv")
        video_id = kwargs.get("video_id", "videoId")
        save_dir = self.data_subtitle_json
        core = kwargs.get("core", 8)

        if not os.path.exists(save_dir):
            os.mkdir(save_dir)

        df = pd.read_csv(filename)
        asyncio.run(self._start_crawling(df, video_id, save_dir, core))

    async def _start_crawling(self, df, video_id, save_dir, core):
        coros = []
        for vid in df[video_id]:
            if not os.path.exists(save_dir + vid[1:] + ".json"):
                print(f"crawling subtitle: {vid[1:]}")
                coros.append(asyncio.gather(self._get_subscription(vid, save_dir)))
                if len(coros) % core == 0:
                    await asyncio.gather(*coros)
                    coros = []

            else:
                print(f'Subtitle {vid} crawled skipped')
        if len(coros) > 0:
            await asyncio.gather(*coros)

    async def _get_subscription(self, vid, save_dir):
        transcript = self._crawl(vid[1:])
        if transcript:
            with open(save_dir + vid[1:] + ".json", 'w+') as fp:
                fp.write(json.dumps(transcript) + "\n")
            print(f'Subtitle {vid} crawled')
        else:
            print(f'Subtitle {vid} crawled failed')

    def _crawl(self, vid):
        try:
            transcript = YouTubeTranscriptApi.get_transcript(vid)
            return transcript
        except:
            return None
