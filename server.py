from fastapi import FastAPI
from fastapi.responses import FileResponse
from api import initModel, do_run

app = FastAPI()

@app.get("/")
async def root(s: str):
    if s.find("spritesheet") == -1:
        s = s + " spritesheet"

    res = do_run(s)
    print(res)
    filename = res[0] + "/" + res[1] + "(" + str(res[2]) + ")_0.png"
    return FileResponse(filename)


if __name__ == "__main__":
    initModel()
    print("model initialized")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7777, log_level="debug")