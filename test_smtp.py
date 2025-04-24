import smtplib

EMAIL = "testprojecthere147@gmail.com"
PASSWORD = "pigljytandsiskfo"

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL, PASSWORD)
    print("✅ SMTP Authentication Successful!")
    server.quit()
except smtplib.SMTPAuthenticationError as e:
    print("❌ Authentication Failed:", e)
except Exception as e:
    print("❌ Error:", e)
