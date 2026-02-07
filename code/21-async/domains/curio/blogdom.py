#!/usr/bin/env python3
from keyword import kwlist
import curio

MAX_KEYWORD_LEN = 4

async def probe(domain: str) -> tuple[str, bool]:  # <1>
    try:
        await curio.socket.getaddrinfo(domain, None)  # <2>
    except curio.socket.gaierror:
        return (domain, False)
    return (domain, True)

async def main() -> None:
    names = (kw for kw in kwlist if len(kw) <= MAX_KEYWORD_LEN)
    domains = (f'{name}.dev'.lower() for name in names)
    async with curio.TaskGroup() as group:  # <3>
        for domain in domains:
            await group.spawn(probe, domain)  # <4>
        async for task in group:  # <5>
            domain, found = task.result
            mark = '+' if found else ' '
            print(f'{mark} {domain}')

if __name__ == '__main__':
    curio.run(main())  # <6>
