##DEVELOPED BY Liamm-##


import requests
import sched
import time
import pyautogui

#Combo Funcs
#Change these around as you desire :)
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
global response
complete = False




s = sched.scheduler(time.time, time.sleep)
def check_emote_state(sc): 
    global complete
    #Get API (Try loop again if it can't connect but in 5 second intervals instead)
    try:
        response = requests.get("http://127.0.0.1:6721/session")  
        #Did we get a response?   
        if(response.status_code == 200):
            #Is the emote active?
            for player in response.json()["teams"][1]["players"]:
                if(player["name"] == response.json()["client_name"]):
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
                        if((response.json()["left_shoulder_pressed"] == True) and (complete == False) and (player["blocking"] == False)):
                            emote_left_shoulder()
                            complete = True
                        elif((response.json()["left_shoulder_pressed"] == False) and (complete == True) and (player["blocking"] == True)):
                            complete = False
                        
                        #Right Shoulder2 - Vol Up
                        if((response.json()["right_shoulder_pressed2"] == True) and (complete == False) and (player["blocking"] == False)):
                            emote_right_shoulder2()
                            complete = True
                        elif((response.json()["right_shoulder_pressed2"] == False) and (complete == True) and (player["blocking"] == True)):
                            complete = False

                        #Left Shoulder2 - Vol Down
                        if((response.json()["left_shoulder_pressed2"] == True) and (complete == False)):
                            emote_left_shoulder2()
                            complete = True
                        elif((response.json()["left_shoulder_pressed2"] == False) and (complete == True)):
                            complete = False
            
        #Loop again
        sc.enter(.001, 1, check_emote_state, (sc,))   
    except requests.exceptions.RequestException as e:
        #Loop again, no game found
        sc.enter(5, 1, check_emote_state, (sc,))  
        print("waiting for game..")

    

s.enter(.001, 1, check_emote_state, (s,))

s.run()
