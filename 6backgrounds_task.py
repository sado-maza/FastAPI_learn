import asyncio
import time
from fastapi import FastAPI, BackgroundTasks
from starlette.concurrency import run_in_threadpool

app = FastAPI()


def synk_def():
    time.sleep(5)
    return {"message": "Hello World with synk"}


async def async_def():
    time.sleep(3)

    return {"message": "Hello World with async"}


@app.get("/")
async def synk_async(bg_task: BackgroundTasks):
    ...

    asyncio.create_task(async_def())
    bg_task.add_task(synk_def)
    return {"message": "start finish"}