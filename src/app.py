from fastapi import FastAPI, UploadFile, Request
from fastapi.templating import Jinja2Templates
import uvicorn
import argparse
import logging
from fastapi.staticfiles import StaticFiles
from model import Model

app = FastAPI()

app.mount("/tmp", StaticFiles(directory="tmp"), name='images')
templates = Jinja2Templates(directory="templates")

app_logger = logging.getLogger(__name__)
app_logger.setLevel(logging.INFO)
app_handler = logging.StreamHandler()
app_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
app_handler.setFormatter(app_formatter)
app_logger.addHandler(app_handler)


@app.get("/health")
def health():
    return {"status": "OK"}

@app.get("/")
def main(request: Request):
    return templates.TemplateResponse("start_form.html",
                                      {"request": request})


@app.post("/process")
def process_request(file: UploadFile, request: Request):
    save_pth = "tmp/" + file.filename
    app_logger.info(f'processing file - {save_pth}')
    with open(save_pth, "wb") as fid:
        fid.write(file.file.read())
    predictor = Model(0.6)
    status, result = predictor(save_pth)
    return templates.TemplateResponse("res_form.html",
                                          {"request": request,
                                           "res": status,
                                           "message": status, "path": result})

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", default=8000, type=int, dest="port")
    parser.add_argument("--host", default="0.0.0.0", type=str, dest="host")
    args = vars(parser.parse_args())

    uvicorn.run(app, **args)
