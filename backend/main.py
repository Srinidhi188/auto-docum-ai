
# main.py
import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from code_parser import parse_code
from ai_generator import generate_documentation
from pdf_utils import create_arch_diagram, create_pdf_from_markdown

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "AutoDoc AI Backend Running"}

@app.post("/upload-code/")
async def upload_code(file: UploadFile = File(...)):
    """
    Accepts a single .py file, parses it, calls LLM to generate markdown documentation.
    Returns JSON with documentation and parsed structure.
    """
    try:
        raw = await file.read()
        code_text = raw.decode("utf-8", errors="ignore")
        parsed = parse_code(code_text)

        doc_markdown = generate_documentation(code_text, parsed)
        return {"status": "success", "filename": file.filename, "parsed_structure": parsed, "documentation": doc_markdown}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status":"error", "message": str(e)})

class PDFRequest(BaseModel):
    documentation: str
    parsed_structure: dict = {}

@app.post("/generate-pdf/")
async def generate_pdf(req: PDFRequest):
    """
    Create a professional PDF from provided markdown documentation text and parsed structure.
    Returns the PDF file.
    """
    try:
        md = req.documentation
        parsed = req.parsed_structure or {}

        # 1) Create architecture diagram (optional) from parsed structure
        diagram_path = create_arch_diagram(parsed, out_path="backend_arch_diagram.png")

        # 2) Create PDF
        pdf_path = create_pdf_from_markdown(md, parsed, diagram_path, filename="autodoc_documentation.pdf")
        if not pdf_path:
            return JSONResponse(status_code=500, content={"status":"error", "message":"PDF generation failed."})

        return FileResponse(pdf_path, media_type='application/pdf', filename="AutoDoc_documentation.pdf")
    except Exception as e:
        return JSONResponse(status_code=500, content={"status":"error", "message": str(e)})


# import os
# from fastapi import FastAPI, UploadFile, File
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import FileResponse
# from pydantic import BaseModel
# from groq import Groq
# from reportlab.pdfgen import canvas

# from ai_generator import generate_documentation
# from code_parser import parse_code
# from dotenv import load_dotenv
# load_dotenv()

# app = FastAPI()

# # Allow frontend access
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # -------- Upload Endpoint --------
# @app.post("/upload-code/")
# async def upload_code(file: UploadFile = File(...)):
#     try:
#         code_bytes = await file.read()
#         code_text = code_bytes.decode()

#         parsed = parse_code(code_text)
#         documentation = generate_documentation(code_text, parsed)

#         return {
#             "status": "success",
#             "filename": file.filename,
#             "parsed_structure": parsed,
#             "documentation": documentation
#         }

#     except Exception as e:
#         return {"status": "error", "message": str(e)}


# # -------- PDF Download Endpoint --------
# class PDFRequest(BaseModel):
#     text: str

# @app.post("/download-pdf/")
# async def download_pdf(data: PDFRequest):
#     text = data.text
#     filename = "documentation.pdf"

#     c = canvas.Canvas(filename)
#     y = 800

#     for line in text.split("\n"):
#         c.drawString(50, y, line)
#         y -= 20
#         if y < 50:
#             c.showPage()
#             y = 800

#     c.save()
#     return FileResponse(filename, filename=filename)

