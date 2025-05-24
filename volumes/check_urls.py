#!/usr/bin/env python3

import fileinput
import asyncio
import httpx
import sys

from typing import NamedTuple

class StatusURL(NamedTuple):
    status: int
    url: str

async def check_url(client: httpx.AsyncClient, start_url: str) -> list[StatusURL]:
    req = client.build_request("GET", start_url)
    responses = []
    while req is not None:
        try:
            http_resp = await client.send(req)
            response = StatusURL(http_resp.status_code, req.url)
        except httpx.HTTPError as e:
            print(e)
            print('URL:', req.url)
            status = -1
            break
        else:
            responses.append(response)
        req = http_resp.next_request
    assert len(responses) > 0, 'NO RESPONSES: ' + start_url
    return responses


async def main() -> None:
    urls = sorted({u for l in fileinput.input() if (u := l.strip())})
    async with httpx.AsyncClient() as client:
        tasks = [check_url(client, url) for url in urls]
        async for task in asyncio.as_completed(tasks):
            status_urls = await task
            for n, status_url in enumerate(status_urls):
                url = str(status_url.url)[:70]
                print(f'{" "*4*n}{status_url.status} {url}')

if __name__ == "__main__":
    asyncio.run(main())