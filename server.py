from fastapi import FastAPI
from fastapi.responses import FileResponse
from api import initModel, do_run
from pymatting import cutout
import PIL

app = FastAPI()

@app.get("/")
async def root(s: str):
    if s.find("spritesheet") == -1:
        s = s + " spritesheet"

    cutFileName = None
    isBlack = True

    while isBlack == True:
        res = do_run(s)
        print(res)
        filename = res[0] + "/" + res[1] + "(" + str(res[2]) + ")_0.png"
        cutFileName = res[0] + "/" + res[1] + "(" + str(res[2]) + ")_cut_0.png"

        img = PIL.Image.open(filename)
        extrema = img.convert("L").getextrema()
        if extrema == (0, 0):
            isBlack = True
        else:
            isBlack = False
            
            cutout(
                filename,
                "./mask.png",
                cutFileName,
            )

    return FileResponse(cutFileName)


if __name__ == "__main__":
    initModel()
    print("model initialized")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7777, log_level="debug")