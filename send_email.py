import requests
def send_email_via_mailgun(api_key, domain, from_addr, to_addr, subject, text, attachment):
    """
    Send an email using the Mailgun API.

    Parameters:
    - api_key (str): Mailgun API key.
    - domain (str): Mailgun domain.
    - from_addr (str): Sender's email address.
    - to_addr (str or list): Recipient's email address or a list of addresses.
    - subject (str): Email subject.
    - text (str): Body of the email.
    - attachment (str): Path to the file to attach.
    """

    # Prepare the data for the API request
    data = {
        "from": from_addr,
        "to": to_addr,
        "subject": subject,
        "text": text,
    }

    # Make the request to Mailgun API
    response = requests.post(
        f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api", api_key),
        data=data,
        files=[("attachment", open(attachment, "rb"))],
    )

    # Check the response
    if response.status_code == 200:
        print("Email sent successfully!")
    else:
        print(f"Failed to send email. Status code: {response.status_code}, Response: {response.text}")

if __name__ == "__main__":
    pass
#    from dotenv import dotenv_values
#
#    config = dotenv_values(".env")
#
#    # Example usage
#    api_key = config["MAILGUN_API_KEY"]
#    domain = config["DOMAIN"]
#    from_addr = f"{config['FROM_USR']}@{domain}"
#    to_addr = config["TO_ADDR"]
#
#    subject = "Hello from Mailgun"
#    text = "This is a test email sent via Mailgun from a Python script."
#
#    send_email_via_mailgun(api_key, domain, from_addr, to_addr, subject, text)
