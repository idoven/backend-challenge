import pytest
from datetime import datetime

from models.ecg_models import ECGData
from processor.basic_processor import ECGProcessor
from database.volatile_database import DatabaseHandlerVolatile

db = DatabaseHandlerVolatile()


@pytest.mark.asyncio
async def test_setting_record_metadata():
    processor = ECGProcessor(db)

    data = ECGData(
        id=44,
        date=datetime.now(),
        leads=[]
    )

    await processor.process_ecg(data, "user1")
    record = db.retrieve_record(44)

    assert record.owner == "user1"


@pytest.mark.asyncio
async def test_process_empty_data():
    processor = ECGProcessor(db)

    data = ECGData(
        id=44,
        date=datetime.now(),
        leads=[]
    )

    await processor.process_ecg(data, "user1")
    record = db.retrieve_record(44)

    assert record.result.id == 44
    assert len(record.result.lead_results) == 0


@pytest.mark.asyncio
async def test_process_lead_without_defined_samples():
    processor = ECGProcessor(db)

    data = ECGData(
        id=44,
        date=datetime.now(),
        leads=[
            {
                'name': 'first',
                'signal': [0, 1, 2, 5, 0, -1, 0, 1, 2, 2, 0, -1]
            }
        ]
    )

    await processor.process_ecg(data, "user1")
    record = db.retrieve_record(44)

    assert record.result.id == 44
    assert len(record.result.lead_results) == 1
    assert record.result.lead_results[0].name == "first"
    assert record.result.lead_results[0].zero_passes == 4


@pytest.mark.asyncio
async def test_process_lead_with_defined_samples():
    processor = ECGProcessor(db)

    data = ECGData(
        id=44,
        date=datetime.now(),
        leads=[
            {
                'name': 'first',
                'samples': 10,
                'signal': [0, 1, 2, 5, 0, -1, 0, 1, 2, 2, 0, -1]
            }
        ]
    )

    await processor.process_ecg(data, "user1")
    record = db.retrieve_record(44)

    assert record.result.id == 44
    assert len(record.result.lead_results) == 1
    assert record.result.lead_results[0].name == "first"
    assert record.result.lead_results[0].zero_passes == 3


@pytest.mark.asyncio
async def test_process_lead_with_defined_samples_too_large():
    processor = ECGProcessor(db)

    data = ECGData(
        id=44,
        date=datetime.now(),
        leads=[
            {
                'name': 'first',
                'samples': 14,
                'signal': [0, 1, 2, 5, 0, -1, 0, 1, 2, 2, 0, -1]
            }
        ]
    )

    await processor.process_ecg(data, "user1")
    record = db.retrieve_record(44)

    assert record.result.id == 44
    assert len(record.result.lead_results) == 1
    assert record.result.lead_results[0].name == "first"
    assert record.result.lead_results[0].zero_passes == 4


@pytest.mark.asyncio
async def test_process_lead_with_multiple_leads():
    processor = ECGProcessor(db)

    data = ECGData(
        id=44,
        date=datetime.now(),
        leads=[
            {
                'name': 'first',
                'signal': [0, 1, 2, 5, 0, -1, 0, 1, 2, 2, 0, -1]
            },
            {
                'name': 'second',
                'samples': 10,
                'signal': [0, 1, 2, 5, 0, -1, 0, 1, 2, 2, 0, -1]
            }
        ]
    )

    await processor.process_ecg(data, "user1")
    record = db.retrieve_record(44)

    assert record.result.id == 44
    assert len(record.result.lead_results) == 2
    assert record.result.lead_results[0].name == "first"
    assert record.result.lead_results[1].name == "second"
    assert record.result.lead_results[0].zero_passes == 4
    assert record.result.lead_results[1].zero_passes == 3
