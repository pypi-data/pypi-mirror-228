import modal.functions
import typing
import typing_extensions

T = typing.TypeVar("T")

class ClsMixin:
    @classmethod
    def remote(cls: typing.Type[T], *args, **kwargs) -> T:
        ...

    @classmethod
    async def aio_remote(cls: typing.Type[T], *args, **kwargs) -> T:
        ...


def check_picklability(key, arg):
    ...


class _Obj:
    _functions: typing.Dict[str, modal.functions._Function]
    _has_local_obj: bool
    _local_obj: typing.Any
    _local_obj_constr: typing.Callable[[], typing.Any]

    def __init__(self, user_cls: type, base_functions: typing.Dict[str, modal.functions._Function], args, kwargs):
        ...

    def get_local_obj(self):
        ...

    def __getattr__(self, k):
        ...


class Obj:
    _functions: typing.Dict[str, modal.functions.Function]
    _has_local_obj: bool
    _local_obj: typing.Any
    _local_obj_constr: typing.Callable[[], typing.Any]

    def __init__(self, user_cls: type, base_functions: typing.Dict[str, modal.functions.Function], args, kwargs):
        ...

    def get_local_obj(self):
        ...

    def __getattr__(self, k):
        ...


class _Cls:
    _user_cls: type
    _functions: typing.Dict[str, modal.functions._Function]

    def __init__(self, user_cls, base_functions: typing.Dict[str, modal.functions._Function]):
        ...

    def get_user_cls(self):
        ...

    def get_base_function(self, k: str) -> modal.functions._Function:
        ...

    def __call__(self, *args, **kwargs) -> _Obj:
        ...

    async def remote(self, *args, **kwargs) -> _Obj:
        ...

    def __getattr__(self, k):
        ...


class Cls:
    _user_cls: type
    _functions: typing.Dict[str, modal.functions.Function]

    def __init__(self, user_cls, base_functions: typing.Dict[str, modal.functions.Function]):
        ...

    def get_user_cls(self):
        ...

    def get_base_function(self, k: str) -> modal.functions.Function:
        ...

    def __call__(self, *args, **kwargs) -> Obj:
        ...

    class __remote_spec(typing_extensions.Protocol):
        def __call__(self, *args, **kwargs) -> Obj:
            ...

        async def aio(self, *args, **kwargs) -> Obj:
            ...

    remote: __remote_spec

    def __getattr__(self, k):
        ...
