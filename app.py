from fastapi import FastAPI, Form, UploadFile, File
from typing import Optional, Annotated
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("MAILGUN_API_KEY")
DOMAIN = os.environ.get("DOMAIN")
FROM_ADDR = f"{os.environ.get('FROM_USR')}@{DOMAIN}"
TO_ADDR = os.environ.get("TO_ADDR")

app = FastAPI()

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
        print("Email sent successfully!")
    else:
        print(f"Failed to send email. Status code: {response.status_code}, Response: {response.text}")


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

    send_email_via_mailgun(subject, text, resume.filename, file_contents)

    return "Form submitted successfully! We will get back to you soon."

if __name__ == "__main__":
    pass
