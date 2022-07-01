import requests
import sched
import time
import pyautogui

#Combo Funcs
def emote_block():
    #Play and pause music
    pyautogui.press("playpause")

def emote_right_shoulder():
    #Skip a song
    pyautogui.press("nexttrack")

def emote_left_shoulder():
    #Skip a song
    pyautogui.press("prevtrack")

def emote_right_shoulder2():
    #Skip a song
    pyautogui.press("volumeup")

def emote_left_shoulder2():
    #Skip a song
    pyautogui.press("volumedown")

#GLOBALS
global complete
complete = False
global pname
pname = "Liamm-"

s = sched.scheduler(time.time, time.sleep)
def check_emote_state(sc): 
    global complete
    #Get API
    response = requests.get("http://127.0.0.1:6721/session")
    if(response):
        #Is the emote active?
        for player in response.json()["teams"][1]["players"]:
            if(player["name"] == pname):
                if(player["is_emote_playing"] == True):
                    ##############
                    #Combo Checks#
                    ##############

                    #Block - Play/Pause
                    if((player["blocking"] == True) and (complete == False)):
                        emote_block()
                        complete = True
                    elif((player["blocking"] == False) and (complete == True)):
                        complete = False

                    #Right Shoulder - Skip Song
                    if((response.json()["right_shoulder_pressed"] == True) and (complete == False)):
                        emote_right_shoulder()
                        complete = True
                    elif((response.json()["right_shoulder_pressed"] == False) and (complete == True)):
                        complete = False

                    #Left Shoulder - Rewind Song
                    if((response.json()["left_shoulder_pressed"] == True) and (complete == False)):
                        emote_left_shoulder()
                        complete = True
                    elif((response.json()["left_shoulder_pressed"] == False) and (complete == True)):
                        complete = False
                    
                    #Right Shoulder2 - Vol Up
                    if((response.json()["right_shoulder_pressed2"] == True) and (complete == False)):
                        emote_right_shoulder2()
                        complete = True
                    elif((response.json()["right_shoulder_pressed2"] == False) and (complete == True)):
                        complete = False

                    #Left Shoulder2 - Vol Down
                    if((response.json()["left_shoulder_pressed2"] == True) and (complete == False)):
                        emote_left_shoulder2()
                        complete = True
                    elif((response.json()["left_shoulder_pressed2"] == False) and (complete == True)):
                        complete = False
        
    #Loop again
    sc.enter(.001, 1, check_emote_state, (sc,))

s.enter(.001, 1, check_emote_state, (s,))

s.run()


# Nice work
# I'm wanting to know if the player is making a fist, pointing a finger, thumbs up etc.
# Your best bet is using the left_shoulder_pressed (grip) and left_shoulder_pressed2 (trigger) fields in the /session response. That will give you an additional 2 bits (4 states) for each hand while in midair. I don't believe the bone response actually has individual finger bones.
# You can also use the holding_left field in the player object (next to is_emote_playing) to see if they are grabbing an object or not. Combining the holding object with hand position is what @iblowatsports used for his music player control in the Echo Speaker System.