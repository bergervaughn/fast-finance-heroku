import smtplib
from email.message import EmailMessage


HOST = "smtp.gmail.com"
PORT = 587
from_email = "fastfinancereply@gmail.com"
PASSWORD = "qtsw szhh aoju phpv"

# to_email = ["bergervaughn@gmail.com", "croberson3518@gmail.com",
#            "montgomeryrussell2000@gmail.com", "trevorcaffrey@gmail.com"]
# subject = "Test SMTP Email"
# body = """
# It is with great pleasure that I would like to announce that our backend can now send emails.
# """
#
# msg = EmailMessage()
# msg['Subject'] = subject
# msg['From'] = from_email
# msg['To'] = ",".join(to_email)
#
# msg.set_content(body)

# with smtplib.SMTP(HOST, PORT) as smtp:
#     smtp.starttls()
#     smtp.login(from_email, PASSWORD)
#     smtp.sendmail(from_email, to_email, msg.as_string())


def send_email(recipient, subject, message):
    """
    Function that takes a list of recipients, a subject, and a message body as input and composes and sends
    an email to the specified list of recipients.

    If the list contains only 1 recipient, then it will handle that accordingly.
    Returns and error message if any of the fields are empty or if the SMTP fails.
    If there are no errors, then it returns "The Email was sent successfully!"

    :param recipient: the list of recipient emails
    :param subject: the subject line of the email
    :param message: the body of the email
    :return: the result of sending the email
    """

    if "" in recipient or subject == "" or message == "":
        return "Error! Recipient, Subject, or Body of Email are empty."

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_email
    if len(recipient) == 1:  # if the email has only one recipient
        recipient = recipient[0]  # turns the list 'recipient' into a single string for later
        msg['To'] = recipient
    else:
        msg['To'] = ",".join(recipient)
    msg.set_content(message)

    with smtplib.SMTP(HOST, PORT) as smtp:
        try:
            smtp.starttls()
            smtp.login(from_email, PASSWORD)
            smtp.sendmail(from_email, recipient, msg.as_string())
        except smtplib.SMTPException as e:
            return f"Email failed to send: {e}"

    return "Email sent successfully!"
