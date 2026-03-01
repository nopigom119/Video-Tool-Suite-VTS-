import time
import datetime
import re
from collections import deque

class TimeEstimator:
    def __init__(self, history_len=5):
        self.start_time = None
        self.last_update_time = None
        self.last_progress = 0
        self.speed_history = deque(maxlen=history_len)
        self.last_eta_str = "--:--"

    def start(self):
        self.start_time = time.time()
        self.last_update_time = self.start_time
        self.last_progress = 0
        self.speed_history.clear()
        self.last_eta_str = "--:--"

    def update(self, current_progress):
        """Update progress and return ETA string (current_progress: 0-100)"""
        now = time.time()
        if self.last_update_time is None:
            self.last_update_time = now
            return self.last_eta_str

        dt = now - self.last_update_time
        if dt < 1.0: 
            return self.last_eta_str

        dp = current_progress - self.last_progress
        if dp < 0: dp = 0

        instant_speed = dp / dt if dt > 0 else 0
        self.speed_history.append(instant_speed)
        
        avg_speed = sum(self.speed_history) / len(self.speed_history) if self.speed_history else instant_speed

        self.last_update_time = now
        self.last_progress = current_progress
        
        if avg_speed <= 0.01:
            self.last_eta_str = "--:--"
        else:
            remaining_percent = 100 - current_progress
            remaining_seconds = remaining_percent / avg_speed
            self.last_eta_str = str(datetime.timedelta(seconds=int(remaining_seconds)))
            
        return self.last_eta_str

    def reset(self):
        """Alias for start() to sync with main.py calls"""
        self.start()

def parse_dnd_paths(data):
    """Clean and split drag-and-drop path strings"""
    paths = []
    pattern = re.compile(r'\{.*?\}|\S+')
    matches = pattern.findall(data)
    for match in matches:
        path = match.strip('{}')
        if path: paths.append(path)
    return paths