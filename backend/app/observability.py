import json
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from threading import Lock


def get_logger() -> logging.Logger:
    logger = logging.getLogger("app.observability")
    if logger.handlers:
        return logger

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    return logger


def log_event(logger: logging.Logger, event: str, **fields) -> None:
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": event,
        **fields,
    }
    logger.info(json.dumps(payload, ensure_ascii=True))


@dataclass
class APIMetrics:
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    requests_total: int = 0
    requests_2xx: int = 0
    requests_4xx: int = 0
    requests_5xx: int = 0
    latency_total_ms: float = 0.0
    _lock: Lock = field(default_factory=Lock, repr=False)

    def record_request(self, status_code: int, duration_ms: float) -> None:
        with self._lock:
            self.requests_total += 1
            self.latency_total_ms += duration_ms
            if 200 <= status_code < 300:
                self.requests_2xx += 1
            elif 400 <= status_code < 500:
                self.requests_4xx += 1
            elif 500 <= status_code < 600:
                self.requests_5xx += 1

    def snapshot(self) -> dict:
        with self._lock:
            uptime_seconds = (
                datetime.now(timezone.utc) - self.started_at
            ).total_seconds()
            avg_latency_ms = (
                self.latency_total_ms / self.requests_total
                if self.requests_total
                else 0.0
            )
            return {
                "started_at": self.started_at.isoformat(),
                "uptime_seconds": round(uptime_seconds, 2),
                "requests_total": self.requests_total,
                "requests_by_status": {
                    "2xx": self.requests_2xx,
                    "4xx": self.requests_4xx,
                    "5xx": self.requests_5xx,
                },
                "avg_latency_ms": round(avg_latency_ms, 2),
            }
