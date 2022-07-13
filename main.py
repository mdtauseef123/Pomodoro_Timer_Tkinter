from tkinter import *
import math

"""
The Pomodoro Technique:- 
25min Work
5min Break
25min Work
5min Break
25min Work
5min Break
25min Work
20min Break
"""
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 1
SHORT_BREAK_MIN = 1
LONG_BREAK_MIN = 20
reps = 0
#We have the set the timer variable global as we don't want to pass the variable of after() in after_cancel()
#Initially it is set to nothing i.e. None
timer = None
# ---------------------------- TIMER RESET ------------------------------- # 


def reset_timer():
    """
    Now we have to reset the timer so when we reset the timer firstly the timer should stop then the timer_text should
    appear as 00:00 and the label should change to 'Timer'.
    In order to stop the timer we should stop it using after_cancel() method by passing the variable which holds the
    timer after() method, in our case it is 'timer'.
    """
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    label.config(text="Timer")
    tick_label.config(text="")
    #We also have to make the reps to 0 as the value of reps is also increasing with the program
    global reps
    reps = 0
# ---------------------------- TIMER MECHANISM ------------------------------- # 


def start_timer():
    #Since we have set the mechanism for after() in seconds, so we can't directly pass minutes or hours instead we have
    #to pass the time in seconds after conversion, so if it is in minutes multiply by 60(1min=60s) or if it is in hours
    #then multiply by 3600(1hr = 3600s)
    global reps
    reps += 1
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps == 1 or reps == 3 or reps == 5 or reps == 7:
        label.config(text="Timer", fg=GREEN)
        count_down(work_sec)
    elif reps == 2 or reps == 4 or reps == 6:
        label.config(text="Break", fg=PINK)
        count_down(short_break_sec)
    elif reps == 8:
        label.config(text="Break", fg=RED)
        count_down(long_break_sec)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 


def count_down(count):
    """
    after() is a method that takes an amount of time(in millisecond(1s=1000ms)) it should wait and then after that
    amount of time it simply calls a particular function, and lastly we will pass arbitrary many positional arguments as
    we want.
    Now we want our timer to be displayed on the canvas text for that we have to hold a variable to the timer text and
    then change with the help of itemconfig() which is similar to config() function which we used in label,button,etc to
    change the attribute.
    Here, after() is behaving like a recursion as it is calling function in which it is placed.
    It is always associated with window variable.
    """
    #In order to display the time in mm:ss format we firstly find the minutes and second in every duration and then we
    #will configure into the timer.
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if len(str(count_min)) == 1:
        count_min = "0" + str(count_min)
    if len(str(count_sec)) == 1:
        count_sec = "0" + str(count_sec)
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count-1)
    else:
        #After each reps gets completed we will call our start_timer() again
        start_timer()
        #And also we will add one tick if we successfully completed one 25 minutes session
        marks = ""
        #Work session is calculated using floor(reps/2)
        work_sessions = math.floor(reps / 2)
        for _ in range(work_sessions):
            marks += "✔"
        tick_label.config(text=marks)

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Pomodoro Timer")
#bg attribute is used for changing background colour
window.config(padx=100, pady=50, bg=YELLOW)

#Creating Timer label
# fg(stands for foreground) attribute is used to change the colour of the text
label = Label(text="Timer", fg=GREEN, font=(FONT_NAME, 50, "normal"), pady=10, bg=YELLOW)
label.grid(row=0, column=1)
# Creating canvas for image.
# We are making our canvas size according to the size of our image.
# To get rid of the border colour use highlightthickness attribute
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
#Adding images to the canvas
tomato_img = PhotoImage(file="tomato.png")
"""
We have to give the position where we want our image to be set, so we want our image to be centred, so we give x=200/2
and y=224/2
Here the image attribute doesn't expect the direct image location instead it expects PhotoImage in which we pass the 
Location of the image
"""
canvas.create_image(100, 112, image=tomato_img)
#This create_text() will put the text on the image it also wants arguments like x and y position and the text it want
#to display here x=103 and y=130 as we also want it on the centre of the screen
#fill attribute is used for the colour of the text that is displayed on the image
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(row=1, column=1)

#Creating start and reset buttons
start_button = Button(text="Start", highlightthickness=0, command=start_timer)
start_button.grid(row=2, column=0)
reset_button = Button(text="Reset", highlightthickness=0, command=reset_timer)
reset_button.grid(row=2, column=2)

#Creating tick label
tick_label = Label(bg=YELLOW)
tick_label.grid(row=3, column=1)


window.mainloop()
