class message:

    def __init__(self ,data: dict):
        self.data = data

    @property
    def update_id(self):
        return self.data['update_id']
    
    @property
    def message_id(self):
        return self.data['message']['message_id']
    
    @property
    def author_id(self):
        return self.data['message']['from']['id']
    
    @property
    def is_bot(self):
        return self.data['message']['from']['is_bot']
    
    @property
    def author_first_name(self):
        return self.data['message']['from']['first_name']
    
    @property
    def author_last_name(self):
        return self.data['message']['from']['last_name']
    
    @property
    def author_username(self):
        return self.data['message']['from']['username']
    
    @property
    def chat_id(self):
        return self.data['message']['chat']['id']
    
    @property
    def chat_type(self):
        return self.data['message']['chat']['type']
    
    @property
    def chat_title(self):
        return self.data['message']['chat']['title']
    
    @property
    def is_reply(self):
        if 'reply_to_message' in self.data['message']:
            return True
        else:
            return False
        
    @property
    def reply_message_id(self):
        if 'reply_to_message' in self.data['message']:
            return self.data['message']['reply_to_message']['message_id']
        else:
            return False
        
    @property
    def reply_data(self):
        if 'reply_to_message' in self.data['message']:
            return self.data['message']['reply_to_message']
        else:
            return False
    
    @property
    def is_forward(self):
        if 'forward_from' in self.data['message']:
            return True
        elif 'forward_from_chat' in self.data['message']:
            return True
        else:
            return False
        
    @property
    def forward_from_id(self):
        if 'forward_from' in self.data['message']:
            return self.data['message']['forward_from']['id']
        elif 'forward_from_chat' in self.data['message']:
            return self.data['message']['forward_from_chat']['id']
        else:
            return None

    @property
    def forward_from_message_id(self):
        if 'forward_from_message_id' in self.data['message']:
            return self.data['message']['forward_from_message_id']
        else:
            return None
        
    @property
    def forward_from_is_bot(self):
        if 'forward_from' in self.data['message']:
            return self.data['message']['forward_from']['is_bot']
        else:
            return None
        
    @property
    def forward_from_is_bot(self):
        if self.is_forward:
            return self.data['message']['forward_from']['is_bot']
        else:
            return None
    
    @property
    def text(self):
        if 'text' in self.data['message']:
            return self.data['message']['text']
        elif 'caption' in self.data['message']:
            return self.data['message']['caption']
        else:
            return None

    @property
    def file_data(self):
        if 'photo' in self.data['message']:
            return self.data['message']['photo']
        elif 'video' in self.data['message']:
            return self.data['message']['video']
        elif 'document' in self.data['message']:
            return self.data['message']['document']
        elif 'audio' in self.data['message']:
            return self.data['message']['audio']
        else:
            return None
    
    @property
    def message_type(self):
        if 'text' in self.data['message']:
            return 'text'
        elif 'photo' in self.data['message']:
            if 'caption' in self.data['message']:
                return 'photoCaption'
            else:
                return 'photo'
        elif 'video' in self.data['message']:
            if 'caption' in self.data['message']:
                return 'videoCaption'
            else:
                return 'video'
        elif 'document' in self.data['message']:
            if 'caption' in self.data['message']:
                return 'documentCaption'
            else:
                return 'document'
        elif 'audio' in self.data['message']:
            if 'caption' in self.data['message']:
                return 'audioCaption'
            else:
                return 'audio'
        else:
            return None