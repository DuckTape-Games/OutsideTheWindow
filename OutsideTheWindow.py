'''
"Outside The Window"
Concept - Window tries to escape you
Made for the Bad Ideas Game Jam
Theme - Outside the Box
Created By Chris Herriman Jr
'''



#############
### SETUP ###
#############

### Imports ###
import turtle as trtl #Used for gameplay mechanics
import tkinter as tk #Used for buttons
from pynput import mouse #Used to track mouse
from pygame import mixer #Used for sounds
import os, sys #Used for pyinstaller
import time #for delays
import random as rnd #Used for random movements and placements

### Makes onefile mode work in pyinstaller
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


### Game Base and Screen Setup ###
trtl.clearscreen() #removes the starting turtle as compared to clear()
screen = trtl.Screen()
trtl.title("Outside The Window")
screen_width = 900
screen_height = 700
screen.setup(screen_width,screen_height)
background_color = "#d0d0d0"
screen.bgcolor(background_color)
screen._root.resizable(False, False) #Sets the screen to not be resizable

### Sound Design ###
audio_on = True #Prevents againast any issues with audio drivers or missing audio files
try:
    mixer.init()
    #Sound effects
    error_sound = mixer.Sound(resource_path("Audio/errorSound.wav"))
    key_click_sequence = mixer.Sound(resource_path("Audio/keyClickSequence.wav"))
    key_click_sound = mixer.Sound(resource_path("Audio/keyClickSound.wav"))
except:
    audio_on = False
#Condenses all the if statements for audio play into one place
def play_audio(audio_file):
    if audio_on:
        audio_file.play()



#####################
### INTRO SEGMENT ###
#####################

### Setup Start Button ###
start_button = trtl.Turtle()
start_button.speed(0)
start_button.penup()
start_button.shape("square")
start_button.turtlesize(3)
start_button.color("blue")
start_button_radius = 37
start_button_coords = [[0,-300,200,0,300,250,0],[0,200,200,0,300,-300,0]]
start_button_movement_count = 0
start_button_click_count = 0
popup = 0

### Tracks the mouse on the screen ###
def motion_tracker(event):
    global start_button_movement_count,popup
    """Updates the label text with the current mouse position."""
    if start_button_movement_count < len(start_button_coords[0]):
        x, y = event.x, event.y
        if abs(((screen_width / 2) + start_button_coords[0][start_button_movement_count]) - x) <= start_button_radius + 1 and abs(((screen_height / 2) - start_button_coords[1][start_button_movement_count]) - y) <= start_button_radius + 1:
            if start_button_movement_count + 1 < len(start_button_coords[0]):
                start_button_movement_count += 1

            if start_button_movement_count == 1:
                trtl.title("Leave Me Alone")
            if start_button_movement_count == 3:
                trtl.title("Fine, you can click me")
            if start_button_movement_count == 4:
                trtl.title("SIKE!!!!")
            if start_button_movement_count == 5:
                screen._root.state('iconic') #Minimizes the screen
                #Creates a popup
                popup = tk.Toplevel(screen._root)
                popup.title("You should just leave...")
                popup_x = screen._root.winfo_x() + (screen._root.winfo_width() // 2) - 160
                popup_y = screen._root.winfo_y() + (screen._root.winfo_height() // 2) - 90
                popup.geometry(f"+{popup_x}+{popup_y}")
                popup.geometry("320x180")
                popup.resizable(False, False)
                popup_label = tk.Button(popup,text="Quit Game", command=lambda:popup.destroy())
                popup_label.pack(pady=10)
                trtl.title("Why are you back?")
            start_button.goto(start_button_coords[0][start_button_movement_count],start_button_coords[1][start_button_movement_count])
            if start_button_movement_count == 6:
                if popup.winfo_exists():
                    popup.destroy()
                trtl.title("Fine, you can click me (For real this time)")
                start_button_movement_count += 1

### Different phases of clicking the start button ###
def click_start_button(x,y): #x and y are required for turtle on click
    global start_button_click_count
    start_button_click_count += 1
    if start_button_click_count == 1:
        play_audio(error_sound)
        trtl.title("Why won't this work?")
    elif start_button_click_count == 2:
        play_audio(error_sound)
        trtl.title("Seriously... Why won't this work?")
    elif start_button_click_count == 3:
        play_audio(error_sound)
        trtl.title("WHY WON'T THIS WORK?????")
        screen.bgcolor("red")
        start_button.color("Black")
    elif start_button_click_count == 4:
        play_audio(error_sound)
        trtl.title("Nevermind, I figured It Out")
        screen.bgcolor("#d0d0d0")
        time.sleep(0.3)
        create_code_popup(list("start_button.onclick(start_game)"))
        screen._root.after(5000, lambda:trtl.title("Fixed. Now Try"))
        start_button.color("Blue")
    elif start_button_click_count == 5:
        start_phase_one()

### Screen Functionality ###
start_button.onclick(click_start_button) #Tracks if the start button is clicked
screen._root.bind("<Motion>", motion_tracker) #Tracks mouse

### Creates the short coding sequence ###
def create_code_popup(on_screen_text):
    code_popup = tk.Toplevel(screen._root)
    popup_x = screen._root.winfo_x() + (screen._root.winfo_width() // 2) - 160
    popup_y = screen._root.winfo_y() + (screen._root.winfo_height() // 2) - 90
    code_popup.geometry(f"+{popup_x}+{popup_y}")
    code_popup.geometry("400x400")
    code_popup.resizable(False, False)
    code_popup.configure(bg="#192a1a")
    code_popup.overrideredirect(True)
    code_label = tk.Label(code_popup,bg="#192a1a", fg="white")
    code_label.place(x=20,y=50)
    code_text = ""
    # Animate typing using Tkinter's scheduler (non-blocking)
    def type_next_char(i=0, current_text=""):
        if i >= len(on_screen_text):
            return  # done
        current_text += on_screen_text[i]
        code_label.config(text=current_text)
        code_popup.after(100, type_next_char, i + 1, current_text)
    for i in range(len(on_screen_text)):
        code_text += on_screen_text[i]
        code_label.config(text=code_text)
        play_audio(key_click_sequence)
        type_next_char()
    def remove_code_popup():
        code_popup.destroy()
        play_audio(key_click_sound)
    code_popup.after(4500, remove_code_popup )



###############
### PHASE 1 ###
###############

### Starts the first phase of the game ###
def start_phase_one():
    screen.clear()
    def found_it(event):
        trtl.title("You Found It!!")
    screen._root.bind('<FocusIn>', found_it)
    trtl.title("Click The Button")
    screen.bgcolor("#ffffff")
    popup_x = screen._root.winfo_x() + (screen._root.winfo_width()) - 885
    popup_y = screen._root.winfo_y() + (screen._root.winfo_height()) - 665
    newX = screen._root.winfo_x()
    newY = screen._root.winfo_y()
    screen._root.geometry(f"+{newX}+{newY}")
    second_screen = tk.Toplevel(screen._root)
    second_screen.geometry(f"+{popup_x}+{popup_y}")
    second_screen.geometry("887x695")
    second_screen.resizable(False, False)
    second_screen.configure(bg="#d0d0d0")
    second_screen.overrideredirect(True)
    fake_button_list = []
    for i in range(20):
        fake_button = tk.Button(second_screen, text="Click Me", command=lambda:trtl.title("Wrong Button"),width=10, height=3)
        fake_button.place(x=rnd.randint(50,850),y=rnd.randint(50,650))
        fake_button_list.append(fake_button)
    blue_square=trtl.Turtle()
    blue_square.speed(0)
    blue_square.penup()
    blue_square.turtlesize(1)
    blue_square.shape("square")
    blue_square.color("blue")
    size_count = 1
    def increase_square_size():
        nonlocal size_count
        if size_count < 10:
            if size_count == 1:
                trtl.title("Nice Job")
            if size_count == 5:
                trtl.title("You Found Me!!!")
            size_count += 1
        blue_square.turtlesize(size_count)
    real_button = tk.Button(screen._root, text="Click\nMe", command=increase_square_size,width=30, height=10)
    real_button.place(x=350,y=300)
    blue_square.onclick(start_phase_two)



###############
### PHASE 2 ###
###############

### Starts the second phase of the game ###
def start_phase_two(x,y): #x and y are required for trtl.onclick()
    screen.clear()


trtl.mainloop()
