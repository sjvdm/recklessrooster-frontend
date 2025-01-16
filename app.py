from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Define a homepage route
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Reckless Roosters"})