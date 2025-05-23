#!/usr/bin/env python3

import fileinput
import asyncio
from urllib.parse import urlparse
from http.client import HTTPSConnection, HTTPConnection
from typing import Tuple

async def check_url(url: str) -> Tuple[str, int]:
    u = urlparse(url)
    hostname = u.hostname or ''
    port = u.port
    path = u.path or '/'
    cnx_type = HTTPSConnection if u.scheme == 'https' else HTTPConnection
    cnx = cnx_type(hostname, port)
    try:
        await asyncio.to_thread(cnx.request, 'GET', path)
        resp = await asyncio.to_thread(cnx.getresponse)
    except OSError as e:
        print(e)
        print('URL:', url)
        status = -1
    else:
        status = resp.status
    cnx.close()
    
    return url, status


async def main() -> None:
    urls = sorted({u for l in fileinput.input() if (u := l.strip())})
    tasks = [check_url(url) for url in urls]
    async for task in asyncio.as_completed(tasks):
        url, status = await task
        if status != 200:
            print(status, url)


if __name__ == "__main__":
    asyncio.run(main())