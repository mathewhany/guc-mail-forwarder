import os
import bs4
from kafka import KafkaConsumer
import requests
import requests.utils
import requests.cookies
from config import EnvVarsConfigLoader

BASE_URL = 'https://mail.guc.edu.eg/owa/'

def get_authenticated_session(
    username: str,
    authenticator_url: str
) -> requests.Session:
    response = requests.post(authenticator_url + '/auth/' + username)
    if response.status_code != 200:
        raise ValueError('Invalid username or password.')
    data = response.json()
    cookies = requests.utils.cookiejar_from_dict(data['cookies'])
    session = requests.Session()
    session.cookies.update(cookies)
    return session

def forward_email(session, mail_id, forward_to):
    print(f"Forwarding mail {mail_id} to {forward_to}")
    
    url_encoded_mail_id = requests.utils.quote(mail_id)
    read_url = f"{BASE_URL}?ae=PreFormAction&t=IPM.Note&a=Forward&id={url_encoded_mail_id}"
    response = session.get(read_url)
    
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    
    inputs = {
        input['name']: input['value']
        for input in soup.select('input')
        if input.has_attr('name') and input.has_attr('value')
    }
    print(response.text)
    print(soup.select_one('#txtbdyldr'))
    print(soup.select_one('#txtsbjldr'))
    inputs["txtbdy"] = soup.select_one('#txtbdyldr').text
    inputs["txtsbj"] = soup.select_one('#txtsbjldr')['value']
    inputs['txtto'] = forward_to
    inputs['hidcmdpst'] = 'snd'
    
    forward_url = f"{BASE_URL}?ae=PreFormAction&t=IPM.Note&a=Send"
    response = session.post(forward_url, data=inputs)
    
    if response.status_code != 200:
        raise ValueError('Failed to forward email.')
    
    print(f"Forwarded mail {mail_id} to {forward_to}")

def main():
    config_loader = EnvVarsConfigLoader()
    config = config_loader.load_config()
    
    kafkaConsumer = KafkaConsumer(
        'mail_ids', 
        bootstrap_servers=config.kafka_bootstrap_servers, 
        group_id='mail_forwarder', 
        value_deserializer=lambda v: v.decode('utf-8'),
        enable_auto_commit=False,
        auto_offset_reset='earliest'
    )
    username = config.username    
    session = get_authenticated_session(username, config.authenticator_url)
    
    print('Waiting for messages...')
    
    for msg in kafkaConsumer:
        mail_id = msg.value
        forward_email(session, mail_id, config.forward_to_mail)
        
        
if __name__ == '__main__':
    main()
    
