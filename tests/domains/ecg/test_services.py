import pytest

from ecg.domains.ecg.services import calculate_zero_crossings


@pytest.mark.parametrize(
    "signal, expected_crossings",
    [
        ([1, -1, 1, -1], 3),
        ([-1, 1, -1, 1, -1], 4),
        ([1, 2, 3, -1, -2, -3], 1),
        ([], 0),
        ([1, 1, 1], 0),
        ([-1, -1, -1], 0),
        ([1, 1, 0, -1, -1], 1),
    ],
)
def test_calculate_zero_crossings(signal, expected_crossings):
    crossings = calculate_zero_crossings(signal)
    assert crossings == expected_crossings
