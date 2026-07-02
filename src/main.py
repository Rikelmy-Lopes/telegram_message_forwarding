from monitor import client

with client:
    client.run_until_disconnected()