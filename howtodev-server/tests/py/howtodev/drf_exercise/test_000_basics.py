"Test that the runner is working."

import pytest


@pytest.mark.describe('Python can')
class TestBasic():
    "Basics"

    @pytest.mark.run(order=1)
    @pytest.mark.it('do basic math')
    def test_basic_math(self):
        "Addition"
        assert 1+1 == 2
