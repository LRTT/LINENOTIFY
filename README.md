# LINE NOTIFY

Example
------------
Personal
```python
from linenotify import LineNotify, Message
personal = LineNotify.Personal('03573c3a-xxxx-xxxx-xxxx-0902dec44a97', 'NTdkOGQyOWQtZDYxxxxxxxxxxxFmMmMtMWU1M2Q5MWE5YzZl')
client = personal.createLineNotifyByGroupName('GROUP_NAME', 'NAME')
client.sendMessage(Message('Hi'))
client.revokeToken()
```
Client
```python
from linenotify import LineNotify, Message
client = LineNotify.Client('TOKEN')
client.sendMessage(Message('Hi'))
```

Installation
------------
```shell
$ pip3 install -r requirements.txt
```
