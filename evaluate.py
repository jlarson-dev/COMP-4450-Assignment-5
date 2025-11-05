import json
import requests 
import os

from typing import List
from pydantic import BaseModel, TypeAdapter, ValidationError
from pathlib import Path
from sklearn.metrics import confusion_matrix


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
        
    def _delete_logs(self):
        """Deletes log file"""
        if os.path.exists(self.log_path):
            os.remove(self.log_path)
            print(f"Deleted existing log file: {self.log_path}")
        
    def post_dat(self, method="a"):
        """Iterates over dat file, POSTing to /predict endpoint. Method determines handling of log file. 'a' will append to log file, while 'd' will delete the log file first"""
        url = "http://127.0.0.1:8000/predict"

        match method:
            case "a":
                pass
            case "d":
                self._delete_logs()
            case _:
                pass
        
        predictions = list()
        true_labels = list()
        for entry in self.dat:
            response = requests.post(
                url,
                json={
                    "text": entry.text,
                    "true_sentiment": entry.true_label
                }
            )
            try:
                data = response.json()
            except Exception:
                print(f"Non-JSON response: {response.text}")
                continue

            predicted = data.get("sentiment")
            if predicted is not None:
                predictions.append(predicted)
                true_labels.append(entry.true_label)
            else:
                print(f"Missing prediction in response: {data}")

        # Accuracy
        correct = sum(p == t for p, t in zip(predictions, true_labels))
        total = len(true_labels)
        accuracy = correct / total if total > 0 else 0

        print(f"\nModel accuracy: {accuracy:.2%} ({correct}/{total} correct)")
                        
if __name__ == "__main__":
    eval = Evaluator(json_path='test.json', log_path='./logs/prediction_logs.json')
    eval.post_dat(method='d')