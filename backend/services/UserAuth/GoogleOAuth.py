import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi import Request
from fastapi.encoders import jsonable_encoder
import redis
import requests
from google.auth.transport.requests import Request as GoogleRequest
from google.auth import exceptions
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from datetime import timedelta

app = FastAPI()

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

SCOPES = []
flow = Flow.from_client_secrets_file(
    'YOUR_CLIENT_SECRETS_FILE.json',
    scopes=SCOPES,
    redirect_uri="YOUR_REDIRECT_URI"
)

def get_session(request: Request):
    return request.session

@app.get("/AuthError")
async def auth_error():
    return JSONResponse(content={"message": "Authentication failed. Please try again."}, status_code=400)

@app.post("/Login")
async def login():
    try:
        authorization_url, state = flow.authorization_url(prompt='consent')
        return RedirectResponse(url=authorization_url)
    except Exception as e:
        return RedirectResponse(url='/AuthError')

@app.post("/OAuth2Callback")
async def OAuth2Callback(request: Request):
    try:
        if request.query_params.get('state') != request.cookies.get('state'):
            raise Exception("State mismatch detected")
        
        flow.fetch_token(authorization_response=str(request.url))

        id_info = id_token.verify_oauth2_token(flow.credentials.id_token, GoogleRequest(), 'YOUR_CLIENT_ID')

        user_id = id_info['sub']
        user_email = id_info['email']
        user_name = id_info.get('name')

        user_info = requests.get("/Users/email/" + user_email)

        if user_info.status_code != 200:
            user_auth_info = requests.post("/UserAuth", json={
                "user_id": user_id,
                "email": user_email,
                "name": user_name,
                "google_oauth": {
                    "id_token": flow.credentials.id_token,
                    "access_token": flow.credentials.token,
                    "refresh_token": flow.credentials.refresh_token
                }
            })

            user_info = requests.post("/Users", json={
                "user_id": user_id,
                "email": user_email,
                "name": user_name,
                "user_auth_id": user_auth_info.json().get('id')
            })

            user_auth_id = user_auth_info.json().get('id')

            requests.put("/UserAuth/user_id/${user_auth_id}/${user_id}")

        session_data = {
            'user_id': user_id,
            'email': user_email,
            'name': user_name
        }

        session_id = os.urandom(24).hex()
        request.session['session_id'] = session_id
        request.session['user'] = session_data
        request.session['tokens'] = {
            'access_token': flow.credentials.token,
            'refresh_token': flow.credentials.refresh_token
        }

        redis_client.setex(session_id, timedelta(days=1), str(jsonable_encoder(request.session)))

        return JSONResponse(content={"message": "Auth successful", "user": session_data, "tokens": request.session['tokens'], "user_id": user_info.id}, status_code=201)
    except Exception as e:
        return RedirectResponse(url='/AuthError')

@app.post("/RefreshToken")
async def refresh_token(request: Request):
    try:
        if 'tokens' not in request.session or 'refresh_token' not in request.session['tokens']:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authenticated")
        
        refresh_token = request.session['tokens'].get('refresh_token')
    
        if not refresh_token:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No refresh token available")
        
        data = {
            'client_id': 'YOUR_CLIENT_ID',
            'client_secret': 'YOUR_CLIENT_SECRET',
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token'
        }

        response = requests.post('https://oauth2.googleapis.com/token', data=data)

        if response.status_code == 200:
            new_tokens = response.json()
            request.session['tokens']['access_token'] = new_tokens.get('access_token')
            redis_client.setex(request.session['session_id'], timedelta(days=1), str(jsonable_encoder(request.session)))
            
            return JSONResponse(content={"message": "Token refreshed successfully", "access_token": request.session['tokens']['access_token']})
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to refresh token")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to refresh token")

@app.get("/IsAuthenticated")
async def is_authenticated(request: Request):
    try:
        if 'user' not in request.session or 'tokens' not in request.session:
            raise HTTPException(status_code=status.HTTP_200_OK, detail="Authenticated: False")

        if redis_client.get(request.session.get('session_id')):
            access_token = request.session['tokens'].get('access_token')

            if access_token:
                response = requests.get(f'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}')
                
                if response.status_code == 200:
                    return JSONResponse(content={"authenticated": True})
                else:
                    return JSONResponse(content={"authenticated": False})
            
            return JSONResponse(content={"authenticated": False})

        return JSONResponse(content={"authenticated": False})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to verify: {str(e)}")

@app.post("/Logout")
async def logout(request: Request):
    try:
        if 'tokens' in request.session and 'access_token' in request.session['tokens']:
            access_token = request.session['tokens']['access_token']
            revoke_url = "https://oauth2.googleapis.com/revoke"
            requests.post(revoke_url, params={'token': access_token})

        redis_client.delete(request.session.get('session_id'))
        request.session.clear()
        
        return RedirectResponse(url="https://accounts.google.com/Logout")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to logout: {str(e)}")