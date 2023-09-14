# Python Websocket Notifications 
## Requirements
We need some data to subscribe so, let's create subscription for movies. Wouldn't You like to know when the next premiere is being moved? 

So in quick summary:
1. Create any sql db 
2. Create table for movies
3. Populate Data with movies
4. Read table data to python
5. Convert data to JSON
6. Create channel for movies notification
7. Modify data of any movie 
8. Receive notification

SQL - [sqlalchemy](https://www.sqlalchemy.org/) <br>
WEBSOCKET - [websockets](https://websockets.readthedocs.io/en/stable/index.html) <br>
TESTS - [pytest](https://docs.pytest.org/en/7.4.x/) <br> 

## Movies U(CRUD)
Let's give websocket client capability to trigger notification.
Other letters of CRUD (beside U) are optional.

## Notification Channel API 
![image](https://github.com/KubaTaba1uga/python_websocket_notifications/assets/73971628/9688771e-ee31-46cd-930b-bc2a59eddf18)


## Create Notification Channel
![image](https://github.com/KubaTaba1uga/python_websocket_notifications/assets/73971628/078a1421-27e3-4720-800e-a0f937c975d6)

## Deliver Notification
![image](https://github.com/KubaTaba1uga/python_websocket_notifications/assets/73971628/44b5ed83-3b08-4b8c-ab75-85fc733e4dcb)
