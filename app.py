from fastapi import FastAPI, Form, UploadFile, File
from typing import Annotated
from fastapi.responses import JSONResponse
import os
import requests
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

API_KEY = os.environ.get("MAILGUN_API_KEY")
DOMAIN = os.environ.get("DOMAIN")
FROM_ADDR = f"{os.environ.get('FROM_USR')}@{DOMAIN}"
TO_ADDR = os.environ.get("TO_ADDR")

app = FastAPI()

ORIGINS = list(str(os.environ.get("ORIGINS")).split(","))

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

def send_email_via_mailgun(subject, text, filename, file_content):
    url = f"https://api.mailgun.net/v3/{DOMAIN}/messages"

    auth=("api", f"{API_KEY}")

    files=[("attachment", (filename, file_content))]

    data = {
        "from": FROM_ADDR,
        "to": TO_ADDR,
        "subject": subject,
        "text": text,
    }

    response = requests.post(url, auth=auth, data=data, files=files)

    if response.status_code == 200:
        return {"message": "Form submitted successfully! We will get back to you soon."}
    else:
        return {"error": f"Failed to send email. Status code: {response.status_code}, Response: {response.text}"}

@app.post("/submit-form/")
async def handle_form_submission(
    name: Annotated[str, Form()],
    phone: Annotated[str, Form()],
    email: Annotated[str, Form()],
    resume: Annotated[UploadFile, File()],
    position: Annotated[str, Form()],
    message: Annotated[str, Form()],
):
    valid_types = [
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    ]

    if resume.content_type not in valid_types:
        return JSONResponse(status_code=400, content={"error": "Invalid file type. Please upload a PDF or Word document."})

    file_contents = await resume.read()
    if len(file_contents) > 10485760:
        return JSONResponse(status_code=400, content={"error": "File size too large. Please upload a file smaller than 10MB."})


    # send email
    subject = f"Application from {name} for {position} position"
    text = f"""
    Position: {position}
    Name: {name}
    Phone: {phone}
    Email: {email}
    Message: {message}
    """
    print(text)

    email_response = send_email_via_mailgun(subject, text, resume.filename, file_contents)

    if "error" in email_response:
        return JSONResponse(status_code=500, content=email_response)
    else:
        return JSONResponse(content=email_response)

    #return JSONResponse(content={"message": "Form submitted successfully! We will get back to you soon."})

if __name__ == "__main__":
    pass
