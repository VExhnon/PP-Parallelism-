import asyncio

# Хранилище для подключений клиентов
clients = []


# Асинхронная функция для обработки клиента
async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"New connection from {addr}")
    clients.append(writer)

    try:
        while True:
            data = await reader.read(100)
            if not data:
                break
            message = data.decode()
            print(f"Received {message} from {addr}")

            # Рассылаем сообщение всем подключенным клиентам
            for client in clients:
                if client != writer:
                    client.write(f"{addr}: {message}".encode())
                    await client.drain()
    except asyncio.CancelledError:
        pass
    finally:
        print(f"Connection closed from {addr}")
        clients.remove(writer)
        writer.close()
        await writer.wait_closed()


# Запуск асинхронного сервера
async def run_server():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 8888)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(run_server())
