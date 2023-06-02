from datetime import datetime

from models.ecg_models import ECGResults
from utilities.record import Record

result = ECGResults(
        id=44,
        date=datetime.now(),
        lead_results=[{'name': 'first', 'zero_passes': 5}]
    )


def test_create_record_successfully():
    record = Record(result, "user1")

    assert record.result == result
    assert record.owner == "user1"


def test_record_dict_has_expected_format():
    record = Record(result, "user1")

    assert record.dict().get("result") == result.dict()
    assert record.dict().get("record_id") == 44
    assert record.dict().get("owner") == "user1"
