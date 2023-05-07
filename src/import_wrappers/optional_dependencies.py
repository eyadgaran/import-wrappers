"""
Wrappers to support optional dependencies
"""
import importlib
import logging
import re
import types
from typing import Any, Optional

LOGGER = logging.getLogger(__name__)


class MissingDependencyMeta(type):
    """
    Use a metaclass to manage attributes of uninitialized MissingDependency objects
    """

    def __repr__(self):
        return f"Missing Dependency Wrapper for {self.import_path} (`pip install {self.pypi_name}` or `pip install {self.host_pypi_name}[{self.extra_group}]`)"

    def __getattr__(self, attr):
        """
        Recursively return Wrappers until a method is actually called
        """
        import_path = f"{self.import_path}.{attr}"
        LOGGER.debug(
            f"Recursively wrapping {attr} attribute of missing import {self.import_path}"
        )
        return types.new_class(
            name=import_path.replace(".", "_").replace(":", "_"),
            bases=(MissingDependency,),
            kwds={
                "metaclass": MissingDependencyMeta,
            },
            exec_body=lambda ns: ns.update(
                {
                    "import_path": import_path,
                    "pypi_name": self.pypi_name,
                    "host_pypi_name": self.host_pypi_name,
                    "extra_group": self.extra_group,
                }
            ),
        )

    def __bool__(self):
        self.raise_error()

    # comparisons
    def __lt__(self, *args, **kwargs):
        self.raise_error()

    def __le__(self, *args, **kwargs):
        self.raise_error()

    def __eq__(self, *args, **kwargs):
        self.raise_error()

    def __ne__(self, *args, **kwargs):
        self.raise_error()

    def __gt__(self, *args, **kwargs):
        self.raise_error()

    def __ge__(self, *args, **kwargs):
        self.raise_error()

    # membership
    def __contains__(self, *args, **kwargs):
        self.raise_error()

    # arithmetic
    def __add__(self, *args, **kwargs):
        self.raise_error()

    def __radd__(self, *args, **kwargs):
        self.raise_error()

    def __iadd__(self, *args, **kwargs):
        self.raise_error()

    def __sub__(self, *args, **kwargs):
        self.raise_error()

    def __rsub__(self, *args, **kwargs):
        self.raise_error()

    def __isub__(self, *args, **kwargs):
        self.raise_error()

    def __mul__(self, *args, **kwargs):
        self.raise_error()

    def __rmul__(self, *args, **kwargs):
        self.raise_error()

    def __imul__(self, *args, **kwargs):
        self.raise_error()

    def __matmul__(self, *args, **kwargs):
        self.raise_error()

    def __rmatmul__(self, *args, **kwargs):
        self.raise_error()

    def __imatmul__(self, *args, **kwargs):
        self.raise_error()

    def __truediv__(self, *args, **kwargs):
        self.raise_error()

    def __rtruediv__(self, *args, **kwargs):
        self.raise_error()

    def __itruediv__(self, *args, **kwargs):
        self.raise_error()

    def __floordiv__(self, *args, **kwargs):
        self.raise_error()

    def __rfloordiv__(self, *args, **kwargs):
        self.raise_error()

    def __ifloordiv__(self, *args, **kwargs):
        self.raise_error()

    def __mod__(self, *args, **kwargs):
        self.raise_error()

    def __rmod__(self, *args, **kwargs):
        self.raise_error()

    def __imod__(self, *args, **kwargs):
        self.raise_error()

    def __divmod__(self, *args, **kwargs):
        self.raise_error()

    def __rdivmod__(self, *args, **kwargs):
        self.raise_error()

    # bitwise

    def __pow__(self, *args, **kwargs):
        self.raise_error()

    def __rpow__(self, *args, **kwargs):
        self.raise_error()

    def __ipow__(self, *args, **kwargs):
        self.raise_error()

    def __lshift__(self, *args, **kwargs):
        self.raise_error()

    def __rlshift__(self, *args, **kwargs):
        self.raise_error()

    def __ilshift__(self, *args, **kwargs):
        self.raise_error()

    def __rshift__(self, *args, **kwargs):
        self.raise_error()

    def __rrshift__(self, *args, **kwargs):
        self.raise_error()

    def __irshift__(self, *args, **kwargs):
        self.raise_error()

    def __or__(self, *args, **kwargs):
        self.raise_error()

    def __ror__(self, *args, **kwargs):
        self.raise_error()

    def __ior__(self, *args, **kwargs):
        self.raise_error()

    def __xor__(self, *args, **kwargs):
        self.raise_error()

    def __rxor__(self, *args, **kwargs):
        self.raise_error()

    def __ixor__(self, *args, **kwargs):
        self.raise_error()

    def __and__(self, *args, **kwargs):
        self.raise_error()

    def __rand__(self, *args, **kwargs):
        self.raise_error()

    def __iand__(self, *args, **kwargs):
        self.raise_error()

    def __invert__(self, *args, **kwargs):
        self.raise_error()


class MissingDependency(object, metaclass=MissingDependencyMeta):
    """
    Wrapper class and callable generator to be used instead of unavailable dependencies
    Errors on reference when not available instead of on import
    This class is not initializable directly (because it will raise an error) so the
    `OptionalDependencyWrapper` class is used to dynamically create an instance of it
    """

    import_path: Optional[str] = None
    pypi_name: Optional[str] = None
    host_pypi_name: Optional[str] = None
    extra_group: Optional[str] = None

    def __init__(self, *args, **kwargs):
        self.raise_error()

    def __new__(cls, *args, **kwargs):
        cls.raise_error()

    @classmethod
    def __call__(cls):
        cls.raise_error()

    @classmethod
    def raise_error(cls):
        message = f"Attempting to use missing dependency {cls.import_path}."
        if cls.pypi_name or cls.host_pypi_name:
            message += " Install via"

        if cls.pypi_name:
            message += f" `pip install {cls.pypi_name}`"
            if cls.host_pypi_name and cls.extra_group:
                message += " or"
        if cls.host_pypi_name and cls.extra_group:
            message += f" `pip install {cls.host_pypi_name}[{cls.extra_group}]`"
        if cls.pypi_name or cls.host_pypi_name:
            message += " and restart runtime"
        raise ImportError(
            message,
        )


class OptionalDependencyWrapper(object):
    """
    Factory class to generate library specific import wrappers
    """

    def __new__(
        cls,
        module_path: str,
        method_name: Optional[str] = None,
        pypi_name: Optional[str] = None,
        host_pypi_name: Optional[str] = None,
        extra_group: Optional[str] = None,
    ):
        # generate a valid class name from the import path
        class_name = module_path.replace(".", "_")
        if method_name:
            class_name = class_name + "_" + method_name
            import_path = f"{module_path}:{method_name}"
        else:
            import_path = module_path

        # normal import if possible
        try:
            if method_name:
                return cls.import_object(module_path, method_name)
            else:
                return cls.import_module(module_path)
        except ImportError:
            LOGGER.debug(f"Wrapping missing dependency: {import_path}")
            return cls.generate_wrapper(
                class_name, import_path, pypi_name, host_pypi_name, extra_group
            )

    @staticmethod
    def import_module(module_path: str) -> Any:
        return importlib.import_module(module_path)

    @classmethod
    def import_object(cls, module_path: Any, method_name: str) -> Any:
        module = cls.import_module(module_path)
        try:
            return getattr(module, method_name)
        except AttributeError:
            # some packages have attributes that do not exist unless explicitly imported
            # quick safety check to make sure we don't execute something we shouldn't
            # only allow paths that are in the form of `[a-zA-Z0-9._]`
            if not re.match(r"^[a-zA-Z0-9._]+$", module_path) or not re.match(
                r"^[a-zA-Z0-9._]+$", method_name
            ):
                raise ValueError(
                    f"Invalid module or method name: {module_path}:{method_name}. Did not pass safety check"
                )
            exec(f"from {module_path} import {method_name}")
            return getattr(module, method_name)

    @classmethod
    def generate_wrapper(
        cls,
        class_name: str,
        import_path: str,
        pypi_name: Optional[str] = None,
        host_pypi_name: Optional[str] = None,
        extra_group: Optional[str] = None,
    ):
        """
        Generate an import wrapper for a module
        """
        return types.new_class(
            name=class_name,
            bases=(MissingDependency,),
            kwds={
                "metaclass": MissingDependencyMeta,
            },
            exec_body=lambda ns: ns.update(
                {
                    "import_path": import_path,
                    "pypi_name": pypi_name,
                    "host_pypi_name": host_pypi_name,
                    "extra_group": extra_group,
                }
            ),
        )
