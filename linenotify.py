import requests

class Message:
    __all__ = [
        'message',
        'imageThumbnail',
        'imageFullsize',
        'imageFile',
        'stickerPackageId',
        'stickerId',
        'notificationDisabled',
    ]
    
    def __init__(self, *args, **kwargs):
        for index, value in enumerate(args):
            setattr(self, self.__all__[index], value)
        for key, value in kwargs.items():
            assert not hasattr(self, key), '\'%s\' already set' % (key)
            assert key in self.__all__, '\'%s\' is invaild args' % (key)
            setattr(self, key, value)

class LineNotify:
    API_URL = 'https://notify-api.line.me/'
    BASE_URL = 'https://notify-bot.line.me/'
    
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Host': 'notify-bot.line.me',
        'Referer': 'https://notify-bot.line.me/my/'
    }

    class Personal:
        def __init__(self, XSRF_TOKEN, SESSION_ID):
            self.XSRF_TOKEN = XSRF_TOKEN
            self.session = requests.session()
            for key, value in {'XSRF-TOKEN': XSRF_TOKEN, 'SESSION': SESSION_ID}.items():
                self.session.cookies.set_cookie(requests.cookies.create_cookie(key, value))
            self.session.headers = LineNotify.HEADERS.copy()
            
        def request(self, method, path, params={}, data=None, json=None):
            return getattr(self.session, method)(LineNotify.BASE_URL + path, params=params, data=data, json=json)

        def getGroupList(self, page=1):
            return self.request('get', 'api/groupList', {'page': page}).json()

        def issueLineNotifyAccessToken(self, name, targetMid, targetType="GROUP"):
            data = {
                "action": "issuePersonalAcessToken",
                "description": name,
                "targetType": targetType,
                "targetMid": targetMid,
                "_csrf": self.XSRF_TOKEN
            }
            return self.request('post', 'my/personalAccessToken', data=data).json()

        def createLineNotifyByGroupName(self, groupName, name):
            group_id = ([group['mid'] for group in self.getGroupList()['results'] if group['name'] == groupName] + [None])[0]
            assert group_id, 'no matched group name'
            return LineNotify.Client(self.issueLineNotifyAccessToken(name, group_id)['token'])

        def logout(self):
            return self.request('post', 'logout', {'_csrf': self.XSRF_TOKEN})

    class Client:
        def __init__(self, access_token):
            self.session = requests.session()
            self.session.headers = LineNotify.HEADERS.copy()
            self.session.headers.update({'Authorization': 'Bearer %s' % (access_token)})

        def request(self, method, path, params={}, data=None, json=None):
            return getattr(self.session, method)(LineNotify.API_URL + path, params=params, data=data, json=json)

        def sendMessage(self, message):
            assert isinstance(message, Message), 'message must be Message, not %s' % (type(message).__name__)
            return self.request('post', 'api/notify', message.__dict__).json()

        def revokeToken(self):
            return self.request('post', 'api/revoke').json()

if __name__ == '__main__':
    personal = LineNotify.Personal('03573c3a-xxxx-xxxx-xxxx-0902dec44a97', 'NTdkOGQyOWQtZDYxxxxxxxxxxxFmMmMtMWU1M2Q5MWE5YzZl')
    client = personal.createLineNotifyByGroupName('GROUP_NAME', 'NAME')
    client.sendMessage(Message('Hi'))
    client.revokeToken()
