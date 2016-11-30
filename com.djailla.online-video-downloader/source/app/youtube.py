#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import humanize
import os
import youtube_dl

from threading import Thread, Event


class YoutubeDownloadThread(Thread):
    video_file_name = ''
    progress = 0
    speed = ''
    size = ''
    error = ''

    @property
    def file_name(self):
        return os.path.basename(self.video_file_name)

    def __init__(self, url, dest_path, subs):
        super(YoutubeDownloadThread, self).__init__()
        self.url = url
        self.dest_path = dest_path
        self.subs = subs
        self._stop = Event()

    def run(self):
        def my_hook(d):
            current_status = d['status']
            if current_status == 'downloading':
                self.video_file_name = d.get('filename')

                if d.get('speed'):
                    self.speed = "%s/s" % humanize.naturalsize(d.get('speed'))
                if d.get('total_bytes'):
                    self.progress = (
                        float(d.get('downloaded_bytes')) /
                        float(d.get('total_bytes')) *
                        100
                    )

                # print('Downloading in progress ...')
                # print("--", self.video_file_name)
                # print("--", self.speed)
                # print("--", self.progress)
            elif current_status == 'finished':
                self.progress = 100
                self.speed = '0 b/s'
            elif current_status == 'error':
                self.error = "Aie aie aie"

        ydl_opts = {
            'allsubtitles': self.subs,
            'progress_hooks': [my_hook],
            'nocheckcertificate': True,
            'outtmpl': self.dest_path + '/' + "%(title)s.%(ext)s"
        }
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
        except Exception as exc:
            self.error = str(exc)

    def stop(self):
        self._stop.set()
