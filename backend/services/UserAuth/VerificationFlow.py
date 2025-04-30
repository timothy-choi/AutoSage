from itsdangerous import URLSafeTimedSerializer
import os
import requests


serializer = URLSafeTimedSerializer(os.process.env.SECRET_KEY)

def generate_verification_token(email):
    return serializer.dumps(email, salt="email-verification")

def send_verification_email(email):
    try:
        token = generate_verification_token(email)

        verification_url = f"http://localhost:5000/UserAuthProcess/verify_email/token={token}"

        response = requests.post(
            "http://localhost:5000/send_email",
            json={
                "email": email,
                "subject": "Email Verification",
                "message": f"Please verify your email by clicking the link: {verification_url}"
            }
        )
        
        if response.status_code != 200:
            raise Exception("Failed to send verification email")
    except Exception as e:
        raise Exception(str(e))
    
def verify_email_token(token):
    try:
        email = serializer.loads(token, salt="email-verification", max_age=1800)

        user_info = requests.get("/Users/email/" + email)

        if user_info.status_code != 200:
            raise Exception("User not found")
        
        requests.put("/UserAuth/is_verified/" + user_info.json().get('userAuth_id'))
    except Exception as e:
        raise Exception("Invalid or expired token")