#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'cached_url'
import os
import sys
import hashlib
import requests
import re
import time

tmp_dir = 'tmp'

def getHeadRequestError(url, headers):
    response = requests.head(url, headers = headers, allow_redirects=True)
    if response.status_code != 200:
        return 'HTTP ' + str(response.status_code)
    try:
        size = int(response.headers.get('content-length', -1))
    except:
        size = -2
    if size > 50 * 1024 * 1024:
        return 'Too Large: %d MB' % int(size / 1024 / 1024)

def getUrlContent(url, headers={}, mode='', encoding='utf-8', sleep=0, no_early_error=False):
    headers['method'] = headers.get('method', 'GET')
    headers['accept'] = headers.get('accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/apng,*/*;q=0.8,application/signed-exchange;v=b3')
    headers['user-agent'] = headers.get('user-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36')
    time.sleep(sleep)

    if mode == 'b' and (not no_early_error):
        early_error = getHeadRequestError(url, headers)
        if early_error:
            return early_error

    with requests.get(url, headers=headers, stream=True) as r:
        if r.status_code != 200:
            return 'HTTP ' + str(r.status_code)

        if mode == 'b':  # for binary
            return r.content

        # for text
        accept_list = ['text', 'html', 'xml', 'json']
        if r.headers.get('content-type') and any(accept in r.headers['content-type'] for accept in accept_list):  # is webpage
            r.encoding = encoding
            return r.text

        return 'Not a webpage'

def getFileName(url):
    k = re.sub(r'\W+', '', url.strip('/').split('/')[-1].split('.')[0])[:8]
    h = hashlib.sha224(url.encode('utf-8')).hexdigest()[:15 - len(k)][:7]
    return k + '_' + h

def getFilePath(url):
    text = url
    for char in ['=', '&', ',']:
        text = text.replace(char, '.')
    text = text.split('?')[0]
    ext = os.path.splitext(text)[1] or '.html'
    if len(ext) > 10:
        ext = ext[0] + ext[-9:]
    return tmp_dir + '/' + getFileName(url) + ext

def cachedContent(url, headers={}, mode='', encoding='utf-8', sleep=0, ttl=float('inf'), no_early_error=False):
    cache = getFilePath(url)
    try:
        while os.path.getmtime(cache) > time.time() - 5:
            time.sleep(5) # for video file in saving
        if (ttl == float('inf') or 
            os.path.getmtime(cache) > time.time() - ttl):
            with open(cache, 'r' + mode) as f:
                return f.read()
    except:
        ...
    content = getUrlContent(url, headers, mode, encoding, sleep, no_early_error)
    os.system('mkdir -p %s > /dev/null 2>&1' % tmp_dir)
    with open(cache, 'w' + mode) as f:
        f.write(content)
    return content

def get(url, headers={}, force_cache=False, mode='', sleep=0, ttl=0, encoding='utf-8', no_early_error=False):
    if force_cache or 'test' in str(sys.argv):
        ttl = float('inf')
    if ttl != 0:
        return cachedContent(url, headers, mode, encoding, sleep, ttl, no_early_error)
    else:
        return getUrlContent(url, headers, mode, encoding, sleep)