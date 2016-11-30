#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This is the main file for the bottle based web interface
of the Online Video Downloader
"""

import bottle
import json
import logging
import os
import platform

from bottle import request, redirect, template
from youtube import YoutubeDownloadProcess
from default_app import app, parent_app, APPLICATION_ROOT

LOGGER_FORMAT = '[%(asctime)-15s] - {%(levelname)s} - %(message)s'
logging.basicConfig(format=LOGGER_FORMAT, level=logging.DEBUG)

# Check if running of my Mac for dev
if platform.system() == 'Darwin':
    bottle.debug(True)
    SHARES_ROOT_PATH = "/Users/gid509037/Perso/shares"
else:
    SHARES_ROOT_PATH = "/shares"

RAINBOW_CONFIG_FILE = '/opt/youtube/.config'
RAINBOW_CONFIG = None
try:
    with open(RAINBOW_CONFIG_FILE) as f:
        RAINBOW_CONFIG = json.load(f)
except IOError:
    logging.warning(
        'Failed to load configuration file (%s)',
        RAINBOW_CONFIG_FILE
    )

dl_process = None


@app.route('/')
@app.route('/index')
def main():
    """Main loop of the web interface"""
    global dl_process

    if dl_process is not None:
        if dl_process.is_alive():
            return template('progress')
        else:
            dl_process.join()
            dl_process = None

    try:
        path_list = ''.join(
            '<option>%s</option>\n' % os.path.join(SHARES_ROOT_PATH, folder)
            for folder in os.listdir(SHARES_ROOT_PATH)
            if not folder.startswith('.')
        )
    except:
        path_list = '<option>No folder available</option>'

    return template('download', path_list=path_list)


@app.get('/progress')
def progress():
    """Display the progress of video download"""
    if dl_process is not None:
        return json.dumps({'progress': dl_process.progress,
                           'speed': dl_process.speed})
    else:
        return json.dumps({'progress': -1,
                           'speed': ''})


@app.post('/download')
def do_download():
    """Start the video download"""
    global dl_process

    try:
        dest_path = request.forms.get('dest_path')
        url = request.forms.get('url')
        subs = request.forms.get('subs')

        if not os.path.isdir(dest_path):
            return template(
                'result',
                title='Error',
                subtitle='The destination path "%s" is not valid' % dest_path
            )

        dl_process = YoutubeDownloadProcess()
        dl_process.dest_path = dest_path
        dl_process.subs = subs
        dl_process.url = url
        dl_process.start()

        return template('progress')
    except:
        return template(
            'error',
            title='Error',
            subtitle='Unexpected error'
        )


@app.get('/complete')
def complete():
    """URL to display the success page"""
    return template(
        'result',
        title='Download complete',
        subtitle=dl_process.file_name,
        dest_path=dl_process.dest_path
    )


@app.get('/dl_error')
def dl_error():
    """URL to display an error page"""
    if dl_process is not None:
        sub = dl_process.error
    else:
        sub = "Unknown error"

    return template(
        'error',
        title='Error',
        subtitle=sub
    )


@app.get('/cancel')
def cancel():
    """Cancel the current action"""
    global dl_process

    if dl_process is not None:
        dl_process.stop()
        dl_process.join()
        dl_process = None

    redirect("index")

parent_app.mount(APPLICATION_ROOT, app)
parent_app.run(
    host='0.0.0.0',
    port=(RAINBOW_CONFIG and RAINBOW_CONFIG.get('port', 8080)) or 8080,
    reloader=(platform.system() == 'Darwin')
)
