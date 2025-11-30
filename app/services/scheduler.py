from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from ..core.logging import get_logger
logger = get_logger(__name__)

scheduler: AsyncIOScheduler | None = None

async def start_scheduler() -> AsyncIOScheduler:
    global scheduler
    if scheduler:
        return scheduler
    scheduler = AsyncIOScheduler()
    scheduler.start()
    logger.info('{"event":"scheduler_started"}')
    return scheduler
