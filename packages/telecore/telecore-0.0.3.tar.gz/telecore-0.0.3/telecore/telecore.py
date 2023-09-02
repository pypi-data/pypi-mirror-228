#!/usr/bin/env python3
"""
telecore
~~~~~~~~~

this library for telegram and it created with telegram api

```
from telecore.telecore import TeleCore
```

"""

# go to linkdoonies and search group links, join to groups and send the banner and left the chat

import requests 

class Errors:
    def emptyToken(__value):
        if __value == None:
            raise ValueError("The Token cannot be Empty")
        else:pass
        
    def emptyParams(__values : list):
        for _v in __values:
            if _v == None:
                raise ValueError(f"you set some parameters to empty\nlenght of it: {_v}")
            else:pass


class TeleCore:
    def __init__(self, BotToken : str, printData : False = None, proxies = None) -> dict:
        self.token = str(BotToken)
        self.api = f"https://api.telegram.org/bot{self.token}"
        self.gpt = "https://haji-api.ir/Free-GPT3/?text="
        self.printData = printData
        self.header = {'Content-Type': 'Application/json', 'Accept': 'Application/json'}
        self.proxy = proxies
        
    def sendMessage(self, text : str = None, chatID : str = None, messageID : str = None, parseMode : str = None):
        Errors.emptyToken(self.token)
        Errors.emptyParams([text , chatID])
        if (self.printData == False or self.printData == None):
            return dict(requests.post(f"{self.api}/sendMessage?chat_id={chatID}&text={text}&reply_to_message_id={messageID if not messageID == None else ''}&parse_mode={parseMode if not parseMode == None else ''}",headers=self.header, proxies=self.proxy).json())
            
        elif self.printData == True:
            print(f"token: {self.token}")
            print(f"api: {self.api}")
            print(f'method: sendMessage')
            print(f"header: {self.header}")
            print(f'text: {text}')
            print(f'chat id: {chatID}')
            print(f'message id: {messageID}')
            print(f'parseMode: {parseMode}')

            return dict(requests.post(f"{self.api}/sendMessage?chat_id={chatID}&text={text}&reply_to_message_id={messageID if not messageID == None else ''}&parse_mode={parseMode if not parseMode == None else ''}", headers=self.header, proxies=self.proxy).json())
       
    def getMe(self):
        Errors.emptyToken(self.token)
        if (self.printData == False or self.printData == None):
            while 1:
                try:
                    return dict(requests.post(f"{self.api}/getMe", headers=self.header, proxies=self.proxy).json())
                    break
                except Exception as e: 
                    return e
                    break
                
        else:
            print(f"token: {self.token}")
            print(f"api: {self.api}")
            print(f'method: getMe')
            print(f"header: {self.header}")
            while 1:
                try:
                    return dict(requests.post(f"{self.api}/getMe", headers=self.header, proxies=self.proxy).json())
                    break
                except Exception as e: 
                    return e
                    break
            
    def forwardMessage(self, chatID : str = None, fromChatID : str = None, messageID : str = None):
        Errors.emptyToken(self.token)
        Errors.emptyParams([chatID, fromChatID, messageID])
        if (self.printData == False or self.printData == None):
            while 1:
                try:
                    return dict(requests.post(f"{self.api}/forwardMessage?chat_id={chatID}&from_chat_id={chatID}&message_id={messageID}", headers=self.header, proxies=self.proxy).json())
                    break
                except Exception as e:
                    return e 
                    break
                
        else:
            print(f"token: {self.token}")
            print(f"api: {self.api}")
            print(f'method: forwardMessage')
            print(f"header: {self.header}")
            print(f'chat id: {chatID}')
            print(f'from chat id: {fromChatID}')
            print(f'message id: {messageID}')
            while 1:
                try:
                    Data = {
                        "chat_id" : chatID,
                        'from_chat_id' : fromChatID,
                        'message_id' : messageID
                    }
                    return dict(requests.post(f"{self.api}/forwardMessage", data=Data, headers=self.header, proxies=self.proxy).json())
                    break
                except Exception as e:
                    return e 
                    break
                
    def getUpdates(self):
        Errors.emptyToken(self.token)
        if (self.printData == False or self.printData == None):
            while 1:
                try:
                    return dict(requests.post(f"{self.api}/getUpdates", headers=self.header, proxies=self.proxy).json())
                    break
                except Exception as e:
                    return e 
                    break
        
        else:
            print(f"token: {self.token}")
            print(f"api: {self.api}")
            print(f'method: getUpdates')
            print(f"header: {self.header}")
            while 1:
                try:
                    return dict(requests.post(f"{self.api}/getUpdates", headers=self.header, proxies=self.proxy).json())
                    break
                except Exception as e:
                    return e 
                    break
                
    def sendPhoto(self, pathOfPhotoOrNamePhoto : str = None, chatID : str = None, messageID : str = None, caption : str = None):
        Errors.emptyToken(self.token)
        Errors.emptyParams([chatID, pathOfPhotoOrNamePhoto])
        while 1:
            try:
                return dict(requests.post(f"{self.api}/sendPhoto?file_id={pathOfPhotoOrNamePhoto}&chat_id={chatID}&caption={caption if not caption == None else ''}&reply_to_message_id={messageID if not messageID == None else ''}", proxies=self.proxy, headers=self.header).json())
            except Exception as er2:
                return er2
            
    
    def sendAudio(self, pathOfAudioOrNameAudio : str = None, chatID : str = None, messageID : str = None, caption : str = None):
        Errors.emptyToken(self.token)
        Errors.emptyParams([pathOfAudioOrNameAudio, chatID])
        while 1:
            try:
                return dict(requests.post(f"{self.api}/sendAudio?file_id={pathOfAudioOrNameAudio}&chat_id={chatID}&caption={caption if not caption == None else ''}&reply_to_message_id={messageID if not messageID == None else ''}", headers=self.header, proxies=self.proxy).json())
            except Exception as er3:
                return er3 
            
    def sendDocument(self, pathOfDocOrNameOfDoc : str = None, chatID : str = None, messageID : str = None, caption : str = None):
        Errors.emptyToken(self.token)
        Errors.emptyParams([pathOfDocOrNameOfDoc, chatID])
        while 1:
            try:
                return dict(requests.post(f"{self.api}/sendDocument?file_id={pathOfDocOrNameOfDoc}&chat_id={chatID}&caption={caption if not caption == None else ''}&reply_to_message_id={messageID if not messageID == None else ''}", headers=self.header, proxies=self.proxy).json())
            except Exception as er4:
                return er4 
    
    def sendVideo(self, pathOfVideoOrNameOfVideo : str = None, chatID : str = None, messageID : str = None, caption : str = None):
        Errors.emptyToken(self.token)
        Errors.emptyParams([pathOfVideoOrNameOfVideo, chatID])
        while 1:
            try:
                return dict(requests.post(f"{self.api}/sendVideo?chat_id={chatID}&file_id={pathOfVideoOrNameOfVideo}&reply_to_message_id={messageID if not messageID == None else ''}&caption={caption if not caption == None else ''}", headers=self.header, proxies=self.proxy).json())
            except Exception as er5:
                return er5
            
    def sendVoice(self, pathOfVoiceOrNameOfVoice : str = None, chatID : str = None, messageID : str = None, caption : str = None):
        Errors.emptyToken(self.token)
        Errors.emptyParams([pathOfVoiceOrNameOfVoice, chatID])
        while 1:
            try:
                return dict(requests.post(f"{self.api}/sendVoice?file_id={pathOfVoiceOrNameOfVoice}&chat_id={chatID}&caption={caption if not caption == None else ''}&reply_to_message_id={messageID if not messageID == None else ''}", headers=self.header, proxies=self.proxy).json())
            except Exception as er6:
                return er6
            
    def starterHandler(self, starterText  = None ,helpHandle : bool = False):
        """
        When a user type `/start` or `/help` , robot was send a starter Text
        
        you can set your text in `starterText` parameter and you can add `/help` with set helpHandle to True.
        """
        Errors.emptyToken(self.token)
        Errors.emptyParams([starterText])
        if helpHandle == True:
            try:
                UP = self.getUpdates().get('result')[-1].get('message')
                if UP.get('text') == '/start' or UP.get('text') == '/help':
                    self.sendMessage(text=starterText, chatID=UP.get('chat').get('id'), messageID=UP.get('message_id') if UP.get('message_id') else '')
            except Exception as ESH:
                pass
                return ESH
            
        elif helpHandle == False:
            try:
                UP = self.getUpdates().get('result')[-1].get('message')
                if UP.get('text') == '/start' :
                    self.sendMessage(text=starterText, chatID=UP.get('chat').get('id'), messageID=UP.get('message_id') if UP.get('message_id') else '')
            except Exception as ESH2:
                pass
                return ESH2
        
        else:pass
        
    def responeText(self, targetText : str = '/'):
        """
        When a User start with a `/` or anything in `targetText` parameter, robot get all of the sentence in front of `/` or anything in `targetText` parameter
        """
        Errors.emptyToken(self.token)
        Errors.emptyParams([targetText])
        try:
            UP = self.getUpdates().get('result')[-1].get('message')
            text = str(UP.get('text'))
            if text.startswith(targetText):
                return text.replace(f'{targetText}', '')
            
        except Exception as ERT:
            pass
            return ERT
        
        
    def sendItAgain(self, starter : str = None):
        """
        When a User message, start with anything in `starter` parameter, robot get all of sentence in front of anything in `starter` and the robot send it back to user.
        """
        Errors.emptyToken(self.token)
        Errors.emptyParams([starter])
        try:
            UP = self.getUpdates().get('result')[-1].get('message')
            text = str(UP.get('text'))
            if text.startswith(starter):
                stData = text.replace(f"{starter}", '')
                self.sendMessage(text=stData, chatID=UP.get('chat').get('id'), messageID=UP.get('message_id') if UP.get('message_id') else '')
        except Exception as ESIA:
            pass
            return ESIA
        
        
    def sendItToMyPV(self, adminChatIDs : list | str = None):
        """
        When a User send a message in pv of admins, robot send him/her message to admin PVs
        """
        Errors.emptyToken(self.token)
        Errors.emptyParams([adminChatIDs])
        try:
            UP = self.getUpdates().get('result')[-1].get('message')
            fromWhat = UP.get('from')
            name = fromWhat.get('first_name')
            _chatID = fromWhat.get('id')
            msgID = UP.get('message_id')
            text = str(UP.get('text'))
            
            if text:
                if type(adminChatIDs) == list:
                    for acis in adminChatIDs:
                        self.sendMessage(text=f'NewMessage !\n\nfrom: {name}\nchatID: {_chatID}\nmessage: {text}', chatID=acis)
                        self.sendMessage(text='your message sent in my Admin(s) PVs', chatID=_chatID, messageID=msgID if msgID else '')
                else:
                    self.sendMessage(text=f'NewMessage !\n\nfrom: {name}\nchatID: {_chatID}\nmessage: {text}', chatID=adminChatIDs)
                    self.sendMessage(text='your message sent in my Admin(s) PVs', chatID=_chatID, messageID=msgID if msgID else '')
        except Exception as ESITMPV:
            pass
            return ESITMPV
        
        
    def searchAndLink(self, searchChats : list | str = None, textToSend : str = None, chatGPT : bool = False):
        """
        Robot go to gaps and find IDs of members (everyone are send a message) and send a banner in PVs
        
        just need to chat ids of gaps for search in it 
        
        the special option of this robot is turning on it chat gpt
        
        you can set your banner in `textToSend` parameter.
        """
        
        Errors.emptyToken(self.token)
        Errors.emptyParams([searchChats, textToSend])
        try:
            UP = self.getUpdates().get('result')[-1].get('message')
            text = str(UP.get('text'))
            msg_id = UP.get('message_id')
            fromWhat = UP.get('from_user')
            chatID = fromWhat.get('id')
            numsToSend = 0
            
            if chatID:
                numsToSend =+ 1
                self.sendMessage(text=textToSend, chatID=chatID)
                print(f'sended => {numsToSend}')
                if chatGPT == True:
                    if text.startswith('/gpt'):
                        dataGPT = text.replace("/gpt ", "")
                        dataHaji = dict(requests.post(self.gpt+dataGPT+"&key=hajiapi", headers=self.header).json())
                        messasge = dataHaji.get('result').get('message')
                        self.sendMessage(text=messasge, chatID=chatID, messageID=msg_id)
                else:pass
                
        except Exception as ESAL:
            pass
            return ESAL
