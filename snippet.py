# -*- coding: utf-8 -*-
import argparse
import json
import requests
import os
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

URL_BASE = ''
TOKEN = ''
VISIBLE_LEVEL = 'private'

def status(args):
    h = Handler()
    h.snippet_checker()

def post(args):
    title = ''
    description = ''
    if args.t:
        title = args.t
    if args.m:
        description = args.m
    if os.path.isabs(args.f):
        path = args.f
    else:
        path = os.path.join(os.getcwd(), args.f)
    h = Handler()
    h.set_config(path, title, description)
    h.upload()

def get(args):
    path = os.getcwd()
    if not args.f:
        args.f = ''
    if os.path.isabs(args.f):
        path = args.f
    else:
        path = os.path.join(os.getcwd(), args.f)
    h = Handler()
    h.download(check_parse_url(args.s_id), path)

def put(args):
    title = ''
    description = ''
    if args.t:
        title = args.t
    if args.m:
        description = args.m
    if os.path.isabs(args.f):
        path = args.f
    else:
        path = os.path.join(os.getcwd(), args.f)
    h = Handler()
    h.set_config(path, title, description)
    h.update(check_parse_url(args.s_id))

def delete(args):
    h = Handler()
    h.delete(check_parse_url(args.s_id))

def check_return_code(r, code=200):
    if r.status_code != code:
        raise RuntimeError('response error: ' + str(r.status_code) + '\n' + str(r.reason))

def check_parse_url(url):
    if url.isdigit():
        return url
    else:
        return url.strip('/').split('/')[-1]

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='commands')

    list_parser = subparsers.add_parser('status', help='List snippets you owned')
    list_parser.set_defaults(func=status)

    upload_parser = subparsers.add_parser('push', help='Upload snippet')
    upload_parser.add_argument('f', type=str, action='store', help='source file path')
    upload_parser.add_argument('-t', type=str, action='store', help='snippet title')
    upload_parser.add_argument('-m', type=str, action='store', help='snippet description')
    upload_parser.set_defaults(func=post)

    download_parser = subparsers.add_parser('pull', help='Download snippet')
    download_parser.add_argument('s_id', action='store', type=str, help='source snippet id')
    download_parser.add_argument('-f', type=str, action='store', help='destinate file path')
    download_parser.set_defaults(func=get)

    update_parser = subparsers.add_parser('update', help='Update snippet')
    update_parser.add_argument('s_id', action='store', type=str, help='destinate snippet id')
    update_parser.add_argument('f', type=str, action='store', help='source file path')
    update_parser.add_argument('-t', type=str, action='store', help='snippet title')
    update_parser.add_argument('-m', type=str, action='store', help='snippet description')
    update_parser.set_defaults(func=put)

    delete_parser = subparsers.add_parser('rm', help='Remove snippet')
    delete_parser.add_argument('s_id', action='store', type=str, help='destinate snippet id')
    delete_parser.set_defaults(func=delete)

    try:
        args = parser.parse_args()
        args.func(args)
    except RuntimeError as e:
        print(e)


class Handler:

    def __init__(self):
        self.API_BASE = URL_BASE + '/api/v4'
        self.URL_BASE = URL_BASE
        self.HEADERS = {
            'Private-Token': TOKEN,
            'Content-Type': 'application/json'
        }

    def snippet_checker(self):
        url = self.API_BASE + '/snippets'
        r = requests.get(url, headers=self.HEADERS, timeout=30)
        check_return_code(r, 200)
        r = r.json()
        if len(r) == 0:
            print('no snippets found')
        else:
            for snippet in r:
                print(snippet['web_url'] + '\t' + snippet['file_name'])

    def upload(self):
        url = self.API_BASE + '/snippets'
        r = requests.post(url, headers=self.HEADERS, data=json.dumps(self.config), timeout=30)
        check_return_code(r, 201)
        r = r.json()
        print(r['web_url'])

    def update(self, s_id):
        url = self.API_BASE + '/snippets/' + str(s_id)
        r = requests.put(url, headers=self.HEADERS, data=json.dumps(self.config), timeout=30)
        check_return_code(r)
        r = r.json()
        print(r['web_url'])

    def delete(self, s_id):
        url = self.API_BASE + '/snippets/' + str(s_id)
        r = requests.delete(url, headers=self.HEADERS, timeout=30)
        check_return_code(r, 204)

    def download(self, s_id, file_path):
        if os.path.isdir(file_path):
            url = self.URL_BASE + '/snippets/' + str(s_id)
            r = requests.get(url, headers=self.HEADERS, timeout=30)
            check_return_code(r)
            r = r.text
            title = re.search('file-title-name(.*?)<', r, re.S)
            file_path = os.path.join(file_path, title.group().split('\n')[1])
        url = self.URL_BASE + '/snippets/' + str(s_id) + '/raw'
        r = requests.get(url, headers=self.HEADERS, timeout=30)
        check_return_code(r)
        with open(file_path, 'w') as file:
            file.write(r.text)
        print('file_path: ' + file_path)

    def set_config(self, file_path, title, description):
        filename = os.path.basename(file_path)
        if title == '':
            title = filename
        with open(file_path, 'r') as file:
            content = file.read()
        self.config = {
            'title': title,
            'file_name': filename,
            'content': content,
            'visibility': VISIBLE_LEVEL
        }
        if description != '':
            self.config['description'] = description


if __name__ == '__main__':
    main()
