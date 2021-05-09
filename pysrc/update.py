#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os.path import basename
from os.path import join as path_join
from time import sleep
from requests import get
from libavctl import send_reload
from config import AV_SOURCES, CHECK_FOR_UPDATES, DB_PATH, UPDATE_FREQ

FIFO_PATH = '/tmp/cobra.sock'

def main() -> None:
    for i in AV_SOURCES:
        r = get(i, allow_redirects=True)
        with open(path_join(DB_PATH, basename(i)), 'wb') as f:
            f.write(r.content)
    send_reload()
    print('Sent reload signal to daemon')


if __name__ == '__main__':
    if CHECK_FOR_UPDATES:
        main()
    else:
        print('Updates disabled. Exiting.')
        exit()
    print(f'Sleeping {UPDATE_FREQ.pprint()}', flush=True)
    try:
        sleep(int(UPDATE_FREQ))
    except KeyboardInterrupt:
        print('Shutting down')
