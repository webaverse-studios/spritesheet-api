from typing import Union, Optional

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from ldm.generate import Generate
from omegaconf import OmegaConf
import random
from api import initModel, do_run

app = FastAPI()

@app.get("/")
async def root(prompt: str):
    res = do_run(prompt)
    return FileResponse(res)


if __name__ == "__main__":
    initModel()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7777, log_level="debug")