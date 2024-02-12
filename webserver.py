import asyncio
import websockets
import json
#from async_files import FileIO
import secrets

HOST = '0.0.0.0'
PORT = 8080

USERS = {}

d = {
    'type': 'message',
    'from': 'client',
    'code': 'test',
    'role': 'host',
    'username': 'testuser',
    'message': 'testmessage'
}

ERRORS = [
    'CodeExists',
    'CodeNotFound',
    'ConnectionClosed',
]

async def error(socket, errortype, msg):
    event = {
        'type': 'error',
        'from': 'server',
        'errortype': errortype,
        'message': msg
    }
    await socket.send(json.dumps(event))

EVENTS = ['start', 'started', 'join', 'joined', 'message']

async def start(socket, host):
    join_code = secrets.token_urlsafe(12)
    connected = {socket}
    USERS[join_code] = connected
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
                for USER in USERS[join_code]:
                    forward_event = {
                        'type': 'message',
                        'from': 'server',
                        'message': f"[{join_code}] | [{host}]: {message['message']}"
                    }
                    await USER.send(json.dumps(forward_event))
    finally:
        print(connected)
        del USERS[join_code]
    
async def join(socket, join_code, member):
    try:
        connected = USERS[join_code]
    except:
        await error(socket, 'SessionNotFound', 'Session not found.')
    connected.add(socket)
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
                print(USERS[join_code])
                async for USER in USERS[join_code]:
                    await USER.send(f"[{join_code}] | [{member}]: {message['message']}")
    finally:
        connected.remove(socket)
        print(connected)
        
        
async def handler(socket):
    try:
        message = await socket.recv()
        event = json.loads(message)
        if event['from'] == 'client':
            user = event['username']
            if event['type'] == 'start':
                await start(socket, user)
            if event['type'] == 'join':
                await join(socket, event['code'], user)
    except:
        print(USERS)
        print(f"{socket} disconnected")
        
    # async for message in socket:
    #     event = json.loads(message)
    #     fr = event['from']
        
    #     if fr == 'client':
    #         eventtype = event['type']
    #         code = event['code']
    #         role = event['role']
    #         uname = event['username']
    #         msg = event['message']

    #         if eventtype == 'start':
    #             result = await start(socket, code, role, uname, msg)
    #             if not result:
    #                 continue
                
        

async def main():
    async with websockets.serve(handler, HOST, PORT):
        print('Server started on {HOST}:{PORT}')
        await asyncio.Future()

if __name__=="__main__":
    asyncio.run(main())