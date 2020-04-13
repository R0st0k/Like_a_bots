import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import datetime


class deadLine:
    def __init__(self, date, task):
        self.date = date
        self.task = task
        self.next = None

def send_message(vk_session, id_type, id, message=None, attachment=None, keyboard=None):
    vk_session.method('messages.send',{id_type: id, 'message': message, 'random_id': random.randint(-2147483648, +2147483648), "attachment": attachment, 'keyboard': keyboard})

def createLinkedList():
    head = DeadLine(datetime.datetime(2023, 5, 31, 23, 59), "Дипломная работа")
    return head

def newElem(deadLine, head):
    if(head):
        curr = head
        while(curr):
            if deadLine.date <= curr.date:
                deadLine.next = curr
                head = deadLine
                break
            if deadLine.date >= curr.date and not curr.next:
                curr.next = deadLine
                break
            if deadLine.date >= curr.date and deadline.date<=curr.next.date:
                deadLine.next = curr.next
                curr.next = deadLine
                break
            curr = curr.next
    else:
        head = deadLine
    return head
    

def removeEl(head, task):
    if(head):
        curr = head
        if head.task == task:
            head = head.next
            return head
        while(curr.next):
            if curr.next.task == task :
                curr.next=curr.next.next
                break
            curr = curr.next
    return head

def printLL(head):
    answer = 'Так-так:\n'
    if(head):
        curr = head
        while(curr):
            answer=answer+str(curr.date.strftime("%d.%m %H:%M - "))+curr.task+'\n'
            curr = curr.next
    else:
        answer = 'Так это, у вас ничего нет'
    return answer
    
def autoDel(head):
    if(head):
        now = datetime.now()
        curr = head
        while curr.date <= now and 
            if(curr.next):
                curr = curr.next
                head = head.next
            else:
                head = None
                break
    return head    

#login, password = "", ""
#vk_session = vk_api.VkApi(login, password, scope = 140488159)
#vk_session.auth()

token = ""
vk_session = vk_api.VkApi(token = token)


session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
head = createLinkedList()

while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
            head = autoDel()
            if event.from_user and (event.user_id == 176002643 or event.user_id == 301186592):
                response = event.text
                if response.find("Удали") == 0:
                    removeEl(head, response[6:])
                    continue
                if response.find("Добавь") == 0:   
                    responseMes = response[7:].split('.')
                    date = datetime.datetime(2020, int(responseMes[0]), int(responseMes[1]), int(responseMes[2]), int(responseMes[3]))
                    new = deadLine(date, responseMes[4])
                    newElem(new, head)
            if event.from_chat:
                response = event.text.lower()
                if response.find("андрей сергеевич,") == 0 and (response.find("дедлайны") != -1 or response.find("дедлайн") != -1 or response.find("сроки") != -1):
                    send_message(vk_session, 'chat_id', event.chat_id, message=printLL(head))
