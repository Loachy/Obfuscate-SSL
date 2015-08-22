# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

SERVER = dict(
    run = False, # run server code or not
    listen = ('0.0.0.0', 443),
    connect = ('127.0.0.1', 22),
    password = b"I'm a happy little tcp forwarder",
    certfile = 'cert.pem'
    )

# <codecell>

CLIENT = dict(
    run = True, # run client code or not
    listen = ('127.0.0.1', 22),
    connect = ('1.2.3.4', 443), # substitute with your ip
    password = b"I'm a happy little tcp forwarder",
    hostname = 'server',
    cafile = 'ca.crt'
    )
