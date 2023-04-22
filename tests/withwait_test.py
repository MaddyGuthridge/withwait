"""
Basic test cases
"""
import pytest
from withwait import wait, WithwaitAbort, WithwaitAbortAll
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
    start = 0
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
    start = 0
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


def test_cancels_correctly():
    """
    Can we cancel the waiting?
    """
    start = time()
    with wait(0.1) as timer:
        timer.cancel()
    end = time()
    assert FloatApprox(0, magnitude=0.01) == end - start


def test_cancels_independently_inner():
    """
    If we run two timers together, do the correct timers get cancelled?
    """
    start = time()
    with wait(0.1):
        with wait(0.2) as inner_timer:
            inner_timer.cancel()
    end = time()
    assert FloatApprox(0.1, magnitude=0.01) == end - start


def test_cancels_independently_outer():
    """
    If we run two timers together, do the correct timers get cancelled?
    """
    start = time()
    with wait(0.2) as outer_timer:
        with wait(0.1):
            outer_timer.cancel()
    end = time()
    assert FloatApprox(0.1, magnitude=0.01) == end - start


def test_aborts_correctly():
    """
    Can we abort the waiting, and when we do, do we get an error?
    """
    start = time()
    with pytest.raises(WithwaitAbort):
        with wait(0.1) as timer:
            timer.abort()
    end = time()
    assert FloatApprox(0, magnitude=0.01) == end - start


def test_abort_cannot_be_caught():
    """
    If we abort the timer, are we unable to catch it (at least not easily)?
    """
    with pytest.raises(WithwaitAbort):
        with wait(0.1) as timer:
            try:
                timer.abort()
            except WithwaitAbort:
                raise ValueError("Yikes it broken")


def test_abort_args_preserved():
    """
    If we abort the timer, are our arguments preserved in the exception?
    """
    try:
        with wait(0.1) as timer:
            timer.abort("hello", "world")
    except WithwaitAbort as e:
        assert e.args == ("hello", "world")


def test_abort_timers_independent_inner():
    """
    If we run two timers together, do the correct timers get aborted?
    """
    start = time()
    with pytest.raises(WithwaitAbort):
        with wait(0.1):
            with wait(0.2) as inner_timer:
                inner_timer.abort()
    end = time()
    assert FloatApprox(0.1, percent=1) == end - start


def test_abort_timers_independent_outer():
    """
    If we run two timers together, do the correct timers get aborted?
    """
    start = time()
    with pytest.raises(WithwaitAbort):
        with wait(0.2) as outer_timer:
            with wait(0.1):
                outer_timer.abort()
    end = time()
    assert FloatApprox(0.1, percent=1) == end - start


def test_abort_all():
    """
    If we use abort_all, do all timers get aborted?
    """
    start = time()
    with pytest.raises(WithwaitAbortAll):
        with wait(0.2) as outer_timer:
            with wait(0.1):
                outer_timer.abort_all()
    end = time()
    assert FloatApprox(0.0, magnitude=0.01) == end - start


def test_abort_all_args_preserved():
    """
    If we give args to abort_all, do they get preserved?
    """
    try:
        with wait(0.2) as outer_timer:
            with wait(0.1):
                outer_timer.abort_all("hello", "world")
    except WithwaitAbortAll as e:
        assert e.args == ("hello", "world")
