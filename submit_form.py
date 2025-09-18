from flask import Flask, request, render_template, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl # For secure connection
import os

app = Flask(__name__)

# Email configuration
SENDER_EMAIL = os.environ.get ('USER_EMAIL')  # Replace with your email
SENDER_PASSWORD = os.environ.get ('EMAIL_PASS') # Replace with your app password (not your main password)
RECEIVER_EMAIL = "deanp3819@gmail.com" # Replace with the recipient email

@app.route('/')
def contact():
    return render_template('contact.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        #subject = request.form['subject']
        message = request.form['message']

        # Create the email message
        msg = MIMEMultipart("alternative")
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        #msg['Subject'] = f"Contact Form: {subject}"

        # Plain text and HTML versions of the message
        text_content = f"Name: {name}\nEmail: {email}\nMessage: {message}"
        html_content = f"""\
        <html>
            <body>
                <p><strong>Name:</strong> {name}</p>
                <p><strong>Email:</strong> {email}</p>
                
                <p><strong>Message:</strong> {message}</p>
            </body>
        </html>
        """

        part1 = MIMEText(text_content, "plain")
        part2 = MIMEText(html_content, "html")

        msg.attach(part1)
        msg.attach(part2)

        try:
            # Connect to SMTP server (e.g., Gmail)
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
            return "Email sent successfully!"
        except Exception as e:
            return f"Error sending email: {e}"

    return redirect(url_for('contact'))

if __name__ == '__main__':
    app.run(debug=True)