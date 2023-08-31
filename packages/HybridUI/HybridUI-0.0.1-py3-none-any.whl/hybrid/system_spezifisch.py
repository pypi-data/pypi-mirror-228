from fastapi import FastAPI
from fastapi_socketio import SocketManager
from . import globals
import json

globals.app=app=FastAPI()
socket_manager = SocketManager(app=app, mount_location='/hybrid/', json=json)
globals.sio=sio=socket_manager._sio

 