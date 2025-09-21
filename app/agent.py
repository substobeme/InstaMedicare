import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(user_email, rec_id, name, age, problem, drugs):
    sender_email = "xxxx"
    sender_password = "xxxx" 

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = user_email
    message["Subject"] = f"Prescription Details - Receipt {rec_id}"

    body = f"""
Prescription Details:

Receipt ID: {rec_id}
Name: {name}
Age: {age}
Problem: {problem}
Recommended Drugs: {', '.join(drugs)}
"""
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, user_email, message.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")
