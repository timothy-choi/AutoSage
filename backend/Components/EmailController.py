from flask import Flask, jsonify, request
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['MAIL_SERVER'] = ''
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = ''  
app.config['MAIL_PASSWORD'] = ''  
app.config['MAIL_DEFAULT_SENDER'] = ''

mail = Mail(app)

def send_user_email_helper(subject_value, recipients, message):
    try:
        msg = Message(
            subject=subject_value,
            recipients=recipients,  
            body=message,
        )
        
        mail.send(msg)
    except Exception as e:
        raise Exception(str(e))

def send_group_email_helper(subject_value, bcc_emails, message):
    try:
        msg = Message(
            subject=subject_value,
            recipients=[],  
            bcc=bcc_emails,  
            body=message
        )

        mail.send(msg)
    except Exception as e:
        raise Exception(str(e))

@app.route("/sendUserEmail", methods=['POST'])
def send_user_email():
    try:
        subject = request.json.get("subject")
        email = request.json.get("email")
        message = request.json.get("message")

        recipients = [email]

        send_user_email_helper(subject, recipients, message)

        return jsonify({"message": "email sent"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/sendGroupEmail", methods=['POST'])
def send_group_email():
    try:
        subject = request.json.get("subject")
        all_emails = request.json.get("emails")
        message = request.json.get("message")

        send_group_email_helper(subject, all_emails, message)

        return jsonify({"message": "email sent"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500