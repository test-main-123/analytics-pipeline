"""Pipeline metrics collection and reporting."""

import time
import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class StepMetric:
    """Metrics for a single pipeline step."""

    name: str
    rows_in: int = 0
    rows_out: int = 0
    duration_seconds: float = 0.0
    errors: int = 0


@dataclass
class PipelineMetrics:
    """Aggregated metrics for a pipeline run."""

    steps: list[StepMetric] = field(default_factory=list)
    start_time: float = 0.0
    end_time: float = 0.0

    def start(self) -> None:
        """Mark the pipeline run as started."""
        self.start_time = time.time()

    def stop(self) -> None:
        """Mark the pipeline run as finished."""
        self.end_time = time.time()

    def add_step(self, metric: StepMetric) -> None:
        """Record a step metric."""
        self.steps.append(metric)

    @property
    def total_duration(self) -> float:
        """Total pipeline duration in seconds."""
        return self.end_time - self.start_time

    def summary(self) -> dict:
        """Return a summary dict of the pipeline run."""
        return {
            "total_duration_seconds": round(self.total_duration, 3),
            "total_steps": len(self.steps),
            "total_errors": sum(s.errors for s in self.steps),
            "steps": [
                {
                    "name": s.name,
                    "rows_in": s.rows_in,
                    "rows_out": s.rows_out,
                    "duration_seconds": round(s.duration_seconds, 3),
                }
                for s in self.steps
            ],
        }

    def log_summary(self) -> None:
        """Log the pipeline metrics summary."""
        s = self.summary()
        logger.info("Pipeline completed in %.3fs with %d steps.", s["total_duration_seconds"], s["total_steps"])
        for step in s["steps"]:
            logger.info("  %s: %d rows in -> %d rows out (%.3fs)", step["name"], step["rows_in"], step["rows_out"], step["duration_seconds"])
