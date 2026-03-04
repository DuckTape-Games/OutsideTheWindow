'''
"Outside The Window"
Concept - Window tries to escape you
Made for the Bad Ideas Game Jam
Theme - Outside the Box
Created By Chris Herriman Jr
'''


#############
### Setup ###
#############

#Imports
import turtle as trtl #Used for gameplay mechanics
import tkinter as tk #Used for buttons
from pynput import mouse #Used to track mouse
from pygame import mixer #Used for sounds
import os, sys #Used for pyinstaller
import time #for delays

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



#Setup Start Button
start_button = trtl.Turtle()
start_button.speed(0)
start_button.penup()
start_button.shape("square")
start_button.turtlesize(3)
start_button.color("blue")
start_button_radius = 37
start_button_coords = [[0,-300,0,200,300,250,0],[0,200,200,0,300,-300,0]]
start_button_movement_count = 0
start_button_click_count = 0

# #Tracks the mouse on the screen
def motion_tracker(event):
    global start_button_movement_count
    """Updates the label text with the current mouse position."""
    x, y = event.x, event.y
    if start_button_movement_count < len(start_button_coords[0]):
        if abs(((screen_width / 2) + start_button_coords[0][start_button_movement_count]) - x) <= start_button_radius + 1 and abs(((screen_height / 2) - start_button_coords[1][start_button_movement_count]) - y) <= start_button_radius + 1:
            if start_button_movement_count + 1 < len(start_button_coords[0]):
                start_button_movement_count += 1
            if start_button_movement_count == 3:
                trtl.title("Leave Me Alone")
            if start_button_movement_count == 5:
                screen._root.state('iconic') #Minimizes the screen
                #Creates a popup
                popup = tk.Toplevel(screen._root)
                popup.title("I SAID LEAVE ME ALONE!!!")
                popup_x = screen._root.winfo_x() + (screen._root.winfo_width() // 2) - 160
                popup_y = screen._root.winfo_y() + (screen._root.winfo_height() // 2) - 90
                popup.geometry(f"+{popup_x}+{popup_y}")
                popup.geometry("320x180")
                popup.resizable(False, False)
                popup_label = tk.Label(popup,text="I SAID LEAVE ME ALONE!!!")
                popup_label.pack(pady=10)
                trtl.title("Why are you back?")
            start_button.goto(start_button_coords[0][start_button_movement_count],start_button_coords[1][start_button_movement_count])
            if start_button_movement_count == 6:
                trtl.title("Fine, you can click me")
                start_button_movement_count += 1

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
        start_game()

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
        play_audio(key_click_sequence)
        if i >= len(on_screen_text):
            return  # done
        current_text += on_screen_text[i]
        code_label.config(text=current_text)
        code_popup.after(100, type_next_char, i + 1, current_text)
    for i in range(len(on_screen_text)):
        code_text += on_screen_text[i]
        code_label.config(text=code_text)
        type_next_char()
    def remove_code_popup():
        code_popup.destroy()
        play_audio(key_click_sound)
    code_popup.after(4500, remove_code_popup )

def start_game():
    screen.clear()
    trtl.title("Outside The Window")








        



start_button.onclick(click_start_button)



screen._root.bind("<Motion>", motion_tracker)

trtl.mainloop()