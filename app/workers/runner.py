import anyio
from ..services.scheduler import start_scheduler
from ..core.logging import get_logger
logger = get_logger(__name__)

async def main():
    await start_scheduler()
    logger.info('{"event":"worker_running"}')
    while True:
        await anyio.sleep(60)

if __name__ == "__main__":
    anyio.run(main)
