from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll
import random
import datetime
import re


class deadLine:
    def __init__(self, date, task):
        self.date = date
        self.task = task
        self.next = None

def send_message_chat(session_api, id, message=None, attachment=None, keyboard=None):
    session_api.messages.send(peer_id = id, message = message, random_id = random.randint(-2147483648, +2147483648), attachment = attachment, keyboard = keyboard)
    
def send_message_user(session_api, id, message=None, attachment=None, keyboard=None):
    session_api.messages.send(user_id = id, message = message, random_id = random.randint(-2147483648, +2147483648), attachment = attachment, keyboard = keyboard)

def createdeadLine(input_line):
    if re.fullmatch(r'([1-9]|0[1-9]|1[0-2])\.([1-9]|[012][0-9]|3[0-1])\.([0-9]|[01][0-9]|2[0-3])\.([0-9]|[0-5][0-9])\..+', input_line):
        true_line = input_line.split('.')
        date = datetime.datetime(2020, int(true_line[0]), int(true_line[1]), int(true_line[2]), int(true_line[3]))
        new = deadLine(date, true_line[4])
        return new
    else:
        return None

def logBack(head):
    File = open('9303.txt', 'w')
    if head:
        curr = head
        while curr:
            File.write(str(curr.date.strftime("%m.%e.%H.%M."))+curr.task+'\n')
            curr = curr.next
    File.close()
    

def createLinkedList():
    try:
        File = open('9303.txt', 'r')
    except FileNotFoundError:
        File = open('9303.txt', 'w')
        return None
    Tasks = [line.strip() for line in File]
    if Tasks == []:
        File.close()
        return None
    else:
        head = createdeadLine(Tasks[0])
        Tasks.remove(Tasks[0])
    curr = head
    while Tasks:
        new = createdeadLine(Tasks[0])
        curr.next = new
        curr = new
        Tasks.remove(Tasks[0])
    File.close()
    return head


def pushNote(head):
    answer = ''
    curr = head
    if curr != None:
        now = datetime.datetime.today() + datetime.datetime(0, 0, 0, 3, 0)
        delta = curr.date - now
    else:
        return answer
    one = False
    three = False
    while delta.days == 0:
        if not one:
            answer = answer+'Сроки, до которых меньше 1 дня:\n'
            one = True
        answer = answer+str(curr.date.strftime("%d.%m %H:%M - "))+curr.task+'\n'
        if curr.next != None:
            curr = curr.next
            delta = curr.date - now
        else:
            return answer
    if one:
        answer = answer + '\n'
    while 1 <= delta.days <= 2:
        if not three :
            answer = answer+'Сроки, до которых меньше 3 дней:\n'
            three = True
        answer = answer+str(curr.date.strftime("%d.%m %H:%M - "))+curr.task+'\n'
        if curr.next != None:
            curr = curr.next
            delta = curr.date - now
        else:
            return answer
    return answer

def autoDel(head):
    if(head):
        now = datetime.datetime.today() + datetime.datetime(0, 0, 0, 3, 0)
        curr = head
        while curr.date <= now: 
            if(curr.next):
                curr = curr.next
                head = head.next
            else:
                head = None
                break
        logBack(head)
    return head    

#login, password = "", ""
#vk_session = vk_api.VkApi(login, password, scope = 'messages')
#vk_session.auth()

token = ""
vk_session = VkApi(token = token)


session_api = vk_session.get_api()
head = createLinkedList()
group_chat = {'9303' : 2000000001}

head = autoDel(head)
push = pushNote(head)
if push != '':
    send_message_chat(session_api, group_chat['9303'], message=push)
