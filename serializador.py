def send_object(conn, obj: object, addr=None):
    msg = repr(obj) + '\n'
    conn.sendall(msg.encode())

    if addr: print(f"client: {addr}, send: {msg}")

def recv_object(conn, buff: list, addr=None):
    if len(buff): response = buff.pop(0)
    else:
        msgs = conn.recv(1024).split(b'\n')
        response = msgs.pop(0)
        for msg in filter(bool, msgs):
            buff.append(msg)

    if addr: print(f"client: {addr}, recv: {response}")

    try:
        if response: return eval(response)
        else:        return None
    except SyntaxError: return None

