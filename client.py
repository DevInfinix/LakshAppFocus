import asyncio
import websockets
import json

async def send_message(socket):
    while True:
        message = input(">>> ")
        if message == 'exit':
            break
        data = {
            'from': 'client',
            'type': 'message',
            'message': message
        }
        await socket.send(json.dumps(data))
            
            
async def receive_message(socket):
    print('okkkkkkkkkkkkkk')
    async for message in socket:
        event = json.loads(message)
        if event['type'] == 'error':
            if event['errortype'] == 'SessionNotFound':
                print(event['message'])       
        if event['type'] == 'started':
            print(f"Your code is: [{event['code']}]")
        if event['type'] == 'joined':
            print(f"You joined {event['code']}")
        if event['type'] == 'message':
            print(event['message'])
        
async def start(server_address, username):
    async with websockets.connect(server_address) as socket:
        event = {
            'from': 'client',
            'type': 'start',
            'username': username
        }
        await socket.send(json.dumps(event))  # Send username
        
        # async def receive_message():
        #     async for message in socket:
        #         print(message)

        await asyncio.gather(send_message(socket), receive_message(socket))
        
async def join(server_address, code, username):
    async with websockets.connect(server_address) as socket:
        event = {
            'from': 'client',
            'type': 'join',
            'code': code,
            'username': username
        }
        await socket.send(json.dumps(event))  # Send username
        
        # async def receive_message():
        #     async for message in socket:
        #         print(message)

        await asyncio.gather(receive_message(socket))

if __name__ == '__main__':
    server_address = 'ws://localhost:8080'
    inp = input('Do you want to (s)tart or (j)oin the session?\n>>> ')
    if inp == 's':
        username = input("\nEnter username:\n>>> ")
        asyncio.run(start(server_address, username))
    if inp == 'j':
        code = input("\nEnter code:\n>>> ")
        username = input("\nEnter username:\n>>> ")
        asyncio.run(join(server_address, code, username))
    
