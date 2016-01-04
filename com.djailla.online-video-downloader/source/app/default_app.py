#!/usr/bin/python
# -*- coding: utf-8 -*-
from bottle import static_file, redirect, template, Bottle

parent_app = Bottle()
app = Bottle()
APPLICATION_ROOT = '/apps/online-video-downloader/'


@parent_app.route('/')
@parent_app.route(APPLICATION_ROOT[:-1])
def parent_default():
    redirect(APPLICATION_ROOT)


@parent_app.error(404)
def parent_404(error):
    return template('result', title='Error 404 : Nothing to do here')


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


@app.error(404)
def error404(error):
    return template('result', title='Error 404 : Nothing to do here')
