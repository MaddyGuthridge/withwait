"""
Basic test cases
"""
import pytest
from withwait import wait
from jestspectation import FloatApprox
from time import time, sleep


def test_waits_standard():
    """
    Does it wait as required under normal circumstances
    """
    start = time()
    with wait(0.1):
        pass
    end = time()
    assert FloatApprox(0.1, percent=1) == end - start


def test_waits_with_partial_sleep():
    """
    Does it wait for the remaining time if a sleep is done in the with
    statement?
    """
    with wait(0.1):
        sleep(0.05)
        start = time()
    end = time()
    assert FloatApprox(0.05, percent=1) == end - start


def test_no_wait_with_full_sleep():
    """
    Does it continue immediately if executing the with statement takes longer
    than we need to wait?
    """
    with wait(0.05):
        sleep(0.1)
        start = time()
    end = time()
    assert FloatApprox(0, magnitude=0.001) == end - start


def test_waits_with_exception():
    """
    Does it wait for the remaining time if an exception is raised in the with
    statement?
    """
    start = time()
    with pytest.raises(ValueError):
        with wait(0.1):
            raise ValueError("Yikes")
    end = time()
    assert FloatApprox(0.1, percent=1) == end - start
