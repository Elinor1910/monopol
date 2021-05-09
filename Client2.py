#############################################################################
# Client - that connect to the multi-threading server
############################################################################
import socket
import threading
import tkinter as tk
import random
import time

openning = tk.Tk()
game_screen = tk.Tk()

class Client(object):
    def __init__(self, ip, port, color, name, password):
        self.ip = ip
        self.port = port
        self.money = 250
        self.place = []
        self.color = color
        self.password = password
        self.name = name
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.player_assets = []
        self.board = (
            "start ----->", "TLV", "question", "Azrieli Towers", "income taxes", "Port of Haifa", "Hamelichim city",
            "surprise", "SuperLand",
            "The Biblical Zoo", "Eletrical company", "The Bima", "jail", "Haifa", "Eilat", "surprise", "Ramat Gan",
            "Petah Tiqwa", "Tveria", "Jerusalem", "question", "Bethlehem")
        self.assets = {"TLV": 250, "Azrieli Towers": 300, "income taxes": 300,
                       "Port of Haifa": 150, "Hamelichim city": 200, "SuperLand": 250, "The Biblical Zoo": 200,
                       "Eletrical company": 400, "The Bima": 250, "Haifa": 200, "Eilat": 150, "Ramat Gan": 300,
                       "Petah Tiqwa": 100, "Tveria": 150, "Jerusalem": 300, "Bethlehem": 230}

    def start(self):
        try:
            print('connecting to ip %s port %s' % (ip, port))
            # Create a TCP/IP socket
            self.sock.connect((ip, port))
            print('connected to server')
            # send receive example
            self.sock.sendall('Hello this is client 1, send me a job'.encode())
            # implement here your main logic
            self.handleServer()
            self.opening_screen(False)

        except socket.error as e:
            print(e)

    def handleServer(self):
        client_handler = threading.Thread(target=self.handle_client, args=())
        # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
        client_handler.start()

    def handle_client(self):
        while True:
            msg = self.sock.recv(1024).decode()
            print(msg)
            if 'player count' in msg:
                if '1' in msg:
                    wait = tk.Label(openning, text='Waiting for more players to join....', bg='white')
                    wait.place(x=200, y=100)
                if '2' in msg:
                    register = "playerInfo: " + str(self.name) + " " + "0" + " " + str(self.color) + " "
                    self.sock.send(str(register).encode())
                    self.draw_board()
                    self.opening_screen(True)
        #    if "yourTurn" in msg:
        #        name, psum, color = self.decode_server_msg(msg)
        #        if name == self.name:
        #            self.draw_players(msg, True)
        #        else:
        #            self.draw_players(msg, False)
        #    if "no" in msg:
        #        self.draw_players(msg, False)
        #        self.sock.send("game started".encode())

    def quitwindow(self, event):
        self.sock.send("im leaving".encode())

    def opening_screen(self, destroy):
        if destroy:
            openning.destroy()
        else:
            open = openning
            open["background"] = "white"
            open.iconbitmap('monopolylogo.ico')
            open.title("Monopoly Cyber")
            open.geometry("500x500+30+30")
            fn = tk.Label(open, text="First Name", bg='black', fg='white')
            fn.place(x=0, y=30)
            ps = tk.Label(open, text="Password", bg='black', fg='white')
            ps.place(x=0, y=50)
            e1 = tk.Entry(open)
            e2 = tk.Entry(open)
            quit = tk.Button(open, text='Quit', command=exit)
            quit.bind("<Button-1>", self.quitwindow)
            quit.place(x=0, y=100)
            e1.place(x=80, y=30)
            e2.place(x=80, y=50)
            show = tk.Button(open, text='Submit', command=lambda: self.get_info(open, e1.get(), e2.get()))
            show.place(x=0, y=80)
        openning.mainloop()

    def get_info(self, open, name, password):
        self.name = name
        self.password = password
        msg = "name&password " + str(name) + " " + str(password)
        self.sock.send(str(msg).encode())
        if self.name != '' and self.password != '':
            lbl = tk.Label(open, text="Choose a color:")
            lbl.place(x=0, y=150)
            black = tk.Button(open, bg='black', fg='white', text="black", width=3, height=2,
                              command=lambda: self.change_color('black', open))
            black.place(x=10, y=200)
            brown = tk.Button(open, bg='brown', fg='white', text="brown", width=3, height=2,
                              command=lambda: self.change_color('brown', open))
            brown.place(x=50, y=200)
            pink = tk.Button(open, bg='pink', fg='white', text="pink", width=3, height=2,
                             command=lambda: self.change_color('pink', open))
            pink.place(x=90, y=200)
        else:
            lbl = tk.Label(open, text='Submit your name and password before you continue', bg='white')
            lbl.place(x=0, y=250)
            self.opening_screen(False)

    def change_color(self, color, open):
        self.color = color
        if self.color != 'red':
            start = tk.Button(open, bg='yellow', text="start", width=10, height=5,
                              command=lambda: self.starting_screen(open))
            start.place(x=200, y=0)

    def starting_screen(self, open):
        self.sock.send("start".encode())
        self.handleServer()
        # open.after(100, lambda: self.starting_screen(open, msg))

    def decode_server_msg(self, info):
        x = info.split()
        print(x)
        name = x[1]
        psum = x[2]
        color = x[3]
        print("name: " + name + " psum: " + str(psum) + " color: " + color)
        return name, psum, color

    def finding_player_place(self, sum):
        sum = int(sum)
        if sum == 0:
            x, y = 0, 0
            bp = self.board[sum]
            return x, y, bp
        boardplace = [0, 10, 20, 30, 40, 50, 60, 70, 80, 81, 82, 83, 73, 63, 53, 43, 33, 23, 13, 12, 11]
        # finding board place
        bp = self.board[sum]
        # finiding x and y
        playerp = boardplace[sum]
        x = (playerp / 10) * 146
        y = (playerp % 10) * 156
        if (playerp < 9):
            x = 0
            y = playerp
        return x, y, bp

    def finding_sum(self, length):
        sum = 0
        for i in range(length):
            sum += self.place[i]
            if sum >= 21:
                sum = sum % 10
        return sum

    def rand_number(self, window):
        rand = random.randrange(1, 7)
        cub = tk.Label(window, bg='black', text=rand, fg='white', width=2, height=2)
        cub.place(x=1030, y=375)
        self.place.append(rand)
        self.sock.send(str(self.finding_sum(len(self.place))).encode())

    def draw_player(self, window, psum):
        x, y = 0, 0
        player = tk.Label(window, text=self.name, bg=self.color, fg='white')
        player.place(x=0, y=0)
        if psum == 0:
            player = tk.Label(window, text=self.name, bg=self.color, fg='white')
            player.place(x=x, y=y)
        elif psum > 0:
            # finding the current position
            x, y, bp = self.finding_player_place(psum)
            player = tk.Label(window, text=self.name, bg=self.color, fg='white')
            player.place(x=int(x), y=int(y))

        print(x, y)

    def questions(self, window):
        question_list = ("What is the difference between list and tuples in Python?",
                         "What type of language is python? Programming or scripting?",
                         "What is namespace in Python?", "What are local variables and global variables in Python?")
        answers_list = (
        "Tuples are immutable", "Tuples are slower than list", "Tuples made with []", "All the answers are currect")
        newWindow = tk.Toplevel(window)
        newWindow["background"] = "white"
        newWindow.iconbitmap('monopolylogo.ico')
        newWindow.title("Monopoly Cyber")
        newWindow.geometry("300x150+30+30")
        tk.Label(newWindow, text=question_list[0]).grid(row=0, column=2)
        rightanswer = tk.Button(newWindow, text=answers_list[0])
        rightanswer.grid(row=1, column=0)
        rightanswer.bind("<Button-1>", lambda: self.congrats(window))
        wronganswer = tk.Button(newWindow, text=answers_list[1])
        wronganswer.grid(row=1, column=3)
        wronganswer.bind("<Button-1>", lambda: self.wrong(window))

        newWindow.mainloop()

    def congrats(self, event, window):
        self.gift_cards(window)
        answer = tk.Label(window, text="congrats! you are right!")
        answer.place(x=0, y=0)

    def wrong(self, event, window):
        answer = tk.Label(window, text="you are wrong, try next time")
        answer.place(x=0, y=0)

    def gift_cards(self, window):
        gift_lst = (500, 100, 50, 50, 100, 1000, 50, 1)
        ran = random.choice(gift_lst)
        self.money += int(ran)
        self.update_and_show_money(window)

    def update_and_show_money(self, window):
        msg = tk.Label(window, text="your current money value:", fg="black")
        msg.place(x=30, y=650)
        mny = tk.Label(window, text=self.money, fg="black")
        mny.place(x=180, y=650)

    def cube(self, window):
        cube = tk.Button(window, bg='black', width=10, height=5, command=lambda: self.rand_number(window))
        cube.place(x=1000, y=350)
        # cube.bind("<Button-1>", self.rand_number(window))

    def draw_board(self):
        window = game_screen
        window.attributes("-fullscreen", True)
        window["background"] = "white"
        window.iconbitmap('monopolylogo.ico')
        window.title("Monopoly Cyber")
        self.draw_board_squares(window)
        self.update_and_show_money(window)
        window.mainloop()

    def picture(self, window):
        img = tk.PhotoImage(file='monopolygif.gif')
        lbl = tk.Label(window, image=img)
        lbl.place(x=500, y=200)
        window.mainloop()

    def players_actions(self, msg, window):
        name, psum, color = self.decode_server_msg(msg)
        x, y, bp = self.finding_player_place(psum)
        if bp == "surprise":
            self.gift_cards(window)
        if bp == "question":
            self.questions(window)

    def draw_players(self, msg, turn):
        name, psum, color = self.decode_server_msg(msg)
        x, y, bp = self.finding_player_place(psum)
        if turn:
            player = tk.Label(game_screen, text=str(name), bg=color, fg='white')
            player.place(x=int(x), y=int(y))
            self.cube(game_screen)
        if not turn:
            player = tk.Label(game_screen, text=str(name), bg=color, fg='white')
            player.place(x=int(x + 40), y=int(y))
            cube = tk.Label(game_screen, bg='white', width=11, height=6)
            cube.place(x=1000, y=350)
        self.handleServer()


    def buy(self, window, x, y, asset):
        print(asset)
        price = self.assets[str(asset)]
        if self.money > price:
            self.player_assets.append(asset)
            self.money -= price
            self.update_and_show_money(window)
            purchase = tk.Label(window, text=self.name + "s'  property    ", bg='gray')
            purchase.place(x=x, y=y + 100)
        else:
            cant = tk.Label(window, text="You don't have enough money to buy this asset", bg='white')
            cant.place(x=450, y=650)

    def countdown(self, t):
        while t:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            print(timer, end="\r")
            time.sleep(1)
            t -= 1
        return 'done'

    def draw_board_squares(self, window):
        boardlen = len(self.board)
        third = int(boardlen / 3) + 2
        colors = ['red', 'blue', 'yellow', 'orange', 'green']
        pname = 0
        x, y, count = 0, 0, 0
        for path in range(third):
            if count > 4:
                count = 0
            asset = self.board[pname]
            square = tk.Label(window, width=20, height=10, bg=colors[count])
            square.place(x=x, y=y)
            name = tk.Label(window, text=asset, bg=colors[count])
            name.place(x=x + 40, y=y + 60)
            if 'start' not in self.board[pname] and "question" not in self.board[pname] and 'jail' not in self.board[
                pname] and 'surprise' not in self.board[pname]:
                price = self.assets[str(asset)]
                purchase = tk.Button(window, text='purchase: ' + str(price), bg='gray',
                                     command=lambda: self.buy(window, x, y, asset))
                purchase.place(x=x, y=y + 100)
            x += 146
            pname += 1
            count += 1

        x = 146
        y = 156
        for path in range(int(boardlen / 7)):
            if count > 4:
                count = 0
            square = tk.Label(window, width=20, height=10, bg=colors[count])
            square.place(x=x, y=y)
            name = tk.Label(window, text=self.board[pname], bg=colors[count])
            name.place(x=x + 40, y=y + 60)
            if 'start' not in self.board[pname] and "question" not in self.board[pname] and 'jail' not in self.board[
                pname] and 'surprise' not in self.board[pname]:
                asset = self.board[pname]
                price = self.assets[str(asset)]
                purchase = tk.Button(window, text='purchase: ' + str(price), bg='gray',
                                     command=lambda: self.buy(window, x, y, asset))
                purchase.place(x=x, y=y + 100)
            count += 1
            y += 156
            pname += 1

        y = y - 156
        x = 146
        for path in range(third - 2):
            if count > 4:
                count = 0
            square = tk.Label(window, width=20, height=10, bg=colors[count])
            square.place(x=x, y=y)
            name = tk.Label(window, text=self.board[pname], bg=colors[count])
            name.place(x=x + 40, y=y + 60)
            if 'start' not in self.board[pname] and "question" not in self.board[pname] and 'jail' not in self.board[
                pname] and 'surprise' not in self.board[pname]:
                asset = self.board[pname]
                price = self.assets[str(asset)]
                purchase = tk.Button(window, text='purchase: ' + str(price), bg='gray',
                                     command=lambda: self.buy(window, x, y, asset))
                purchase.place(x=x, y=y + 100)
            x += 146
            count += 1
            pname += 1

        for path in range(int(boardlen / 7)):
            if count > 4:
                count = 0
            square = tk.Label(window, width=20, height=10, bg=colors[count])
            square.place(x=x, y=y)
            name = tk.Label(window, text=self.board[pname], bg=colors[count])
            name.place(x=x + 40, y=y + 60)
            if 'start' not in self.board[pname] and "question" not in self.board[pname] and 'jail' not in self.board[
                pname] and 'surprise' not in self.board[pname]:
                asset = self.board[pname]
                price = self.assets[str(asset)]
                purchase = tk.Button(window, text='purchase: ' + str(price), bg='gray',
                                     command=lambda: self.buy(window, x, y, asset))
                purchase.place(x=x, y=y + 100)
            count += 1
            y -= 156
            pname += 1
        exitb = tk.Button(window, text='Exit', command=exit)
        exitb.place(x=0, y=300)
        # self.picture(window)


if __name__ == '__main__':
    ip = '127.0.0.1'
    port = 1730
    color = "red"
    name = "-"
    password = "-"
    c = Client(ip, port, color, name, password)
    c.start()
