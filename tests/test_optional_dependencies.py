import types

import pytest

from import_wrappers.optional_dependencies import (
    MissingDependency,
    MissingDependencyMeta,
    OptionalDependencyWrapper,
)


class TestMissingDependencyObject(object):
    """
    Just test trying to call methods directly on the MissingDependency object
    """

    def test_new(self):
        # default call when invoked directly
        with pytest.raises(ImportError):
            MissingDependency()
        with pytest.raises(ImportError):
            MissingDependency.__new__(MissingDependency)

    def test_init(self):
        obj = object.__new__(MissingDependency)
        with pytest.raises(ImportError):
            obj.__init__()

    def test_call(self):
        obj = object.__new__(MissingDependency)
        with pytest.raises(ImportError):
            obj()


class TestMissingDependencyWithMetaclass(object):
    """
    Tests for the MissingDependency object with a metaclass
    """

    @pytest.fixture
    @staticmethod
    def mock_dependency():
        return types.new_class(
            name="test",
            bases=(MissingDependency,),
            kwds={
                "metaclass": MissingDependencyMeta,
            },
            exec_body=lambda ns: ns.update(
                {
                    "import_path": "test",
                    "pypi_name": "something",
                    "host_pypi_name": "main-project",
                    "extra_group": "test",
                }
            ),
        )

    def test_error_message(self, mock_dependency):
        with pytest.raises(ImportError) as exc:
            mock_dependency()

        assert (
            str(exc.value)
            == "Attempting to use missing dependency test. Install via `pip install something` or `pip install main-project[test]` and restart runtime"
        )

        # cover the different variations of the error message
        mock_dependency.host_pypi_name = None
        with pytest.raises(ImportError) as exc:
            mock_dependency()
        assert (
            str(exc.value)
            == "Attempting to use missing dependency test. Install via `pip install something` and restart runtime"
        )

        mock_dependency.pypi_name = None
        mock_dependency.host_pypi_name = "main-project"
        with pytest.raises(ImportError) as exc:
            mock_dependency()
        assert (
            str(exc.value)
            == "Attempting to use missing dependency test. Install via `pip install main-project[test]` and restart runtime"
        )

    def test_repr(self, mock_dependency):
        assert (
            repr(mock_dependency)
            == "Missing Dependency Wrapper for test (`pip install something` or `pip install main-project[test]`)"
        )
        assert (
            str(mock_dependency)
            == "Missing Dependency Wrapper for test (`pip install something` or `pip install main-project[test]`)"
        )

    def test_callable(self, mock_dependency):
        with pytest.raises(ImportError):
            mock_dependency()

    def test_inheritence(self, mock_dependency):
        class ChildObj(mock_dependency):
            pass

        with pytest.raises(ImportError):
            ChildObj()

    def test_recursive_refs(self, mock_dependency):
        # show that we can access attributes recusively
        mock_dependency.abc
        obj = mock_dependency.abc.ghi
        obj.jkl

        assert isinstance(obj, MissingDependencyMeta)
        assert issubclass(obj, MissingDependency)
        with pytest.raises(ImportError):
            mock_dependency.abc()

    def test_noneness(self, mock_dependency):
        with pytest.raises(ImportError):
            bool(mock_dependency)

    def test_arithmetic(self, mock_dependency):
        var = 1
        with pytest.raises(ImportError):
            mock_dependency + var
        with pytest.raises(ImportError):
            var + mock_dependency
        with pytest.raises(ImportError):
            mock_dependency += var
        with pytest.raises(ImportError):
            mock_dependency - var
        with pytest.raises(ImportError):
            var - mock_dependency
        with pytest.raises(ImportError):
            mock_dependency -= var
        with pytest.raises(ImportError):
            mock_dependency * var
        with pytest.raises(ImportError):
            var * mock_dependency
        with pytest.raises(ImportError):
            mock_dependency *= var
        with pytest.raises(ImportError):
            mock_dependency / var
        with pytest.raises(ImportError):
            var / mock_dependency
        with pytest.raises(ImportError):
            mock_dependency /= var
        with pytest.raises(ImportError):
            mock_dependency @ var
        with pytest.raises(ImportError):
            var @ mock_dependency
        with pytest.raises(ImportError):
            mock_dependency @= var
        with pytest.raises(ImportError):
            var @= mock_dependency
        with pytest.raises(ImportError):
            mock_dependency % var
        with pytest.raises(ImportError):
            var % mock_dependency
        with pytest.raises(ImportError):
            mock_dependency %= var
        with pytest.raises(ImportError):
            var %= mock_dependency
        with pytest.raises(ImportError):
            mock_dependency**var
        with pytest.raises(ImportError):
            var**mock_dependency
        with pytest.raises(ImportError):
            mock_dependency **= var
        with pytest.raises(ImportError):
            var **= mock_dependency
        with pytest.raises(ImportError):
            mock_dependency // var
        with pytest.raises(ImportError):
            var // mock_dependency
        with pytest.raises(ImportError):
            mock_dependency //= var
        with pytest.raises(ImportError):
            var //= mock_dependency
        with pytest.raises(ImportError):
            divmod(mock_dependency, var)
        with pytest.raises(ImportError):
            divmod(var, mock_dependency)

    def test_bitwise(self, mock_dependency):
        var = 1
        with pytest.raises(ImportError):
            mock_dependency << var
        with pytest.raises(ImportError):
            var << mock_dependency
        with pytest.raises(ImportError):
            mock_dependency <<= var
        with pytest.raises(ImportError):
            var <<= mock_dependency
        with pytest.raises(ImportError):
            mock_dependency >> var
        with pytest.raises(ImportError):
            var >> mock_dependency
        with pytest.raises(ImportError):
            mock_dependency >>= var
        with pytest.raises(ImportError):
            var >>= mock_dependency
        with pytest.raises(ImportError):
            mock_dependency & var
        with pytest.raises(ImportError):
            var & mock_dependency
        with pytest.raises(ImportError):
            mock_dependency &= var
        with pytest.raises(ImportError):
            var &= mock_dependency
        with pytest.raises(ImportError):
            mock_dependency | var
        with pytest.raises(ImportError):
            var | mock_dependency
        with pytest.raises(ImportError):
            mock_dependency |= var
        with pytest.raises(ImportError):
            var |= mock_dependency
        with pytest.raises(ImportError):
            mock_dependency ^ var
        with pytest.raises(ImportError):
            var ^ mock_dependency
        with pytest.raises(ImportError):
            mock_dependency ^= var
        with pytest.raises(ImportError):
            var ^= mock_dependency
        with pytest.raises(ImportError):
            ~mock_dependency

    def test_comparison(self, mock_dependency):
        with pytest.raises(ImportError):
            mock_dependency < 1
        with pytest.raises(ImportError):
            1 < mock_dependency
        with pytest.raises(ImportError):
            mock_dependency <= 1
        with pytest.raises(ImportError):
            1 <= mock_dependency
        with pytest.raises(ImportError):
            mock_dependency > 1
        with pytest.raises(ImportError):
            1 > mock_dependency
        with pytest.raises(ImportError):
            mock_dependency >= 1
        with pytest.raises(ImportError):
            1 >= mock_dependency
        with pytest.raises(ImportError):
            mock_dependency == 1
        with pytest.raises(ImportError):
            1 == mock_dependency
        with pytest.raises(ImportError):
            mock_dependency != 1
        with pytest.raises(ImportError):
            1 != mock_dependency

    def test_membership(self, mock_dependency):
        with pytest.raises(ImportError):
            1 in mock_dependency


class TestOptionalDependencyWrapper:
    """
    Set of tests to check that the import wrappers work as expected when a dependency is missing.
    """

    def test_loading_module(self):
        wrapper = OptionalDependencyWrapper(
            "nonexistent",
        )
        assert isinstance(wrapper, MissingDependencyMeta)
        assert issubclass(wrapper, MissingDependency)

    def test_loading_submodule(self):
        wrapper = OptionalDependencyWrapper(
            "nonexistent.super_nonexistent",
        )
        assert isinstance(wrapper, MissingDependencyMeta)
        assert issubclass(wrapper, MissingDependency)

    def test_importing_object(self):
        wrapper = OptionalDependencyWrapper(
            "nonexistent",
            "nonexistent",
        )
        assert isinstance(wrapper, MissingDependencyMeta)
        assert issubclass(wrapper, MissingDependency)

    def test_importing_unsafe_object(self):
        # attempt injection of "malicious" code
        with pytest.raises(ValueError):
            OptionalDependencyWrapper("re", "match; raise Exception;")

    def test_generating_wrapper(self):
        wrapper = OptionalDependencyWrapper.generate_wrapper(
            class_name="nonexistent",
            import_path="nonexistent",
            pypi_name="nonexistent",
            host_pypi_name="nonexistent",
            extra_group="nonexistent",
        )
        assert isinstance(wrapper, MissingDependencyMeta)
        assert issubclass(wrapper, MissingDependency)

    """
    Set of tests to check that the import wrappers work as expected when a dependency is present.
    This focuses on verifying the import mechanism since we cannot use the default import syntax
    (e.g. from dependency import module)
    """

    def test_passthrough_existing_module(self):
        """Test that the wrapper for an optional dependency that already exists on the system is
        a passthrough."""
        wrapper = OptionalDependencyWrapper("re")
        assert not isinstance(wrapper, MissingDependencyMeta)
        import re

        assert wrapper == re

    def test_passthrough_existing_submodule(self):
        wrapper = OptionalDependencyWrapper("collections.abc")
        assert not isinstance(wrapper, MissingDependencyMeta)
        import collections.abc

        assert wrapper == collections.abc

    def test_passthrough_existing_object(self):
        wrapper = OptionalDependencyWrapper("re", "match")
        assert not isinstance(wrapper, MissingDependencyMeta)
        from re import match

        assert wrapper == match
