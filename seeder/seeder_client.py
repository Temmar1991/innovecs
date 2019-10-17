from socketIO_client import SocketIO, LoggingNamespace
import time
socket = SocketIO('http://localhost', 9000, LoggingNamespace)
socket.emit('Ping')
socket.wait()
