#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 10:55:39 2019

@author: apurvi
"""

import speech_recognition as sr
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
import sys
from selenium.webdriver.support.ui import WebDriverWait
os.system("clear")

r=sr.Recognizer()
mic=sr.Microphone()
flag_stop=0
flag_autoplay=0 #0 means enabled
song_list=[]
playi_list=0
start_time=-1
i=0
current_song=""
def play_song(command):
    global current_song
    global start_time
    print('playing song')
    #time.sleep(1)
    song=""
    for i in range(1,len(command)):
        song+=command[i]+' '
            #print()
                #song+=command[i]
    print("song is",song)
    search_box=driver.find_element_by_name("search_query")
     
    search_box.click()
        #song='shape of you'
    search_box.clear()
    search_box.send_keys(song)
    search_box.submit()
    wait = WebDriverWait(driver, 3)
    visible = EC.visibility_of_element_located
    wait.until(visible((By.ID, "video-title")))
    

    song_link=driver.find_element_by_id("video-title")
    current_song=song_link.get_attribute('href')
    song_link.click()
    wait = WebDriverWait(driver, 10)
        
    visible1 = EC.visibility_of_element_located
    wait.until(visible1((By.CLASS_NAME,"ytp-time-duration")))
    
    
    start_time = driver.find_element_by_class_name("ytp-time-duration").text
       

def stop_song():
    print("inside pause")
    button=driver.find_element_by_class_name('ytp-play-button')
    global flag_stop
    if flag_stop==0 :
        flag_stop=1
        button.click()

def resume_song():
    button=driver.find_element_by_class_name('ytp-play-button')
    global flag_stop
    if flag_stop==1 :
        flag_stop=0
        button.click()

def replay_song():
    button=driver.find_element_by_class_name('ytp-play-button')
    check_end=button.get_attribute('title')
    check_end=check_end.lower()
    if(check_end=='replay'):
        button.click()
    

def autoplay():
    print("enter autoplay")
    wait = WebDriverWait(driver, 10)
    visible = EC.visibility_of_element_located
    wait.until(visible((By.ID, "toggle")))

    button=driver.find_element_by_id("toggle")
    print(button.get_attribute('aria-label'))
    global flag_autoplay
    if(flag_autoplay==0):
        flag_autoplay=1
        button.click()
        print('clicked')

def e_autoplay():
    print("enter autoplay")
    wait = WebDriverWait(driver, 10)
    
    visible = EC.visibility_of_element_located
    wait.until(visible((By.ID, "toggle")))

    button=driver.find_element_by_id("toggle")
    print(button.get_attribute('aria-label'))
    global flag_autoplay
    if(flag_autoplay==1):
        flag_autoplay=0
        button.click()
        print('clicked')
    
def play_list(i):
    global playi_list
    print("enter")
    #print(i)
    if(i==len(song_list)):
        playi_list=0
        return
        
    #print(song_list[i])
    send_song=song_list[i].split(' ')
    #Sprint(send_song)
    play_song(send_song)



def check_end():
    
    global start_time
    #time.sleep(5)
    print('entered')
    print(start_time)

    print("here")
    end_time=driver.find_element_by_class_name('ytp-time-current').text
    print(end_time)
    if(start_time==end_time):
            print("end")
            return False
    else:
            return True
        
       
def start_from(command):
    
    global current_song
    
    #song_modify=current_song
    if(command[1]=='again'):
        song_from=current_song+'&t=0'
        #stop_song()
        driver.get(song_from)
        return
    
    print(command[2])
    
    if(command[3]=='seconds'):
        song_from=current_song+'&t='+command[2]
        #print(current_song)
        #stop_song()
        driver.get(song_from)
        return
    
    if(command[3]=='minutes'):
        convert=int(command[2])*60
        song_from=current_song+'&t='+str(convert)
        #print(current_song)
        #stop_song()
        driver.get(song_from)
        return
    
    
    
       
def take_command():
    global song_list
    global playi_list
    global i
    
    with mic as source:
            
            if(playi_list==1):
        
                checking=check_end()
                if(checking==False):
                    #playi_list=1
                    i=i+1
                    play_list(i)
            print("WAITING FOR COMMAND....")
            
            r.adjust_for_ambient_noise(source)

            audio=r.listen(source)
            try:
                text=r.recognize_google(audio)
                text=text.lower()
                print('you said : {}'.format(text))
                command=text.split(' ')
                
                if(command[0]=='play' and command[1]=='from'):
                    start_from(command)
                elif(command[0]=='play' and playi_list==0) :
                    play_song(command)
                elif(command[0]=='pause'):
                    
                    stop_song()
                elif(command[0]=='resume'):
                    resume_song()
                elif(command[0]=="replay"):
                    replay_song()
                elif(text=="disable autoplay"):
                    autoplay()
                elif(text=="enable autoplay"):
                    e_autoplay()
                elif(text=="playlist"):
                    song_list=[]
                    return
                    #take_command()
                    
                elif(command[0]=='add'):
                    song_list.append(text)
                
                elif(command[0]=='play' and command[1]=='from'):
                    start_from(command)
                elif(command[0]=='start' and command[1]=='again'):
                    start_from(command)
                elif(text=='done'):
                    i=0
                    play_list(i)
                    time.sleep(1)
                    autoplay()
                    playi_list=1
                    
                elif(text=='bye'):
                    driver.close()
                    sys.exit()
                    #print(song_list[i])
                    
                   
                    
                    
                
                else:
                    print('wrong command')
               
                    
            except:
                pass
                
                
            


driver=webdriver.Chrome('/home/apurvi/Downloads/chromedriver_linux64/chromedriver')
driver.get('https://www.youtube.com/')
time.sleep(1)
print("-------COMMANDS-------\nplay song_name\ndisable autoplay\nenable autoplay\n\n--control playing song as-----\npause\nresume\nstart again\nplay from <time> in minutes or seconds\n")
print("to repeat song:REPLAY\n\n----Give playlist as------")
print("say\n 1.playlist\n2.add <song_name>\n3.done")
    
while 1: 
    take_command()
    