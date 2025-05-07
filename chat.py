import sys
import socket
import fileinput

packageNumber = 0

def createMessage(data):
    global packageNumber
    msgBeforeChecksum = f"{data}|AY{packageNumber}AZ"
    packageNumber += 1

    totCharValue = 0
    for c in msgBeforeChecksum:
        totCharValue += ord(c)
    checksum = hex(((totCharValue & 0xffff) ^ 0xffff) + 1).upper()[2:]
    msg = f"{msgBeforeChecksum}{checksum}\r"
    #print(f"DEBUG MSG: {msg}")
    return msg.encode("iso-8859-1")

if len(sys.argv) == 3:
    print("Configuring...")

    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        print(f"Connecting to {sys.argv[1]} {int(sys.argv[2])}...")
        tcp_socket.connect((sys.argv[1], int(sys.argv[2])))

        print("Chat with SIP2!")
        while True:
            text = input("> ")
            if text.lower() == "exit":
                break
            tcp_socket.sendall(createMessage(text))
            try:
                data = ""
                while not data.endswith("\r"):
                    chunk = tcp_socket.recv(1024).decode("iso-8859-1")
                    #print(f"DEBUG CHUNK: {chunk}")
                    if not chunk:
                        break
                    data += chunk
                print(data)
            except socket.timeout:
                print("No response received (timeout)")
            except Exception as e:
                print(f"Error reading response: {e}")
    finally:
        tcp_socket.close()
else:
    print("Wrong number of arguments.")