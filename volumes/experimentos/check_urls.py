#!/usr/bin/env python3

import fileinput
import asyncio
import httpx
import sys

from typing import NamedTuple


class StatusURL(NamedTuple):
    status: int
    url: str
    exception: Exception | None = None


async def check_url(client: httpx.AsyncClient, start_url: str) -> list[StatusURL]:
    req = client.build_request("GET", start_url)
    results = []
    while req is not None:
        try:
            http_resp = await client.send(req)
            result = StatusURL(http_resp.status_code, req.url)
        except httpx.HTTPError as e:
            result = StatusURL(0, req.url, e)
        else:
            req = http_resp.next_request
        results.append(result)

    assert len(results) > 0, 'NO results: ' + start_url
    return results


async def main() -> None:
    urls = sorted({u for l in fileinput.input() if (u := l.strip())})
    async with httpx.AsyncClient() as client:
        tasks = [check_url(client, url) for url in urls]
        async for task in asyncio.as_completed(tasks):
            results = await task
            for n, result in enumerate(results):
                url = str(result.url)[:70]
                print(f'{" "*4*n}{result.status} {url}')

if __name__ == "__main__":
    asyncio.run(main())