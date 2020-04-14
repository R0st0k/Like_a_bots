from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType,VkBotMessageEvent
import random
import datetime
import request


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
    if True:
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
            File.write(str(curr.date.strftime("%m.%d.%H.%M."))+curr.task+'\n')
            curr = curr.next
    File.close()
    

def createLinkedList():
    File = open('9303.txt', 'r')
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

def newElem(deadLine, head):
    if head and deadLine:
        curr = head
        while(curr):
            if deadLine.date <= curr.date:
                deadLine.next = curr
                head = deadLine
                break
            if deadLine.date >= curr.date and not curr.next:
                curr.next = deadLine
                break
            if deadLine.date >= curr.date and deadLine.date<=curr.next.date:
                deadLine.next = curr.next
                curr.next = deadLine
                break
            curr = curr.next
        logBack(head)
    elif deadLine:
        head = deadLine
        logBack(head)
    return head
    

def removeEl(head, task):
    if head and task:
        curr = head
        if head.task == task:
            head = head.next
            return head
        while(curr.next):
            if curr.next.task == task :
                curr.next=curr.next.next
                break
            curr = curr.next
        logBack(head)
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

def pushNote(head):
    answer = ''
    curr = head
    if curr != None:
        now = datetime.datetime.today()
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
        now = datetime.datetime.today()
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

token = "b212e808e685d53bae44e644ec8970c51ea2bb73c45a781e0c15ca326ed613c37fbd031148241174fc0b1"
vk_session = VkApi(token = token)


session_api = vk_session.get_api()
head = createLinkedList()
group_chat = {'9303' : 2000000001}

while True:
    longpoll = VkBotLongPoll(vk_session, "194170086")
    try:
        head = autoDel(head)
        push = pushNote(head)
        if push != '':
            send_message_chat(session_api, group_chat['9303'], message=push)
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                head = autoDel(head)
                if event.from_user and (event.obj['from_id'] == 176002643 or event.obj['from_id'] == 301186592):
                    response = event.obj['text']
                    if response.find("Удали") == 0:
                        head = removeEl(head, response[6:])
                        continue
                    if response.find("Добавь") == 0:
                        head = newElem(createdeadLine(response[7:]), head)
                        continue
                if event.from_user:
                    message = event.obj['text']
                    response = message.lower()
                    if response.find("андрей сергеевич,") == 0 and (response.find("deadline") != -1 or response.find("дедлайн") != -1 or response.find("срок") != -1):
                        send_message_user(session_api, event.obj['from_id'], message=printLL(head))
                        continue
                if event.from_chat:
                    message = event.obj['text']
                    response = message.lower()
                    if response.find("андрей сергеевич,") == 0 and (response.find("deadline") != -1 or response.find("дедлайн") != -1 or response.find("срок") != -1):
                        send_message_chat(session_api, event.obj['peer_id'], message=printLL(head))
                        continue
    except request.exceptions.ReadTimeout as timeout:
        continue
