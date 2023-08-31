import inspect
from functools import wraps

from curio.meta import from_coroutine


def awaitableClassMethod(syncfunc):
    """
    Decorator that allows an asynchronous function to be paired with a
    synchronous function in a single function call.  The selection of
    which function executes depends on the calling context.  For example:

        def spam(sock, maxbytes):                       (A)
            return sock.recv(maxbytes)

        @awaitable(spam)                                (B)
        async def spam(sock, maxbytes):
            return await sock.recv(maxbytes)

    In later code, you could use the spam() function in either a synchronous
    or asynchronous context.  For example:

        def foo():
            ...
            r = spam(s, 1024)          # Calls synchronous function (A) above
            ...

        async def bar():
            ...
            r = await spam(s, 1024)    # Calls async function (B) above
            ...

    """

    def decorate(asyncfunc):
        @wraps(asyncfunc)
        def wrapper(cls, *args, **kwargs):
            if from_coroutine():
                return asyncfunc(cls, *args, **kwargs)
            else:
                return syncfunc(cls, *args, **kwargs)

        wrapper._syncfunc = syncfunc
        wrapper._asyncfunc = asyncfunc
        wrapper._awaitable = True
        wrapper.__doc__ = syncfunc.__doc__ or asyncfunc.__doc__
        return wrapper

    return decorate
