#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os

from bottle import request, redirect, template
from youtube import YoutubeDownloadProcess
from default_app import app, parent_app, APPLICATION_ROOT


SHARES_ROOT_PATH = "/shares"
# SHARES_ROOT_PATH = "/Users/gid509037/Perso/shares"

config = None
try:
    with open('/opt/youtube/.config') as f:
        config = json.load(f)
except:
    print 'Failed to load configuration'

dl_process = None


@app.route('/')
@app.route('/index')
def main():
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
            if not folder.startswith('.'))
    except:
        path_list = '<option>No folder available</option>'

    return template('download', path_list=path_list)


@app.get('/progress')
def progress():
    if dl_process is not None:
        return json.dumps({'progress': dl_process.progress,
                           'speed': dl_process.speed})
    else:
        return json.dumps({'progress': -1,
                           'speed': ''})


@app.post('/download')
def do_download():
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
    return template(
        'result',
        title='Download complete',
        subtitle=dl_process.get_file_name(),
        dest_path=dl_process.dest_path
    )


@app.get('/dl_error')
def dl_error():
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
    global dl_process

    if dl_process is not None:
        dl_process.stop()
        dl_process.join()
        dl_process = None

    redirect("index")

parent_app.mount(APPLICATION_ROOT, app)
parent_app.run(host='0.0.0.0', port=(config and config.get('port', 8080)) or 8080)

# # DEBUG MODE
# import bottle
# bottle.debug(True)
# parent_app.run(host='0.0.0.0', port=(config and config.get('port', 8080)) or 8080, reloader=True)
