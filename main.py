import asyncio
import websockets
import json


async def receive_and_store(websocket, path):
    try:
        # Open the file for appending
        with open("data.json", "a") as file:
            while True:
                # Receive JSON data from the client
                data = await websocket.recv()
                json_data = json.loads(data)
                if "getAll" in json_data:
                            # Send the contents of the file when the command is "getAll"
                            with open("data.json", "r") as file2:
                                print("Data sending")
                                file_contents = file2.read()
                                await websocket.send(file_contents)
                else:



                    # Append the received data to the list of transactions
                    with open("data.json", "r") as file_read:
                        file_data = json.load(file_read)
                        file_data["Transactions"].append(json_data)

                    # Write the updated JSON data back to the file
                    with open("data.json", "w") as file2:
                        json.dump(file_data, file2)

                    print("Data received and stored")

    except websockets.exceptions.ConnectionClosed:
        pass


start_server = websockets.serve(receive_and_store, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
