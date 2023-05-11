import functools
import tracemalloc
from collections.abc import Callable
from time import perf_counter
from typing import Any, Union

from .modules.view import View


def checking(_func: Union[Callable, None] = None, *,
             arguments: bool = False, result: bool = False):
    """This decorator count func time and memory"""
    def check(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            args_list = [str(x) for x in args]
            args_list.extend(f'{k}={v}' for k, v in kwargs.items())
            tracemalloc.start()
            t0 = perf_counter()
            _res = func(*args, **kwargs)
            view = View(args_list, name=func.__name__, time=perf_counter()-t0,
                        amount=tracemalloc.get_traced_memory()[-1],
                        func_res=_res)
            view.setup(chk_result=result, chk_arguments=arguments)
            view.show()
            tracemalloc.stop()
            return _res
        return wrapper
    return check(_func) if _func else check
    
