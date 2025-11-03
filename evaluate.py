import json
import requests 

from typing import List, Optional
from pydantic import BaseModel, TypeAdapter, ValidationError
from pathlib import Path


class Evaluator():
    class LogEntry(BaseModel):
        text: str
        true_label: str
        
        
    def __init__(self, json_path, log_path):
        self.json_path = self._validate_json(json_path)
        self.log_path = self._validate_log(log_path)
        self.dat = self._load_data()
        
    def _validate_json(self, json_path):
        path = Path(json_path)
        if path.exists():
            print(f'✅ Loaded {path} successfully')
            return path
        raise FileNotFoundError(f"File at {path} not found.")
    
    def _validate_log(self, log_path):
        path = Path(log_path)
        if path.exists():
            print(f'✅ Loaded {path} successfully')
            return path
        raise FileNotFoundError(f"File at {path} not found.")
        
    def _validate_data(self, data):
        """Validates the data structure of loaded test data"""
        adapter = TypeAdapter(List[self.LogEntry])
        try:
            validated = adapter.validate_python(data)
            return validated
        except ValidationError as e:
            raise ValueError(f"Invalid log data format: {e}")
    
    def _load_data(self) -> List['Evaluator.LogEntry']:
        """Load JSON data from file or return empty dict if file doesn't exist"""
        with open(self.json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        return self._validate_data(data)
        
        
    def post_dat(self, method):
        """Iterates over dat file, POSTing to /predict endpoint. Method determines if function will write over old log file or append to existing one. w to write over, a to append"""
        match method:
            case 'r':
                pass
            case 'w':
                pass
                        
if __name__ == "__main__":
    eval = Evaluator(json_path='test.json', log_path='./logs/prediction_logs.json')
    