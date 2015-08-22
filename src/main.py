# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import asyncio
from asyncio import coroutine
from functools import partial
import ssl

# <codecell>

from config import SERVER, CLIENT

# <codecell>

@coroutine
def relay(reader, writer, loop):
    try:
        while not reader.at_eof():
            data = yield from reader.read(4096)
            writer.write(data)
            yield from writer.drain()
    except Exception as e:
        pass
    writer.close()

# <codecell>

@coroutine
def tcp2ssl(reader_c, writer_c, loop, addr, hostname, ssl, password):
    try:
        reader_s, writer_s = yield from asyncio.open_connection(*addr, loop=loop, ssl=ssl,
                                                                server_hostname=hostname)
        writer_s.write(password)
    except Exception as e:
        return
    asyncio.async(relay(reader_c, writer_s, loop), loop=loop)
    asyncio.async(relay(reader_s, writer_c, loop), loop=loop)

# <codecell>

@coroutine
def ssl2tcp(reader_c, writer_c, loop, addr, password):
    try:
        reader_s, writer_s = yield from asyncio.open_connection(*addr, loop=loop)
        data = yield from reader_c.readexactly(len(password))
    except Exception as e:
        return
    if data == password:
        asyncio.async(relay(reader_c, writer_s, loop), loop=loop)
        asyncio.async(relay(reader_s, writer_c, loop), loop=loop)

# <codecell>

def client_side(loop, listen, connect, hostname, password, cafile, **kwarg):
    ssl_ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=cafile)
    return asyncio.start_server(partial(tcp2ssl, loop=loop, addr=connect,
                                        hostname=hostname, ssl=ssl_ctx,
                                        password=password),
                                *listen, loop=loop)

# <codecell>

def server_side(loop, listen, connect, password, certfile, **kwarg):
    ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_ctx.load_cert_chain(certfile)
    return asyncio.start_server(partial(ssl2tcp, loop=loop, addr=connect,
                                        password=password),
                                *listen, ssl=ssl_ctx, loop=loop)

# <codecell>

loop = asyncio.get_event_loop()

# <codecell>

if CLIENT['run']:
    asyncio.async(client_side(loop, **CLIENT), loop=loop)

# <codecell>

if SERVER['run']:
    asyncio.async(server_side(loop, **SERVER), loop=loop)

# <codecell>

loop.run_forever()
