import os
import time
from typing import List

from fastapi import FastAPI, HTTPException, Request, Response
from pydantic import HttpUrl

from assistent.assistent import Assistent
from assistent.inference import AIInference, OpenaiEmbeddings
from assistent.local_retrieve import LocalRetrieve
from schemas.request import PredictionRequest, PredictionResponse
from utils.logger import setup_logger
from utils import load_config, DIR


def _set_env(var: str):
    if not os.environ.get(var):
        raise EnvironmentError(f"{var} is not setted")
_set_env("TAVILY_API_KEY")
_set_env("LANGSMITH_API_KEY")
_set_env("OPENAI_TOKEN")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "MegaSchoolAI"

# Initialize
app = FastAPI()
logger = None

config = load_config(f"{DIR}/config.json")
inference = AIInference()
retrieve = LocalRetrieve(embeddings=os.environ['OPENAI_TOKEN'], base_url=config['base_url'], model=config['embeddings'])


@app.on_event("startup")
async def startup_event():
    global logger
    logger = await setup_logger()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    body = await request.body()
    await logger.info(
        f"Incoming request: {request.method} {request.url}\n"
        f"Request body: {body.decode()}"
    )

    response = await call_next(request)
    process_time = time.time() - start_time

    response_body = b""
    async for chunk in response.body_iterator:
        response_body += chunk

    await logger.info(
        f"Request completed: {request.method} {request.url}\n"
        f"Status: {response.status_code}\n"
        f"Response body: {response_body.decode()}\n"
        f"Duration: {process_time:.3f}s"
    )

    return Response(
        content=response_body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type,
    )


@app.post("/api/request", response_model=PredictionResponse)
async def predict(body: PredictionRequest):
    try:
        await logger.info(f"Processing prediction request with id: {body.id}")
        # Здесь будет вызов вашей модели
        assistent = Assistent(inference=inference).create_graph()
        result = assistent.invoke({"query": body.query})
        result['reasoning'] = result['reasoning'] + f'\nОтвет сгенерирован моделью: {inference.model}'
        response = PredictionResponse(
            id=body.id,
            answer=result['answer'],
            reasoning=result['reasoning'],
            sources=result['sources'],
        )
        await logger.info(f"Successfully processed request {body.id}")
        return response
    except ValueError as e:
        error_msg = str(e)
        await logger.error(f"Validation error for request {body.id}: {error_msg}")
        raise HTTPException(status_code=400, detail=error_msg)
    except Exception as e:
        await logger.error(f"Internal error processing request {body.id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
