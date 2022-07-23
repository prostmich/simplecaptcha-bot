import asyncio
from contextlib import suppress
from typing import Any, Dict, Optional

from arq import create_pool
from arq.connections import ArqRedis, RedisSettings
from arq.jobs import Job

from app.data_structures.arq import JobConfig
from app.misc.loggers import logger


class ArqScheduler:
    def __init__(self) -> None:
        self._redis: Optional[ArqRedis] = None

    async def init(
        self,
        connection_uri: str,
    ) -> None:
        self._redis = await create_pool(RedisSettings.from_dsn(connection_uri))

    async def enqueue_job(
        self, task: str, job_kwargs: Dict[str, Any], job_config: JobConfig
    ) -> Optional[Job]:
        job = await self._enqueue_job(task, job_kwargs, job_config)
        logger.info(
            "Enqueued job ({task}) with params {kwargs}".format(
                task=task, kwargs=job_kwargs
            )
        )
        return job

    async def abort_job(self, job_id: str) -> None:
        await self._abort_job(job_id)
        logger.info("Aborted job ({job_id})".format(job_id=job_id))

    async def _enqueue_job(
        self, task: str, task_kwargs: Dict[str, Any], task_config: JobConfig
    ) -> Optional[Job]:
        if self._redis is None:
            raise Exception("Redis connection is not initialized")
        kwargs = task_kwargs | task_config.as_dict()
        return await self._redis.enqueue_job(function=task, **kwargs)

    async def _abort_job(self, job_id: str) -> None:
        if self._redis is None:
            raise Exception("Redis connection is not initialized")
        with suppress(asyncio.TimeoutError):
            await Job(job_id, redis=self._redis).abort(timeout=0)
