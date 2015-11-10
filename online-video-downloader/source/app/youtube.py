#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re

from subprocess import Popen, PIPE, STDOUT
from threading import Thread


class YoutubeDownloadProcess(Thread):
    url = ''
    dest_path = ''
    subs = False
    video_file_name = ''

    progress = 0
    process = None
    speed = ''
    size = ''
    error = ''

    def get_file_name(self):
        return os.path.basename(self.video_file_name)

    def run(self):
        cmd = [
            "youtube-dl",
            self.url,
            "-o", self.dest_path.rstrip('/') + '/' + "%(title)s.%(ext)s",
            "--newline",
            "--no-check-certificate"
        ]
        if self.subs:
            cmd.append('--all-subs')

        self.process = Popen(cmd, stdout=PIPE, stderr=STDOUT)

        while 1:
            line = self.process.stdout.readline()
            if not line:
                break

            download_str = re.match(r'\[download\] (.*)', line)
            if download_str:
                already = re.match(r'\[download\] (.*) has already been downloaded', line)
                if already:
                    self.video_file_name = already.group(1)
                    self.progress = 100

                destination = re.match(r'\[download\] Destination: (.*)', line)
                if destination:
                    self.video_file_name = destination.group(1)

                progress = re.match(r'\[download\] (.*)% of (.*) at (.*) ETA (.*)', line)
                if progress:
                    self.progress = float(progress.group(1))
                    self.speed = progress.group(3)
                    if not self.size:
                        self.size = progress.group(2)

            error_str = re.match(r'ERROR: (.*); please report (.*)', line)
            if error_str:
                self.progress = -1
                self.error = error_str.group(1)
                break

        return

    def stop(self):
        if self.process is not None:
            self.process.kill()
