
from uuid import uuid4
import socket
from datetime import datetime
from json import loads, dumps
from threading import Thread
from argparse import ArgumentParser

parser = ArgumentParser(description="参数说明(Parameter Description)")
parser.add_argument("--command", type=str, help="运行时启动的命令(Command launched at runtime)", default=None)
parser.add_argument("--name", type=str, help="运行时默认的名字(Default name at runtime)", default=None)
parser.add_argument("--language", type=str, help="运行时默认的语言(Default language at runtime)", default="zh-cn")
parser.add_argument("--host", type=str, help="运行时默认绑定的主机(The default bound host at runtime)", default="0.0.0.0")
parser.add_argument("--port", type=int, help="运行时默认绑定的端口(The default bound port at runtime)", default=5550)
parser.add_argument("--password", type=str, help="创建连接时的密码(Password when creating a connection)", default="")

args = parser.parse_args()
CueWord: str = ">>> "
GetNowTime: str = lambda: datetime.now().strftime("%H:%M:%S")
LanguageTable: dict[str:list[str]] = {
    "zh-cn": [
        "\"create\" 后面要加参数.",
        "使用 \"create\" 命令创建一个实例.",
        "使用 \"join\" 命令加入(连接)一个实例.",
        "已绑定地址 ",
        "地址 {} 已连接服务器.",
        "当前语言为 ",
        "已设置语言为 ",
        "语言已经是 ",
        "使用 \"language\" 或者 \"lang\" 命令查看/修改语言.",
        "已连接地址 ",
        "你还没取名字.",        # 10
        "有地址 {} 正在尝试连接.",
        "已连接地址: ",
        " 注册名称为: ",        # 13
        "已被踢出.",
        "你可能已经被踢出或者服务端已经关闭.",
        "按下回车退出.",
        "服务器已关闭.",
        "没有人被禁言.",
        "你已被禁言.",           # 19
        "后面参数无效.",
        "密码错误.",
        "密码为:",
        "密码正确.",
        "密码错误."
    ],
    "en-us": [
        "The parameter should be carried after \"create\".",
        "Create an instance using the \"create\" command.",
        "Join an instance by using the \"join\" command.",
        "Bind Address ",
        "Address {} connected to server.",
        "The current language is ",
        "Language has been set to ",
        "Language already is ",
        "Use the \"language\" or \"lang\" command to view/modify the language."
        "Connected to address ",
        "You haven't given a name yet.",
        "There is an address attempting to connect.",
        "Connected address:",
        " The registered name is:",
        "kicked out.",
        "You may have been kicked out or the server may have been shut down.",
        "Press Enter to exit.",
        "The server has been shut down.",
        "No one is banned from speaking.",
        "You have been banned from speaking.",
        "The following parameters are invalid.",
        "Password error.",
        "The password is",
        "Password is correct.",
        "Password error."
    ]
}
language: str = args.language
name = args.name

class Console():
    def __init__(self) -> None:
        "提供一些关于控制台的命令(Provide some commands about the console)"
    
    def LogMessage(self, message: dict[str: str], 
                   LogName: bool = True) -> None:
        "打印收到的消息, 格式为: [time] [消息]"
        print(f'[{message["time"] + (":" + message["sender"] if (LogName) else "")}] {message["message"]}')
    
    def LogEvent(self, *event: str, Id: int, joinChar: str = "", end: str = "\n") -> None:
        "打印发送的时间"
        # print(f'[{GetNowTime()}] {LanguageTable[language][Id][0] + joinChar.join(map(str, event)) + LanguageTable[language][Id][1]}')
        print(f"[{GetNowTime()}] {LanguageTable[language][Id].format(joinChar.join(map(str, event)))}", end=end)

console: Console = Console()

class Server:
    def __init__(self, host: str, port: int, password: str) -> None:
        self.host = host
        self.port = port
        self.Socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ClientSockets: dict = {}  # 存储连接的客户端
        self.ClientMessages: list = [] # 存储所有客户端发送的消息
        self.stop = False
        self.AllProhibition = False
        self.ProhibitionList = []
        self.Password = password
    
    def Start(self) -> None:
        self.Socket.bind((self.host, self.port))
        self.Socket.listen()
        print(LanguageTable[language][3] + f"{host}:{port}", LanguageTable[language][22], self.Password)
        Thread(target=self.InputCommand, args=()).start()
        while ...:
            try:
                self.ClientSocket, self.Addr = self.Socket.accept()
                console.LogEvent(*self.Addr, Id=11, joinChar=":")
                self.Connect()
            except:
                if (self.stop):
                    print(LanguageTable[language][17], end="")
                    break

    def Connect(self) -> None:
        try:
            date = loads(self.ClientSocket.recv(pow(2, 20)).decode("utf-8"))
            if (not date["password"] == self.Password):
                raise IndexError
            self.ClientSockets[date["name"]] = self.ClientSocket
            self.ClientSocket.send(b"200")
            self.ClientSocket.send(dumps({"message": self.ClientMessages}).encode("utf-8"))
            console.LogEvent(*self.Addr, Id=4, joinChar=":",
                              end=LanguageTable[language][13] + date["name"] + "\n") #13
            Thread(target=self.GetMessage, args=(self.ClientSocket, date["name"], )).start()
        except:
            self.ClientSocket.send(b"404")
            self.ClientSocket.close()
    
    def GetMessage(self, Socket: socket.socket, Name: str) -> None:
        try:
            while ...:
                date = Socket.recv(pow(2, 20))
                message: dict = loads(date.decode("utf-8"))
                if (not (("message" and "time" and "uuid" and "sender") in message)):
                    continue
                if (message["sender"] in self.ProhibitionList):
                    message = {
                        "message": LanguageTable[language][19],
                        "sender": "server",
                        "prohibition": 0
                    }
                    Socket.send(dumps(message).encode("utf-8"))
                elif (self.AllProhibition):
                    message = {
                        "message": LanguageTable[language][18],
                        "sender": "server",
                        "prohibition": 0
                    }
                    Socket.send(dumps(message).encode("utf-8"))
                else:
                    console.LogMessage(message)
                    for name, c in self.ClientSockets.items():
                        c.send(dumps({
                            "message": message["message"],
                            "time": GetNowTime(),
                            "uuid": str(uuid4()),
                            "sender": message["sender"]
                        }).encode("utf-8"))

                    self.ClientMessages.append(message)
        except Exception as e:
            print(e)
            Socket.close()
            if (Name in self.ClientSockets):
                del self.ClientSockets[Name]
    
    def InputCommand(self):
        while ...:
            self.UserInput = input("").split(" ")
            if (self.UserInput[0] == "kick"):
                if (len(self.UserInput) == 2 and self.UserInput[1] in self.ClientSockets):
                    self.ClientSockets[self.UserInput[1]].close()
                    del self.ClientSockets[self.UserInput[1]]
                    print(self.UserInput[1], LanguageTable[language][14])
            elif (self.UserInput[0] == "user"):
                if (len(self.UserInput) == 2 and self.UserInput[1] == "list"):
                    for name, _ in self.ClientSockets.items():
                        print(name, end=" ")
                    print()
                elif (len(self.UserInput) >= 2 and 
                      (self.UserInput[1] == "prohibition" or 
                       self.UserInput[1] == "pro")):
                    if (len(self.UserInput) >= 4):
                        if (self.UserInput[2] == "add"):
                            for name in self.UserInput[3:]:
                                if (name in self.ClientSockets):
                                    self.ProhibitionList.append(name)
                        elif (self.UserInput[2] == "remove" or 
                              self.UserInput[2] == "rm"):
                            for name in self.UserInput[3:]:
                                if (name in self.ProhibitionList):
                                    self.ProhibitionList.remove(name)
                        else:
                            print(self.UserInput[1], LanguageTable[language][20])
                    elif (len(self.UserInput) == 2):
                        print((LanguageTable[language][18]
                               if not len(self.ProhibitionList)
                               else " ".join(self.ProhibitionList)))
            elif (self.UserInput[0] == "stop"):
                self.stop = True
                self.Socket.close()

class Client:
    def __init__(self, host: str, port: int, name: str, password) -> None:
        self.host = host
        self.port = port
        self.Socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = name
        self.Password = password
    
    def Start(self):
        self.Socket.connect((self.host, self.port))
        print(LanguageTable[language][12] + f"{self.host}:{self.port}")
        self.Socket.send(dumps({"name": self.name, "password": self.Password}).encode("utf-8"))
        if (self.Socket.recv(1024) == b"404"):
            print(LanguageTable[language][24])
            return
        if (self.Password != ""):
            print(LanguageTable[language][23])
        self.HistoricalInfo: list = loads(self.Socket.recv(pow(2, 20)).decode("utf-8"))["message"]
        self.LogMessage()
        Thread(target=self.GetMessage, args=()).start()
        while ...:
            self.Input = input("")
            self.date = {
                "message": self.Input,
                "time": GetNowTime(),
                "uuid": str(uuid4()),
                "sender": self.name
            }
            if (self.Input.strip()):
                self.Socket.send(dumps(self.date).encode("utf-8"))

    def GetMessage(self):
        while ...:
            try:
                message = loads(self.Socket.recv(pow(2, 20)).decode("utf-8"))
                if (message["sender"] != self.name and not
                    "prohibition" in message):
                    print(f'{message["sender"]}: {message["message"]}')
                elif ("prohibition" in message):
                    print(LanguageTable[language][19])
            except:
                print(LanguageTable[language][15])
                input(LanguageTable[language][16])
                exit()

    def LogMessage(self):
        for i in self.HistoricalInfo:
            if (i["sender"] == self.name):
                print(i["message"])
            else:
                print(f"{i['sender']}: {i['message']}")


while ...:
    UserInput: list = (input(CueWord).split(' ')
                       if args.command is None
                       else args.command.split(" "))
    args.command = None
    # UserInput = ["create", "server"]
    if (UserInput[0] == "create"):
        if (len(UserInput) > 1 and UserInput[1] == "server"):
            name: str = ("administer" 
                         if name is None 
                         else name)
            host = (
                UserInput[UserInput.index("--host") + 1] 
                if ("--host" in UserInput and len(UserInput) > UserInput.index("--host") + 1) 
                else args.host
            )
            port = (
                int(UserInput[UserInput.index("--port") + 1])
                if ("--port" in UserInput and len(UserInput) > UserInput.index("--port") + 1) 
                else args.port
            )
            password = (
                int(UserInput[UserInput.index("--password") + 1])
                if ("--password" in UserInput and len(UserInput) > UserInput.index("--password") + 1) 
                else args.password
            )
            Server(host, port, password).Start()
        else:
            print(LanguageTable[language][0])
    elif (UserInput[0] == "join"):
        if (UserInput[1] == "server"):
            if (name is None):
                print(LanguageTable[language][10])
                continue
            host = (
                UserInput[UserInput.index("--host") + 1] 
                if ("--host" in UserInput and len(UserInput) > UserInput.index("--host") + 1) 
                else ("127.0.0.1"
                      if args.host == "0.0.0.0"
                      else args.host)
            )
            port = (
                int(UserInput[UserInput.index("--port") + 1])
                if ("--port" in UserInput and len(UserInput) > UserInput.index("--port") + 1) 
                else args.port
            )
            password = (
                int(UserInput[UserInput.index("--password") + 1])
                if ("--password" in UserInput and len(UserInput) > UserInput.index("--password") + 1) 
                else args.password
            )
            # Client(host, port, name)
            Client(host, port, name, password).Start()
    elif (UserInput[0] == "lang" or UserInput[0] == "language"):
        if (len(UserInput) == 2 and UserInput[1] in [i[0] for i in list(LanguageTable.items())]):
            if (language == UserInput[1]):
                print(LanguageTable[language][7] + f"\"{language}\".")
            else:
                language = UserInput[1]
                print(LanguageTable[language][6] + f"\"{language}\".")
        else:
            print(LanguageTable[language][5] + f"\"{language}\".")
    elif (UserInput[0] == "name"):
        if (len(UserInput) == 1):
            print((name
                   if not name is None
                   else "Null"))
        elif (len(UserInput) == 2):
            name = UserInput[1]
    elif (UserInput[0] == "help"):
        if (len(UserInput) > 1):
            pass
        else:
            print(LanguageTable[language][1])
            print(LanguageTable[language][2])
            print(LanguageTable[language][8])

