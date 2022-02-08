from typing import NamedTuple
from os import getenv
import requests
from time import sleep
from db import add_chat_info

url = "https://dev.wapp.im/v3/"

headers = {
  'X-Tasktest-Token': getenv("TOKEN")
}


class Chat(NamedTuple):
    chat_id: int
    chat_token: str

class UserInfo(NamedTuple):
    name: str
    phone: str


def get_chat() -> Chat:
    """Получаем чат"""
    r = requests.get(url + "chat/spare?crm=TEST&domain=test", headers=headers)
    r_json = r.json()
    print(r_json)
    return Chat(chat_id=r_json["id"],
                chat_token=r_json["token"])


def get_qr(chat: Chat) -> None:
    """получаем QR code"""
    r = requests.get(url + f"instance{chat.chat_id}/qr_code?token={chat.chat_token}", headers=headers)
    with open("qr_code.html", "w") as file:
        file.write(r.text)
    print(r.text)


def get_status(chat: Chat) -> str:
    """Получаем статус аккаунта"""
    r = requests.get(url + f"instance{chat.chat_id}/status?full=1&token={chat.chat_token}", headers=headers)
    print(r.text)
    r_json = r.json()
    return r_json["accountStatus"]
  

def get_me(chat: Chat) -> UserInfo:
    """Получаем инфо о пользователе"""
    r = requests.get(url + f"instance{chat.chat_id}/me?token={chat.chat_token}", headers=headers)
    r_json = r.json()
    return UserInfo(name=r_json["name"],
                    phone=r_json["number"])


def send_message(chat: Chat, phone: str) -> None:
    """Отправляем сообщения"""
    payload={
        'phone': '79872745052' ,
        'body': 'Hello, World!',
        'quotedMsgId': '',
        'sendSeen': '1',
        'typeMsg': 'text',
        'latitude': '35.227221',
        'longitude': '25.249377',
        'title': 'Название ',
        'footer': 'Подвал'
    }
    r = requests.post(url + f"instance{chat.chat_id}/sendMessage?token={chat.chat_token}", headers=headers, data=payload)
    print(r.text)



def main():
    try:
        chat = get_chat()
    except Exception:   
        print("Нет свободных чатов")
        return

    status = get_status(chat)
    while status != "authenticated":
        if status == "got qr code":
            get_qr(chat)
            sleep(10)
        status = get_status(chat)
    
    user_info = get_me(chat)
    add_chat_info(chat=chat, user=user_info)
    send_message(chat, user_info.phone)

if __name__ == '__main__':
    main()