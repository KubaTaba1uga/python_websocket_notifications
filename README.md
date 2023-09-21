# Python Websocket Notifications 
Create http service for managing websocket channels.
To make testsing easier, CRUD for app's data, can be implemented.

Managin channel has to be inline with [SPEC](https://github.com/KubaTaba1uga/python_websocket_notifications/blob/main/OMA-TS-REST_NetAPI_NotificationChannel-V1_0-20200319-C.pdf).  

## Example overview
Chat service. Message is composed of Body, From and To. Nothing fancy.

##  Solution overview
Subscriptions are part of MessageStore. However channels(notifications) should be seperated into a service. 

### Channel creation
1. User makes post to notificationsservice /<usr_id>/channels
2. Server returns: callbackURL (address where message store should proxy requests), channelURL (websocket url)

### Subscription creation
1. User makes post to messagestore /subscriptions (with callbackURL)
2. Server add callbackURL to notifications proxies urls list 
3. Server returns subscription data

### Proxying reuest
1. Server eceives any request
2. If request matches change createrium it is being proxy to notification server
3. Server processes request further
4. Server returns response

Message store makes obj dump (if request qualifies for change tracing) and sends it to NotificationService tohetger with user id (box id). <br>
NotificationService downloads all subscriptions for specific user, if there is a match sends obj_dump to specific channel queue. <br>
Websocket have two modes: broadcasting live or replaying past. <br>
If websocket is broadcasting live, channel's queue is popped to recive a message. <br>
If websocket is replaying from past, search is being performed to recive messages. <br>



### Some notes:

1. Create endpoint for managing subscriptions <br>
   1.1 New subscription require callback reference (WS channel URI) <br>
   1.2 RestartToken should be object's lat edit timestamp (more info in 5.1.4.3.1) <br>
   1.3 Creating a subscription -> creating a worker <br>
   1.4 What should trigger new notification in worker? (SQL change? then some kind of search query > sql converter is needed? )<br>
3. Create enpoint for managing channels <br>
4. [Optional] Create endpoint for updating app's data <br>


Bullet points from `Appendix I Notification delivery using WebSockets`:
1. Create Subprotocol Registration in Sec-WebSocket-Protocol
2. do not implement connCheck/connAck in application layer (at this point)
3. Use notificationList for all notifications, this way mechanism is more generic
4. NotificationChannel data structure includes a “channelURL” element which provides a URI of scheme “ws:” or “wss:”(this URI mechanism is descrybed further).

Bullet points from 5.1.4 in NMS API (to fullfill).
1. A box represents the logical store that belongs to designated owner(s).
2. To subscribe to NMS notifications, create a new resource under http://{serverRoot}/nms/{apiVersion}/{storeName}/{boxId}/subscriptions
![image](https://github.com/KubaTaba1uga/python_websocket_notifications/assets/73971628/36737ef5-28b8-494e-8b1e-b0c56db82021)

## Stack
HTTP SERVER - [aiohttp](https://docs.aiohttp.org/en/stable/index.html) <br>
SQL - [sqlalchemy](https://www.sqlalchemy.org/) <br>
WEBSOCKET - [websockets](https://websockets.readthedocs.io/en/stable/index.html) <br>
TESTS - [pytest](https://docs.pytest.org/en/7.4.x/) <br> 


## Quick Summary
![image](https://github.com/KubaTaba1uga/python_websocket_notifications/assets/73971628/3e31b2e5-fe51-475e-a61c-77f62d800de7)

## Notification Channel API 
Implementing whole API is mandatory. Users or api version can be mocked.
![image](https://github.com/KubaTaba1uga/python_websocket_notifications/assets/73971628/9688771e-ee31-46cd-930b-bc2a59eddf18)


## Create Notification Channel
![image](https://github.com/KubaTaba1uga/python_websocket_notifications/assets/73971628/078a1421-27e3-4720-800e-a0f937c975d6)

## Deliver Notification
![image](https://github.com/KubaTaba1uga/python_websocket_notifications/assets/73971628/44b5ed83-3b08-4b8c-ab75-85fc733e4dcb)

## Manage Subscription
![image](https://github.com/KubaTaba1uga/python_websocket_notifications/assets/73971628/9851ebc8-db0f-4643-b774-b242ebc75404)

## What should be first? Subscription or Channel?
![image](https://github.com/KubaTaba1uga/python_websocket_notifications/assets/73971628/14ce62fe-ef94-47a6-9956-d92140dfa05c)

## What is CallbackURL?
![image](https://github.com/KubaTaba1uga/python_websocket_notifications/assets/73971628/f9394868-5cb1-40bc-9821-e1a403f063e8)
![image](https://github.com/KubaTaba1uga/python_websocket_notifications/assets/73971628/258a244c-8ffa-458b-b315-ff50bebb6326)
![image](https://github.com/KubaTaba1uga/python_websocket_notifications/assets/73971628/7f5888bd-f2d7-4642-bd1b-8931906ad324)
Let's assume for a moment that callback URL points to some <channel>/ws on the server. Then server uses that info to determine that all messages connected to this subscription should be sent to the cleint via this ws.
This makes sense however it is in conflict with ## How i see relation between Subscription and Channel. I'm not sure yet which one is correct.


