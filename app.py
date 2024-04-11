from fastapi import FastAPI, Form, UploadFile, File
from typing import Optional, Annotated
from send_email import send_email_via_mailgun
import os


api_key = os.environ.get("MAILGUN_API_KEY")
domain = os.environ.get("DOMAIN")
from_addr = f"{os.environ.get('FROM_USR')}@{domain}"
to_addr = os.environ.get("TO_ADDR")

app = FastAPI()


@app.post("/submit-form/")
async def handle_form_submission(
    name: Annotated[str, Form()],
    phone: Annotated[str, Form()],
    email: Annotated[str, Form()],
    resume: Annotated[UploadFile, File()],
    message: Optional[Annotated[str, Form()]] = None,
):
    file_location = f"./{resume.filename}"

    with open(file_location, "wb") as file_object:
        file_object.write(resume.file.read())

    # Send an email with the form data
    subject = f"New Employment Application from {name}"
    text = f"""
    Name: {name}
    Phone: {phone}
    Email: {email}
    Message: {message}
    """

    send_email_via_mailgun(api_key, domain, from_addr, to_addr, subject, text, file_location)

    # remove the file after sending the email
    os.remove(file_location)

    return "Form submitted successfully! We will get back to you soon."
