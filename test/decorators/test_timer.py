from my_utils.decorators import time


def test_timer(capsys):
    @time.timer
    def add(x):
        return x + 1

    val = add(2)
    captured = capsys.readouterr().out
    assert val == 3
    assert "timer" in captured
    assert "sec" in captured
