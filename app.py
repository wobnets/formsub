from fastapi import FastAPI, Form, UploadFile, File
from typing import Optional, Annotated
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
print(f"ORIGINS: {ORIGINS}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def send_email_via_mailgun(subject, text, filename, file_content):
    print(f"ORIGINS: {ORIGINS}")
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
        return "Form submitted successfully! We will get back to you soon."
    else:
        return f"Failed to send email. Status code: {response.status_code}, Response: {response.text}"


@app.post("/submit-form/")
async def handle_form_submission(
    name: Annotated[str, Form()],
    phone: Annotated[str, Form()],
    email: Annotated[str, Form()],
    resume: Annotated[UploadFile, File()],
    message: Optional[Annotated[str, Form()]] = None,
):
    file_contents = await resume.read()

    # send email
    subject = f"New Employment Application from {name}"
    text = f"""
    Name: {name}
    Phone: {phone}
    Email: {email}
    Message: {message}
    """

    return send_email_via_mailgun(subject, text, resume.filename, file_contents)


if __name__ == "__main__":
    pass
