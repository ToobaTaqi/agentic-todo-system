from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Todo:
    id: int
    description: str
    completed: bool = False
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
