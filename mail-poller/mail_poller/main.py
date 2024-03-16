import bs4
from kafka import KafkaProducer
import requests
import requests.utils
import requests.cookies
import config
from redis import Redis

BASE_URL = 'https://mail.guc.edu.eg/owa/'

def get_authenticated_session(
    username: str
) -> requests.Session:
    response = requests.post(config.authenticator_url + '/auth/' + username)
    if response.status_code != 200:
        raise ValueError('Invalid username or password.')
    data = response.json()
    cookies = requests.utils.cookiejar_from_dict(data['cookies'])
    session = requests.Session()
    session.cookies.update(cookies)
    return session
    

def count_mail_pages(
    session: requests.Session
) -> int:
    res = session.get('https://mail.guc.edu.eg/owa/')
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    pages = soup.select('.pTxt')
    return len(pages)


def get_mail_ids(session: requests.Session, page: int) -> list[str]:
    res = session.get(f"{BASE_URL}?pg={page}")
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    
    mails = [
        checkbox['value'] 
        for checkbox in soup.select('input[name="chkmsg"]')
    ]
    
    return mails
        

redis = Redis(host=config.redis_host, port=config.redis_port, decode_responses=True)
kafkaProducer = KafkaProducer(
    bootstrap_servers=config.kafka_bootstrap_servers,
    value_serializer=lambda v: v.encode('utf-8')
)

def main():
    username = config.guc_username 
    session = get_authenticated_session(username)
    pages_count = count_mail_pages(session)
    
    for page in range(pages_count):
        for mail_id in get_mail_ids(session, page):
            if redis.sismember('mail_ids', mail_id):
                print("Skipping", mail_id)
                continue
            
            print("Sending", mail_id)
            redis.sadd('mail_ids', mail_id)
            kafkaProducer.send('mail_ids', mail_id)
    
    print("Flushing...")
    kafkaProducer.flush()
    print("Flushed!")
            
        
if __name__ == '__main__':
    main()
    
