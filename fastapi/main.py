from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"id": "12345"}
    )

@app.post("/search")
async def search(search_query: str = Form()):
    return (f"search_query: {search_query}")

# @app.post("/scrape")


# On timer, re-run webscraper