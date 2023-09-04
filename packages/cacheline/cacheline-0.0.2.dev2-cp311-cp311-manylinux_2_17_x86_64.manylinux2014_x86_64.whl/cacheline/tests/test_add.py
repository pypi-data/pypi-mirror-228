from cacheline.add import add  # type:ignore


def test_add():
    assert add(1, 2) == 3
