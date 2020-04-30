from drf_exercise import models


def test_model():
    assert models.Employee(name='Ben').name == 'Ben'
