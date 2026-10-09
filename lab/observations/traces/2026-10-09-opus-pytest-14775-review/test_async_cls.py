import pytest

class TestA:
    @pytest.fixture(scope="class")
    @classmethod
    async def afix(cls):
        return 1

    def test_1(self, afix):
        pass

    def test_2(self, afix):
        pass
