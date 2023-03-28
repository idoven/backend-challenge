from pydantic import BaseModel
import json

'''
ecg_dict = {
  "id": int,
  "date": str,
  "leads": [
    {
      "name": str,
      "number_of_samples": int,
      "signal": [int]
    }
  ]
}
'''

class Data(BaseModel):
    data: dict
    
    class Config:
        schema_extra: dict = {
            'example': [{
                'data': {
                    "id": "ecg1",
                    "date": "2022-04-01",
                    "leads": [{
                        "name": "I",
                        "number_of_samples": 1000,
                        "signal": [1, 2, 3, 0, 5, 6, 0, 8, 0, 10]
                        },
                        {
                        "name": "II",
                        "number_of_samples": 1000,
                        "signal": [11, 12, 13, 0, 15, 16, 0, 18, 19, 20]
                    }]
                }
            }]
        }

    def check_values(json_data):
        result = {}
        parsed_data = json.dumps(json_data)
        # Load JSON data as a Python dictionary
        data = json.loads(parsed_data)
        
        # Check if "signal" field contains any integer value of 0
        for lead in data['leads']:
            signal = lead['signal']
            count = 0
            for i in range(len(signal)-1):
                if signal[i] >= 0 and signal[i+1] < 0:
                    count += 1
                elif signal[i] < 0 and signal[i+1] >= 0:
                    count += 1
            result[lead['name']] = count
        return result
            