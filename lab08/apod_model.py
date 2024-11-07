import requests
from datetime import datetime

class APODModel:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.nasa.gov/planetary/apod"
        
    def get_apod(self, date=None):
        params = {'api_key': self.api_key}
        if date:
            params['date'] = date
            
        response = requests.get(self.base_url, params=params)
        
        if response.status_code != 200:
            raise Exception(f"API request failed with status code: {response.status_code}")
            
        return response.json()
    
    @staticmethod
    def validate_date(date_str):
        try:
            input_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            start_date = datetime(1995, 6, 16).date()
            today = datetime.now().date()
            
            if start_date <= input_date <= today:
                return True
            return False
        except ValueError:
            return False
