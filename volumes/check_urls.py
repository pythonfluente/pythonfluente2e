#!/usr/bin/env python3

import fileinput
import asyncio
import httpx
import sys

async def check_url(client: httpx.AsyncClient, start_url: str) -> tuple[str, int, str]:
    req = client.build_request("GET", start_url)
    status = 0
    end_url = '?'
    while req is not None:
        end_url = req.url
        try:
            resp = await client.send(req)
            status = resp.status_code
        except httpx.HTTPError as e:
            print(e)
            print('URL:', req.url)
            status = -1
            break
        req = resp.next_request

    return end_url, status, start_url 


async def main() -> None:
    urls = sorted({u for l in fileinput.input() if (u := l.strip())})
    async with httpx.AsyncClient() as client:
        tasks = [check_url(client, url) for url in urls]
        async for task in asyncio.as_completed(tasks):
            url, status, starting_url = await task
            if url != starting_url:
                print(status, url)
                print('was', starting_url)
            elif status != 200:
                print(status, url)

if __name__ == "__main__":
    asyncio.run(main())