import requests
from .cookies import CookieLoader, CookiesSaver
from .credientials import CredentialsLoader, Credientials

class AuthProvider:
    def __init__(
        self, 
        cookies_loader: CookieLoader,
        cookies_saver: CookiesSaver,
        credientials_loader: CredentialsLoader
    ) -> None:
        self._cookies_loader = cookies_loader
        self._cookies_saver = cookies_saver
        self._credientials_loader = credientials_loader
        
    def get_cookies(self, username: str) -> dict[str, str]:
        cookies = self._cookies_loader.load(username)
    
        if not self._is_valid_cookies(cookies):
            print('Invalid cookies. Logging in...')
            credientials = self._credientials_loader.load(username)
            cookies = self._login(credientials)
            self._cookies_saver.save(username, cookies)
            
        if not self._is_valid_cookies(cookies):
            print('Login failed.')
            raise ValueError('Invalid username or password.')
        
        return cookies.get_dict()

    
    def _is_logged_in(self, session: requests.Session) -> bool:
        req = session.get('https://mail.guc.edu.eg/owa/', allow_redirects=False)
        return req.text.find('Inbox') != -1


    def _is_valid_cookies(self, cookies: requests.cookies.RequestsCookieJar) -> bool:
        if cookies is None:
            return False
        
        print('Checking cookies...')
        session = requests.Session()
        session.cookies.update(cookies)
        return self._is_logged_in(session)
    
        
    def _login(self, credientials: Credientials) -> requests.cookies.RequestsCookieJar:
        session = requests.Session()
        
        session.post('https://mail.guc.edu.eg/owa/auth.owa', data = {
            'flags': 4,
            'destination': 'https://mail.guc.edu.eg/owa/',
            "forcedownlevel": "0",
            'username': credientials.username,
            'password': credientials.password
        })
        
        return session.cookies
