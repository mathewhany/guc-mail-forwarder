from fastapi import FastAPI, HTTPException
from .auth_provider import AuthProvider

def create_server(
    auth_provider: AuthProvider
) -> FastAPI:
    app = FastAPI()

    @app.post('/auth/{username}')
    def authenticate(username: str):
        try:
            cookies = auth_provider.get_cookies(username)
            return { 'cookies': cookies }
        except ValueError as e:
            raise HTTPException(status_code=401, detail=str(e))
    
    return app
