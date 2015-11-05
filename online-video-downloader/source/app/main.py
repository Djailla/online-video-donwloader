#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os

from bottle import request, static_file, redirect, template, Bottle
from youtube import YoutubeDownloadProcess

ROOT_PATH = "/shares"
# ROOT_PATH = "/Users/gid509037/Perso/shares"

config = None
try:
    with open('/opt/youtube/.config') as f:
        config = json.load(f)
except:
    print 'Failed to load configuration'

app = Bottle()
dl_process = None


@app.route('/')
def main():
    global dl_process

    if dl_process is not None:
        if dl_process.is_alive():
            return template('progress')
        else:
            dl_process.join()
            dl_process = None

    path_list = ''.join('<option>%s</option>\n' % os.path.join(ROOT_PATH, folder)
                        for folder in os.listdir(ROOT_PATH)
                        if not folder.startswith('.'))
    print path_list

    return template('download', path_list=path_list)


@app.route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='./static/')


@app.route('/css/<filename>')
def server_css(filename):
    return static_file(filename, root='./static/css/')


@app.route('/css/fonts/<filename>')
def server_fonts(filename):
    return static_file(filename, root='./static/css/fonts/')


@app.route('/js/<filename>')
def server_js(filename):
    return static_file(filename, root='./static/js/')


@app.route('/img/<filename>')
def server_img(filename):
    return static_file(filename, root='./static/img/')


@app.get('/progress')
def progress():
    if dl_process is not None:
        return json.dumps({'progress': dl_process.progress,
                           'speed': dl_process.speed})
    else:
        return json.dumps({'progress': -1,
                           'speed': ''})


@app.error(404)
def error404(error):
    return template('result', title='Error 404 : Nothing to do here')


@app.post('/download')
def do_download():
    global dl_process

    dest_path = request.forms.get('dest_path')
    url = request.forms.get('url')

    if not os.path.isdir(dest_path):
        return template('result', title='Error', subtitle='The destination path "%s" is not valid' % dest_path)

    dl_process = YoutubeDownloadProcess()
    dl_process.dest_path = dest_path
    dl_process.url = url
    dl_process.start()

    return template('progress')


@app.get('/complete')
def complete():
    return template('result', title='Download complete', subtitle=dl_process.get_file_name())


@app.get('/dl_error')
def dl_error():
    if dl_process is not None:
        sub = dl_process.error
    else:
        sub = "Unknown error"

    return template('result', title='Error', subtitle=sub)


@app.get('/cancel')
def cancel():
    global dl_process

    if dl_process is not None:
        dl_process.stop()
        dl_process.join()
        dl_process = None

    redirect("/")


app.run(host='0.0.0.0', port=(config and config.get('port', 8080)) or 8080)
