#!/usr/bin/env python -*- coding: utf-8 -*-

import os
from multiprocessing import Process

import wmt_data 
from utils import parallelized_download, run_command

def download_wmt_monolingual(lang, maxp=5):
    langdir = 'wmt-data/mono/' + lang + '/'
    os.makedirs(langdir, exist_ok=True)
    os.chdir(langdir)
    _urls = wmt_data.monolingual[lang]
    parallelized_download('wget', _urls, max_processes=maxp)
    os.chdir('../../..')

def download_wmt_parallel(corpus_name):    
    corpusdir = 'wmt-data/parallel/' + corpus_name + '/'
    os.makedirs(corpusdir, exist_ok=True)
    os.chdir(corpusdir)
    url = wmt_data.parallel[corpus_name]
    parallelized_download('wget', [url])
    run_command('tar zxvf *.tgz')
    os.chdir('../../..')

def get_all_wmt_monolingual():
    for lang in wmt_data.monolingual:
        download_wmt_monolingual(lang)
    
def get_all_wmt_parallel():
    for corpus_name in wmt_data.parallel:    
        download_wmt_parallel(corpus_name)

def get_all_wmtdata():
    thread_mono = Process(target = get_all_wmt_monolingual).start()
    thread_para = Process(target = get_all_wmt_parallel).start()
    homedir = os.path.expanduser("~")
    run_command('mv wmt-data '+homedir)

if __name__ == '__main__':
    get_all_wmtdata()