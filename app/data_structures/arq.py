from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Union


@dataclass
class JobConfig:
    job_id: Optional[str] = None
    run_after: Optional[Union[timedelta, int, float]] = None
    run_date: Optional[datetime] = None

    def __post_init__(self) -> None:
        assert not (
            self.run_after and self.run_date
        ), "Only one of run_after or run_date can be specified"

    def as_dict(self) -> Dict[str, Any]:
        return {
            "_job_id": self.job_id,
            "_defer_by": self.run_after,
            "_defer_until": self.run_date,
        }

    def __str__(self):
        return ", ".join([f"{k}={v}" for k, v in self.__annotations__.items()])
