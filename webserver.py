import asyncio
import websockets
import json
#from async_files import FileIO
import secrets
import signal


HOST = '0.0.0.0'
PORT = 8080

ROOMS = {}

# d = {
#     'type': 'message',
#     'from': 'client',
#     'code': 'test',
#     'role': 'host',
#     'username': 'testuser',
#     'message': 'testmessage'
# }

# ERRORS = [
#     'SessionNotFound',
#     'RoomFull'
# ]

# EVENTS = ['start', 'started', 'join', 'joined', 'message', 'disconnected']

async def error(socket, errortype, msg):
    event = {
        'type': 'error',
        'from': 'server',
        'errortype': errortype,
        'message': msg
    }
    await socket.send(json.dumps(event))
    
async def start(socket, host):
    join_code = secrets.token_urlsafe(12)
    ROOMS[join_code] = {'host': socket}
    
    try:
        event = {
            'type': 'started',
            'from': 'server',
            'code': join_code
        }
        await socket.send(json.dumps(event))
        print(f'[{join_code}] Host ({host}) started')
        
        async for message in socket:
            message = json.loads(message)
            
            if message['type'] == 'message':
                print(f"[{join_code}] Host sent: {message['message']}")
                forward_event = {
                    'type': 'message',
                    'from': 'server',
                    'code': join_code,
                    'message': message['message'],
                    'user': host
                }
                websockets.broadcast(list(ROOMS[join_code].values()), json.dumps(forward_event))
                
    finally:
        event = {
            'type': 'disconnected',
            'from': 'server',
            'code': join_code,
            'user': host,
            'role': 'host'
        }
        websockets.broadcast(list(ROOMS[join_code].values()), json.dumps(event))
        print(f"[{join_code}] | Host disconnected")
        del ROOMS[join_code]
    
    
    
async def join(socket, join_code, member):
    try:
        ROOM = ROOMS[join_code]
    except:
        await error(socket, 'SessionNotFound', 'Session not found.')
        return
        
    if len(list(ROOM.values())) >= 2:
        await error(socket, 'RoomFull', 'The room is full.')
        return
        
    ROOM['member'] = socket
    
    try:
        event = {
            'type': 'joined',
            'from': 'server',
            'code': join_code
        }
        await socket.send(json.dumps(event))
        print(f'[{join_code}] Member ({member}) joined')
        
        async for message in socket:
            message = json.loads(message)
            if message['type'] == 'message':
                print(f"[{join_code}] Member sent: {message['message']}")
                forward_event = {
                    'type': 'message',
                    'from': 'server',
                    'code': join_code,
                    'message': message['message'],
                    'user': member
                }
                websockets.broadcast(list(ROOM.values()), json.dumps(forward_event))
    finally:
        event = {
            'type': 'disconnected',
            'from': 'server',
            'code': join_code,
            'user': member,
            'role': 'member'
        }
        websockets.broadcast(list(ROOM.values()), json.dumps(event))
        print(f"[{join_code}] | Member disconnected")
        del ROOM['member']
        
        
async def handler(socket):
    try:
        message = await socket.recv()
        event = json.loads(message)
        if event['from'] == 'client':
            user = event['user']
            if event['type'] == 'start':
                await start(socket, user)
            if event['type'] == 'join':
                await join(socket, event['code'], user)
    except:
        for ROOM in ROOMS:
            for key, value in ROOMS[ROOM].items():
                if value == socket:
                    event = {
                        'type': 'disconnected',
                        'from': 'server',
                        'code': ROOM,
                        'role': key
                    }
                    websockets.broadcast(list(ROOMS[ROOM].values()), json.dumps(event))
                    print(f"[{ROOM}] {key} disconnected")
                    if key == 'host':
                        del ROOMS[ROOM]
                    else:
                        del ROOMS[ROOM]['member']
        

async def main():
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)
    
    async with websockets.serve(handler, HOST, PORT, ping_interval=5, ping_timeout=None):
        print('Server started on {HOST}:{PORT}')
        await stop

if __name__=="__main__":
    asyncio.run(main())