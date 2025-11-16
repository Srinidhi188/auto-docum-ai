from git_reader import get_git_history
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from code_parser import parse_code


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/git-history/")
def git_history():
    history = get_git_history(repo_path="..")  # check project root
    return history

@app.post("/upload-code/")
async def upload_code(file: UploadFile = File(...)):
    try:
        content = await file.read()
        code_text = content.decode("utf-8", errors="ignore")

        # Parse code safely
        parsed = parse_code(code_text)

        return {
            "status": "success",
            "filename": file.filename,
            "parsed_structure": parsed
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
    
