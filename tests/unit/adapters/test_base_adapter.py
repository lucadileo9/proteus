import pytest

from proteus.adapters.base import BaseAdapter


class TestBaseAdapterAbstract:
    """Verify that BaseAdapter cannot be instantiated directly."""

    def test_cannot_instantiate(self):
        """Instantiating BaseAdapter directly raises TypeError."""
        with pytest.raises(TypeError):
            BaseAdapter()

    def test_abstract_methods(self):
        """BaseAdapter declares load() and dump() as abstract methods."""
        abstracts = BaseAdapter.__abstractmethods__
        assert "load" in abstracts
        assert "dump" in abstracts

    def test_subclass_missing_method(self):
        """A subclass that only implements load() is still abstract."""

        class Incomplete(BaseAdapter):
            def load(self, raw):
                return {}

        with pytest.raises(TypeError):
            Incomplete()
