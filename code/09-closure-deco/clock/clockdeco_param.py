# clockdeco_param.py

"""
>>> snooze(.1)  # doctest: +ELLIPSIS
[0.101...s] snooze(0.1) -> None
>>> clock('{name}: {elapsed}')(time.sleep)(.2)  # doctest: +ELLIPSIS
sleep: 0.20...
>>> clock('{name}({args}) dt={elapsed:0.3f}s')(time.sleep)(.2)
sleep(0.2) dt=0.201s
"""

# tag::CLOCKDECO_PARAM[]
import time

DEFAULT_FMT = '[{elapsed:0.8f}s] {name}({args}) -> {result}'  # <1>

def clock(fmt=DEFAULT_FMT):  # <2>
    def decorate(func):      # <3>
        def clocked(*_args): # <4>
            t0 = time.perf_counter()
            _result = func(*_args)  # <5>
            elapsed = time.perf_counter() - t0
            name = func.__name__
            args = ', '.join(repr(arg) for arg in _args)  # <6>
            result = repr(_result)  # <7>
            print(fmt.format(**locals()))  # <8>
            return _result  # <9>
        return clocked  # <10>
    return decorate  # <11>

if __name__ == '__main__':

    @clock()  # <12>
    def snooze(seconds):
        time.sleep(seconds)

    for i in range(3):
        snooze(.123)

# end::CLOCKDECO_PARAM[]
