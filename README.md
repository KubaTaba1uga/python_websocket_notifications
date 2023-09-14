# Python Websocket Notifications 
Create http service for managing websocket channels, updating data embedded into an app.

Mechanism for notifications need to be inline with [SPEC](https://github.com/KubaTaba1uga/python_websocket_notifications/blob/main/OMA-TS-REST_NetAPI_NotificationChannel-V1_0-20200319-C.pdf).  

## Requirements
We need some data to subscribe so, let's create subscription for movies. Wouldn't You like to know when the next premiere is being moved? 

Successfull app flow:
1. Create any sql db 
2. Create table for movies
3. Populate Data with movies
4. Read table data to python
5. Convert data to JSON
6. Create channel for movies notification
7. Receive websocket subscription data (?? not included in specs ??)
8. Subscribe movies (?? not included in specs ??)
9. Modify data of any movie 
10. Receive notification


## Stack
HTTP SERVER - [aiohttp](https://docs.aiohttp.org/en/stable/index.html) <br>
SQL - [sqlalchemy](https://www.sqlalchemy.org/) <br>
WEBSOCKET - [websockets](https://websockets.readthedocs.io/en/stable/index.html) <br>
TESTS - [pytest](https://docs.pytest.org/en/7.4.x/) <br> 

## Movies U(CRUD)
Let's give websocket client capability to trigger notification.
Other letters of CRUD (beside U) are optional.

## Notification Channel API 
Implementing whole API is mandatory. Users or api version can be mocked.
![image](https://github.com/KubaTaba1uga/python_websocket_notifications/assets/73971628/9688771e-ee31-46cd-930b-bc2a59eddf18)


## Create Notification Channel
![image](https://github.com/KubaTaba1uga/python_websocket_notifications/assets/73971628/078a1421-27e3-4720-800e-a0f937c975d6)

## Deliver Notification
![image](https://github.com/KubaTaba1uga/python_websocket_notifications/assets/73971628/44b5ed83-3b08-4b8c-ab75-85fc733e4dcb)
