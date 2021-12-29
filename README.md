# Minor Project <font size="2">(Under Devlopment)</font> 

- [x] Registration
- [x] Login
- [x] My Profile
- [x] Search Materials
- [x] Upload Materials 
- [x] Unlock Material
- [x] Messaging

### Basic Setup

Installing dependencies
```colsole
> pip install requirements.txt
```


Create necessary environment variable for Database  and Email backend credentials, for example, 
```colsole
> export POSTGRES_NAME=postgres
> export POSTGRES_USER=postgres
> export POSTGRES_PASSWORD=Alcohol#99
> export EMAIL_HOST_USER=useremail@example.com
> export EMAIL_HOST_PASSWORD=ExamplePasswordauers36
```


Configure Channel Layers via the` CHANNEL_LAYERS` Django setting  
In this example, Redis is running on localhost (127.0.0.1) port 6379:
```colsole
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}
```


Create Administrator 
```colsole
> python manage.py createsuperuser
```

Apply Migrations
```colsole
> python manage.py migrate
```


Run the server  
```colsole
> python manage.py runserver
```


To view all all available API endpoints
```console
> python3 -m webbrowser http://127.0.0.1:8000/swagger/
```


<br/>


## Chat Feature
### Here’s an example of Request Header for connecting to the socket
```
Sec-WebSocket-Version: 13
Sec-WebSocket-Key: ny91/tJ2KCCfxC3kSlAN6Q==
Connection: Upgrade
Upgrade: websocket
Authorization: Bearer EXampLeJWtTokEnLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQyOTQ3OTg4LCJpYXQiOjE2NDAzNTU5ODgsImp0aSI6ImRjYmQ2NDY3ZDViNzQ4OWM5NWY1YjBlYTg2NDY1ODY1IiwidXNlcl9pZCI6Mn0.0lBAzYTgdAAOVdM3brZaqv0HXXEApmmxGGtOFnINzJc
Sec-WebSocket-Extensions: permessage-deflate; client_max_window_bits
Host: 127.0.0.1:8000
````
### Joining a Chat
```json
{
    "command": "join_chat",
    "user_id": 1
}
```

### Sending a Message (After Joining a Chat)
```json
{
    "message": "Hello World!"
}
```



