from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api
import random
import datetime

class DeadLine:
    def __init__(self, date, task):
        self.date = date    
        self.task = task
        self.next = NULL
     
def send_message(vk_session, id_type, id, message=None, attachment=None, keyboard=None):
    vk_session.method('messages.send',{id_type: id, 'message': message, 'random_id': random.randint(-2147483648, +2147483648), "attachment": attachment, 'keyboard': keyboard})

def createLinkedList(): 
    head = DeadLine(datetime.datetime(today.year, 04, 30, 23, 59), "Дискретная математика - Задания от Рыбина")
    return head

def newElem(deadLine, head):
    curr = head
    while(curr):   #Проход по списку 
        if deadLine.date <= curr.date:
            deadLine.next = curr
            head = deadLine
            brake            
        if deadLine.date >= curr.date and not curr.next:
            curr.next = deadLine
            brake
        if deadLine.date >= curr.date and deadline.date<=curr.next.date:
            deadLine.next = curr.next
            curr.next = deadLine
            break
        curr = curr.next

def removeEl(head, task):
    curr = head
    if head.task == task:
        head = head.next
        return
    while(curr.next):
        if curr.next.task == task : 
            curr.next=curr.next.next
            break
        curr = curr.next        
                
def printLL(head):
    curr = head
    answer = 'Так-так:\n'
    while(curr):
        answer=answer+str(datetime.strftime(curr.date, "%d.%m %H:%M - "))+curr.task+'\n'
        curr = curr.next
    return answer

login, password = "", ""
vk_session = vk_api.VkApi(login, password)
vk_session.auth()

session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
head = createlinkedlist()

while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW
            response = event.text.lower()
            if event.from_chat:
                if response.find("андрей сергеевич,") == 0 and (response.find("дедлайны") != -1 or response.find("дедлайн") != -1 or response.find("сроки") != -1):
                    send_message(vk_session, 'chat_id', event.chat_id, message=printLL(head))
            if event.from_user and (event.user_id == '176002643' or event.user_id == '301186592'):
                responseMes = response.split('.')      
                date = datetime.datetime(today.year, int(responseMes[0]), int(responseMes[1]), int(responseMes[2]), int(responseMes[3]))
                new = DeadLine(date, responseMes[4])
                newElem(new, head)
            if event.from_user and (event.user_id == '176002643' or event.user_id == '301186592'):
                if response.find("удали") == 0:
                    removeEl(head, response[6:])