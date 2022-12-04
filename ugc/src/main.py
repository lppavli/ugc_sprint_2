import logging
import uvicorn as uvicorn
from fastapi import FastAPI
from aiokafka import AIOKafkaProducer
from fastapi.responses import ORJSONResponse
import sentry_sdk
from api.v1 import progress
from core.settings import Settings
from db import kafka_producer
from src.api.v1 import likes

settings = Settings()


if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        traces_sample_rate=settings.traces_sample_rate,
    )

app = FastAPI(
    title='API for posting user-generated content events to UGC db',
    docs_url="/ugc/openapi",
    openapi_url='/ugc/openapi.json',
    description='',
    default_response_class=ORJSONResponse,
    version="1.0.0",
)


@app.on_event("startup")
async def startup():
    kafka_producer.aio_producer = AIOKafkaProducer(
        **{
            'bootstrap_servers': '{}:{}'.format(
                settings.kafka_host,
                settings.kafka_port
            )
        }
                                    )
    await kafka_producer.aio_producer.start()


@app.on_event("shutdown")
async def shutdown():
    await kafka_producer.aio_producer.stop()


app.include_router(progress.router, prefix='/ugc/v1', tags=['progress_film'])
app.include_router(likes.router, prefix="/api/v1/likes", tags=["likes"])

if __name__ == '__main__':
    logging.info('Start application')
    uvicorn.run(
        "main:app",
        host='0.0.0.0',
        port=8001,
    )
