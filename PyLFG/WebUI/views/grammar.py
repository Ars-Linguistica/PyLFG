from fastapi import FastAPI, Form
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/grammar")
async def grammar_view(request):
    return templates.TemplateResponse("grammar_view.html", {"request": request})

@app.post("/upload_grammar")
async def upload_grammar(request, grammar: str = Form(...)):
    # Save the uploaded grammar to a file or database
    # ...
    return templates.TemplateResponse("upload_success.html", {"request": request})
