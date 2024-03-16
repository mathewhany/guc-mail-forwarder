from .auth_provider import AuthProvider
from .cookies import JsonCookieLoader, JsonCookieSaver
from .credientials import EnvVarCredentialsLoader
from .server import create_server

file_path = 'cookies.json'
auth_provider = AuthProvider(
    cookies_loader=JsonCookieLoader(file_path),
    cookies_saver=JsonCookieSaver(file_path),
    credientials_loader=EnvVarCredentialsLoader()
)

server = create_server(auth_provider)

if __name__ == '__main__':
    server.run(host='')
    
