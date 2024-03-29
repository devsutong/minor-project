﻿# Study Material Sharing Platform

> - [x] Registration   
> - [x] Login  
> - [x] Create profile  
> - [x] Browse materials
> - [x] Browse Users     
> - [x] Search materials  
> - [x] Upload materials and earn Unlocks  
> - [x] Unlock a material  
> - [x] Upvote or Downvote a material  
> - [x] Chat with other users and/or send attachments
 
### Technologies used
<hr>

> - Django
> - REST API
> - Postgresql
> - Redis 
> - Channels
> - Web Sockets

### Basic Setup
<hr>

Installing dependencies
```colsole
> pip install -r requirements.txt
```

Setup System Environments (Example)
```colsole
> export POSTGRES_NAME=poStGRes
> export POSTGRES_USER=poStGRes
> export POSTGRES_PASSWORD=eXampleP4ssW0rd
> export EMAIL_HOST_USER=examplemail@domain.com
> export EMAIL_HOST_PASSWORD=eXampleP4ssW0rd
```

Setup Redis, Database and Email Backend in [setting.py](minorproject/settings.py)


Migrate Models  
```colsole
> python manage.py makemigrations
> python manage.py migrate
```

Create Administrator 
```colsole
> python manage.py createsuperuser
```

Run the server  
```colsole
> python manage.py runserver
```
To view all all available API endpoints
```console
> python -m webbrowser http://127.0.0.1:8000/swagger/
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
<br>

## What's not covered 
<hr>

> - Notification features


