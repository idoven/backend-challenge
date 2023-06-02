from models.ecg_models import ECGData, ECGResults, ECGLeadResult
from database.database_handler import DatabaseHandler
from utilities.record import Record


class ECGProcessor:
    def __init__(self, database: DatabaseHandler):
        self.db = database

    async def process_ecg(self, data: ECGData, username: str):
        result = ECGResults(id=data.id, date=data.date, lead_results=[])

        for lead in data.leads:
            lead_result = ECGLeadResult(name=lead.name, zero_passes=0)

            if lead.samples > 0:
                length = min(lead.samples, len(lead.signal))
            else:
                length = len(lead.signal)

            for i in range(length-1):
                if lead.signal[i] > 0 and lead.signal[i+1] <= 0:
                    lead_result.zero_passes += 1
                elif lead.signal[i] <= 0 and lead.signal[i+1] > 0:
                    lead_result.zero_passes += 1

            result.lead_results.append(lead_result)

        self.db.add_record(result.id, Record(result, username))
