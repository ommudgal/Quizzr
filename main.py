# imorts
import mysql.connector
import customtkinter
from customtkinter import *
import tkinter
from mysql.connector import RefreshOption

# Setting the base deafult Appearance for the app
customtkinter.set_appearance_mode("blue")
customtkinter.set_default_color_theme("dark-blue")


# Setting Mysql Database and connector in a class, this will be called upon frequently in the app
class Mysql:
    mydb = mysql.connector.connect(host="localhost", user="root", passwd="password")
    cursorObject = mydb.cursor()


# Current Logged in user and Login status
class Current:
    logged_Inuser = ""
    login_Status = False


class App(customtkinter.CTk):
    WIDTH = 600
    HEIGHT = 480

    def __init__(self):
        super().__init__()
        self.state("zoomed")
        self.title("Quizzr")

        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # creating a function to deleate all the wigids placed on self
        def clear():
            # list of all wigids placed by grid methode
            list = self.grid_slaves()
            for l in list:
                l.destroy()
            # list of all wigids placed by place methode
            list = self.place_slaves()
            for l in list:
                l.destroy()
            # list of all wigids placed by pack methode
            list = self.pack_slaves()
            for l in list:
                l.destroy()

        # the register functon here we will take user details and check if they are already registered in the database.
        # and if they are not registered then add their data to the database
        def register():
            clear()

            Username_Entry = CTkEntry(
                master=self, placeholder_text="CREATE YOUR USERNAME", width=200
            )

            Email_Entry = CTkEntry(
                master=self, placeholder_text="ENTER YOUR EMAIL", width=200
            )

            Password_Entry = CTkEntry(
                master=self, placeholder_text="ENTER YOUR PASSWORD", width=200
            )
            Username_Entry.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)
            Email_Entry.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)
            Password_Entry.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

            def try_register():
                register_button.destroy()
                a = Username_Entry.get()
                b = Email_Entry.get()
                c = Password_Entry.get()
                syntax = f"INSERT INTO logdata VALUES('{a}','{b}','{c}');"
                try:
                    Mysql.cursorObject.execute("USE Quizzr")
                    Mysql.cursorObject.execute(syntax)
                except mysql.connector.Error:
                    registerfailed = CTkLabel(
                        self,
                        text="This Email id is already associated with an account try loggin in",
                    )
                    register_button.destroy()
                    registerfailed.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)
                    logtransfer = CTkButton(master=self, text="login", command=login)
                    logtransfer.place(relx=0.5, rely=0.79, anchor=tkinter.CENTER)

                else:
                    registeredsuccessfully = CTkLabel(
                        self, text="Registered Successfully"
                    )
                    registeredsuccessfully.place(
                        relx=0.5, rely=0.7, anchor=tkinter.CENTER
                    )
                    # button totransfer to the login screen

                    Mysql.mydb.commit()

                    logtransfer = CTkButton(master=self, text="login", command=login)
                    logtransfer.place(relx=0.5, rely=0.79, anchor=tkinter.CENTER)
                    register_button.destroy()

            register_button = CTkButton(
                master=self, text="Register", command=try_register
            )
            register_button.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)

        def login():
            clear()
            self.grid_columnconfigure(1, weight=1)
            self.grid_rowconfigure(0, weight=1)

            # defining a frame to the screen
            center_frame = CTkFrame(master=self)
            center_frame.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)

            # Creating the email and password entries and placing them on the screen
            email_entry = CTkEntry(
                master=center_frame,
                placeholder_text="Enter Your Email",
                width=200,
                height=32,
                fg_color="black",
            )
            email_entry.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

            password_entry = CTkEntry(
                master=center_frame,
                placeholder_text="Enter your password",
                width=200,
                height=32,
                fg_color="black",
            )
            password_entry.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

            def try_login():
                email = email_entry.get()
                password = (password_entry.get(),)

                syntax = f"SELECT password FROM logdata WHERE Email = '{email}'"
                Mysql.cursorObject.execute("USE Quizzr")
                Mysql.cursorObject.execute(syntax)
                password_in_db = Mysql.cursorObject.fetchone()
                if password == password_in_db:
                    Current.logged_Inuser = email
                    Current.login_Status = True
                    loggedinlabel = CTkLabel(self, text="Logged in")
                    loggedinlabel.place(relx=0.7, rely=0.7, anchor=tkinter.CENTER)
                    mainscreen()
                else:
                    invalidcrdentialslabel = CTkLabel(self, text="Invalid Credentials")
                    invalidcrdentialslabel.place(
                        relx=0.5, rely=0.7, anchor=tkinter.CENTER
                    )

            loginbutton = CTkButton(
                master=center_frame,
                width=120,
                height=32,
                border_width=2,
                text="login",
                hover=True,
                hover_color="purple",
                fg_color="black",
                command=try_login,
            )
            loginbutton.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)

        # Defining a function to change login status to false
        def logout():
            Current.logged_Inuser = ""
            Current.login_Status = "False"
            startscreen()

        # The mainscreen after logging in. this is where the user will create and play quizzes
        def mainscreen():
            clear()
            # dividing the screen into 3 frames
            self.grid_columnconfigure(1, weight=1)
            self.grid_rowconfigure(0, weight=1)
            left_frame = CTkFrame(master=self, width=200, corner_radius=0)
            left_frame.grid(row=0, column=0, sticky="nswe")

            center_frame = CTkFrame(master=self)
            center_frame.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

            right_frame = CTkFrame(master=self, width=200, corner_radius=0)
            right_frame.grid(row=0, column=999, sticky="nswe")
            # =========================LEFT FRAME==========================

            # reconfiguring the grid in the left frame
            left_frame.grid_rowconfigure(0, minsize=10)
            left_frame.grid_rowconfigure(5, weight=1)
            left_frame.grid_rowconfigure(8, minsize=20)
            left_frame.grid_rowconfigure(11, minsize=10)

            # creating the title label
            titlelabel = CTkLabel(
                master=left_frame,
                text="QUIZZR",
                font=("Avenir Next LT Pro", 35),
                text_color="white",
            )
            titlelabel.grid(row=2, column=0, pady=10, padx=10, sticky="w")

            # Theme selector drop down menu
            themeselector = CTkOptionMenu(
                master=left_frame,
                values=["Dark", "Light"],
                command=self.changetheme,
            )
            themeselector.grid(
                row=8,
                column=0,
                pady=10,
                padx=20,
                sticky="s",
            )
            # =======================RIGHT FRAME===============================

            # reconfiguring the grid of the frame on the right side
            right_frame.grid_rowconfigure(0, minsize=10)
            right_frame.grid_rowconfigure(5, weight=1)
            right_frame.grid_rowconfigure(8, minsize=20)
            right_frame.grid_rowconfigure(11, minsize=10)

            # the button which execute the logout function
            logoutbutton = CTkButton(master=right_frame, text="LOGOUT", command=logout)
            logoutbutton.grid(row=4, column=0, pady=10, padx=20, sticky="e")

            # the button that returns you to the main screen
            returnbutton = CTkButton(
                master=right_frame, text="RETURN TO MAIN MENU", command=mainscreen
            )
            returnbutton.grid(row=999, column=0, padx=5, pady=10, sticky="s")

            # =========================CENTER FRAME===========================

            # reconfiguring the grid for the frame in the center
            center_frame.grid_rowconfigure(0, minsize=10)
            center_frame.grid_rowconfigure(5, weight=1)
            center_frame.grid_rowconfigure(8, minsize=20)
            center_frame.grid_rowconfigure(11, minsize=10)

            # Creates a new quiz.
            def createquiz():
                # Destroy all center_frame slaves.
                def destroybutton():
                    list = center_frame.grid_slaves()
                    for l in list:
                        l.destroy()

                destroybutton()
                quiznameentry = CTkEntry(
                    master=center_frame,
                    placeholder_text="ENTER QUIZ NAME",
                    width=900,
                    height=64,
                )
                quiznameentry.grid(
                    row=0,
                    column=1,
                    padx=20,
                    pady=120,
                    columnspan=3,
                )

                # upon clicking the create quiz button this function will be called.
                # This function will register the quiz into the quizdata table,
                # and create a new table in the database quizzes where the questions and the answers will be stored
                def make_quiz_table():
                    global quizid
                    quizid = 0
                    tempquizname = quiznameentry.get()
                    # replace blank spaces for underscore
                    quizname = tempquizname.replace(" ", "_")
                    quizname.replace(" ", "_")

                    # registering quiz
                    Mysql.cursorObject.execute("Use Quizzr")
                    Mysql.cursorObject.execute("Select * from quizdata")
                    for row in Mysql.cursorObject:
                        quizid += 1
                    syntax = f"INSERT INTO quizdata VALUES('{str(quizid)}','{quizname}','{Current.logged_Inuser}')"
                    Mysql.cursorObject.execute(syntax)

                    # creating quiztable
                    Mysql.cursorObject.execute("Use quizzes")
                    syntax = f"CREATE TABLE z{str(quizid)}(Question VARCHAR(999) NOT NULL, Answer VARCHAR(999) NOT NULL)"
                    Mysql.cursorObject.execute(syntax)
                    Mysql.mydb.commit
                    question_entry()

                # This function creats the Question Entry screen
                def question_entry():
                    destroybutton()
                    questionentry = CTkEntry(
                        master=center_frame,
                        placeholder_text="Enter Your Question",
                        width=900,
                        height=64,
                    )
                    questionentry.grid(row=1, column=1, padx=20, pady=100, columnspan=3)

                    answerentry = CTkEntry(
                        master=center_frame,
                        placeholder_text="Enter Your Answer (In all small letters)",
                        width=720,
                        height=50,
                    )
                    answerentry.grid(row=3, column=1, padx=20, pady=20, columnspan=3)

                    # This function saves the current question and saves the quizdata to the database,
                    # and takes the use back to the main menu
                    def save_quiz():
                        syntax = f"INSERT INTO z{str(quizid)} VALUES('{questionentry.get()}','{answerentry.get()}')"
                        Mysql.cursorObject.execute(syntax)
                        Mysql.mydb.commit()
                        mainscreen()

                    # This function dos ethe same thins as the previous one but instead of returing to the main menu
                    # it send the user to a blank question creation screen
                    def next_question():
                        syntax = f"INSERT INTO z{str(quizid)} VALUES('{questionentry.get()}','{answerentry.get()}')"
                        Mysql.cursorObject.execute(syntax)
                        Mysql.mydb.commit()
                        question_entry()

                    submitbutton = CTkButton(
                        master=center_frame,
                        text="Next Question",
                        width=120,
                        height=64,
                        command=next_question,
                    )
                    submitbutton.grid(row=6, column=1, padx=10, pady=20)
                    savebutton = CTkButton(
                        master=center_frame,
                        text="Save Quiz",
                        width=120,
                        height=64,
                        command=save_quiz,
                    )
                    savebutton.grid(row=6, column=3, padx=10, pady=20)

                nextbutton = CTkButton(
                    master=center_frame, text="Next", command=make_quiz_table
                )
                nextbutton.grid(row=3, column=2, padx=20, pady=10)

            def playquiz():
                # Destroy all slaves.
                def destroybutton():
                    list = center_frame.grid_slaves()
                    for l in list:
                        l.destroy()

                destroybutton()
                # Configures the master and center of the mainframe.
                mainframe = CTkFrame(master=center_frame)
                mainframe.pack(fill=tkinter.BOTH, expand=1)

                mycanvas = CTkCanvas(mainframe)
                mycanvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
                mycanvas.configure(bg="#292929", highlightthickness=0)

                myscrollbar = CTkScrollbar(
                    mainframe, orientation=tkinter.VERTICAL, command=mycanvas.yview
                )
                myscrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
                mycanvas.configure(yscrollcommand=myscrollbar.set)

                secondframe = CTkFrame(mycanvas)
                mycanvas_object = mycanvas.create_window(
                    (0, 0), window=secondframe, anchor=tkinter.CENTER, tag="secondframe"
                )

                # defigning an event and binding it to the canvas
                def mainframe(event):
                    canvas_width = mycanvas.winfo_width()
                    canvas_height = mycanvas.winfo_height()
                    center_x = canvas_width / 2
                    center_y = canvas_height / 2
                    mycanvas.coords(mycanvas_object, center_x, center_y)

                mycanvas.bind("<Configure>", mainframe)

                def selectquiz():
                    refresh = RefreshOption.LOG | RefreshOption.THREADS
                    Mysql.mydb.cmd_refresh(refresh)

                    def destroy():
                        list = secondframe.grid_slaves()
                        for l in list:
                            l.destroy()
                        list = secondframe.place_slaves()
                        for l in list:
                            l.destroy()
                        list = secondframe.pack_slaves()
                        for l in list:
                            l.destroy()

                    destroy()
                    Mysql.cursorObject.execute("USE Quizzr")
                    Mysql.cursorObject.execute("Select * from quizdata")
                    a = []
                    for row in Mysql.cursorObject:
                        a += [row]
                    b = []

                    # Run a quiz.
                    def quiz(args):
                        print(args)
                        Mysql.cursorObject.execute("USE quizzes")
                        Mysql.cursorObject.execute(f"Select * from  z{str(args[0])}")
                        quizdata = []
                        for rows in Mysql.cursorObject:
                            quizdata += [rows]
                        quizstart(quizdata, 0)

                    # this loop creats a button for each quiz and packs them into the scrollable frame "second_frame"
                    for i in a:
                        Mysql.cursorObject.execute(
                            "SELECT Username from logdata where Email = '" + i[2] + "'"
                        )
                        j = Mysql.cursorObject.fetchone()
                        Creator = ""
                        for name in j:
                            b += [i[1] + " || Created by: " + str(name)]
                            Creator = str(name)

                        CTkButton(
                            master=secondframe,
                            text=i[1] + " || Created by: " + Creator,
                            command=lambda i=i: quiz(i),
                        ).pack(pady=5)

                    # this class keeps track of the score
                    class Score:
                        score = 0

                    # function to start the quiz
                    def quizstart(quizdata, currentquestion):
                        number_of_questions = len(quizdata)
                        destroy()

                        # Checks if the answer is correct in the quiz
                        def checkanswer():
                            f = currentquestion
                            a = answerentry.get()
                            if quizdata[currentquestion][1] == a:
                                print("correct answer")
                                f += 1
                                Score.score += 1
                                try:
                                    quizstart(quizdata, f)
                                except:
                                    IndexError
                                    destroy()
                                    quizcompletelabel = CTkLabel(
                                        master=secondframe, text="Quiz Complete!"
                                    ).pack(pady=5)
                                    answersummary = CTkLabel(
                                        master=secondframe,
                                        text="Currect answers = " + str(Score.score),
                                    ).pack(pady=5)
                                    returntoquizselect = CTkButton(
                                        master=secondframe,
                                        text="Return",
                                        command=selectquiz,
                                    ).pack(pady=5)
                            else:
                                print("incorrect answer")
                                f += 1
                                try:
                                    quizstart(quizdata, f)
                                except:
                                    IndexError
                                    destroy()
                                    quizcompletelabel = CTkLabel(
                                        master=secondframe, text="Quiz Complete!"
                                    ).pack(pady=5)
                                    totalquestions = CTkLabel(
                                        master=secondframe,
                                        text=f"Total questions = {str(len(quizdata))}",
                                    ).pack(pady=5)
                                    answersummary = CTkLabel(
                                        master=secondframe,
                                        text="Currect answers = " + str(Score.score),
                                    ).pack(pady=5)
                                    returntoquizselect = CTkButton(
                                        master=secondframe,
                                        text="Return",
                                        command=selectquiz,
                                    ).pack(pady=5)
                                    Score.score = 0

                        questionlabel = CTkLabel(
                            master=secondframe, text=quizdata[currentquestion][0]
                        )
                        questionlabel.pack(pady=5)
                        answerentry = CTkEntry(
                            master=secondframe, placeholder_text="Enter your answer"
                        )
                        answerentry.pack(pady=5)
                        submitbutton = CTkButton(
                            master=secondframe, text="Submit", command=checkanswer
                        )
                        submitbutton.pack(pady=5)

                selectquiz()

            createquizbutton = CTkButton(
                master=center_frame,
                text="Create Quiz",
                height=64,
                width=240,
                command=createquiz,
            )
            createquizbutton.grid(row=2, column=0, padx=120, pady=120, sticky="n")

            playquizbutton = CTkButton(
                master=center_frame,
                text="Play a quiz",
                height=64,
                width=240,
                command=playquiz,
            )
            playquizbutton.grid(row=2, column=1, padx=120, pady=120, sticky="n")

        def startscreen():
            clear()
            # TITLE LABEL
            titlelabel = CTkLabel(self, text="QUIZZR", font=("Avenir Next LT Pro", 76))
            titlelabel.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)
            # REGISTER BUTTON
            regbutton = CTkButton(
                master=self,
                width=120,
                height=32,
                border_width=2,
                # corner_radius=10,
                text="Register",
                command=register,
                hover=True,
                hover_color="purple",
                # bg_color="black",
                fg_color="black",
            )
            regbutton.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)
            # LOGIN BUTTON
            logbutton = CTkButton(
                master=self,
                width=120,
                height=32,
                border_width=2,
                # corner_radius=10,
                text="Login",
                command=login,
                hover=True,
                hover_color="purple",
                # bg_color="black",
                fg_color="black",
            )
            logbutton.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)

        startscreen()
        self.mainloop()

    def on_closing(self, event=0):
        self.destroy()

    # Change the theme mode.
    def changetheme(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)
        print(self.appearance_mode)


app = App()
app.mainloop()
