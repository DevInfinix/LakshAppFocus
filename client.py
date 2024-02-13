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
            
            
async def receive_message(socket, role):
    async for message in socket:
        event = json.loads(message)
        if event['type'] == 'error':
            if event['errortype'] == 'SessionNotFound':
                print(event['message'])    
                break
            if event['errortype'] == 'RoomFull':
                print(event['message'])
                break
        if event['type'] == 'started':
            print(f"Your code is: [{event['code']}]")
        if event['type'] == 'joined':
            print(f"You joined {event['code']}")
        if event['type'] == 'message':
            print(event['message'])
        if event['type'] == 'disconnected':
            if event['from'] == 'server':
                if event['role'] == 'host':
                    print('The host has been disconnected')
                    if role == 'host':
                        return
                    else:
                        break
                elif event['role'] == 'member':
                    print('Member disconnected')
                    if role == 'member':
                        return
                    else:
                        pass
                    
                
                
async def start(server_address, username):
    async with websockets.connect(server_address) as socket:
        event = {
            'from': 'client',
            'type': 'start',
            'username': username
        }
        await socket.send(json.dumps(event)) 
        
        send_task = asyncio.create_task(send_message(socket))
        recieve_task = asyncio.create_task(receive_message(socket, 'host'))
        done, pending = await asyncio.wait(
            [send_task, recieve_task],
            return_when=asyncio.FIRST_COMPLETED,
        )
        for task in pending:
            task.cancel()
            
        #await asyncio.gather(send_message(socket), receive_message(socket, 'host'))
        
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
        
        

        await asyncio.gather(receive_message(socket, 'member'))

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
    
