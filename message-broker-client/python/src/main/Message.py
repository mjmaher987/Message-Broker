from dataclasses import dataclass
from datetime import datetime

@dataclass
class Message:
    key: str
    value: str
    time_arrived: datetime
