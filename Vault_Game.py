import sys
sys.path.append("/home/strimble/TheVaultBTYSE/AD4115_SPI_Comms")
import AD4115_SPI_Driver as adc_spi
from AD4115_SPI_Driver import register_map
from time import sleep
import time
import matplotlib.pyplot as plt
import numpy as np
import spidev

import RPi.GPIO as GPIO
import time
import datetime


from pydub import AudioSegment
from pydub.playback import play, _play_with_simpleaudio
import simpleaudio

from scoreClient import ScoreClient
import pygame
import pygame_textinput
import adafruit_led_animation.color as color

from itertools import cycle
import threading
import alsaaudio

import random

RED = (255, 0, 0)

STANDBY = 0
GET_INPUT = 1
IN_GAME = 2
RESULTS = 3

display_time = "00.00"
receiver_connected = []
door_status = "Open"
game_status = STANDBY

def draw_glowing_line(surface, color, start, end, width):
    pygame.draw.line(surface, color, start, end, width)

def gameplay_gui():
    """
    This function creates all of the elements of the Vault GUI
    It runs in a Thead and stays in sync with the main game code using the games
    game_status 
    """
    global game_status
    global timer
    global display_time
    global laser_break
    global receiver_connected
    global door_status
    global screen_height
    global screen_width
    global lines
    ONLINE_MODE = True
    pygame.init()
    width = 1920
    height = 1080
    screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
    screen_height = screen.get_height()
    screen_width = screen.get_width()
    dialogue_font = pygame.font.Font('assets/research_remix.ttf', 70)
    game_text_font = pygame.font.Font('assets/research_remix.ttf', 70)
    game_score_font = pygame.font.Font('assets/research_remix.ttf', 150)
    small_font = pygame.font.Font('assets/research_remix.ttf', 20)
    score_font = pygame.font.Font('assets/research_remix.ttf',50)
    adi_logo = pygame.image.load('assets/ADI_logo.png').convert()
    adi_logo = pygame.transform.scale(adi_logo, (240,136))
    adi_logo_rect = adi_logo.get_rect(topleft=(25,25))
    pygame.display.set_caption('Vault')
    pygame.event.set_allowed([pygame.QUIT, pygame.K_RETURN])
    running = True
    color_pool = cycle(color.RAINBOW)
    try:
        while running:
            
            while game_status == STANDBY:
                print("GUI in standby")
                try:
                    if ONLINE_MODE is True:
                        print("Attempting to get top 10")
                        leaderboard_list = score_client.get_top_10()
                        if leaderboard_list is not None:
                    
                            print(str(leaderboard_list))
                            clock = pygame.time.Clock()
                            
                            leaderboard_title = dialogue_font.render('Leaderboard', True, color.WHITE)
                            leaderboard_title_rect = leaderboard_title.get_rect(center=(int(width/2), 120))
                            game_start_prompt = dialogue_font.render("Ready to play Vault!", True, color.WHITE)
                            game_start_prompt_rect = game_start_prompt.get_rect(center=(int(width/2), 980))
                            off_text_surface = pygame.Surface(game_start_prompt_rect.size)
                            off_text_surface.fill((0,0,0,0))
                            blink_surfaces = cycle([game_start_prompt, off_text_surface])
                            blink_surface = next(blink_surfaces)
                            pygame.time.set_timer(BLINK_EVENT, 1000)
                            header_name_list = ['Name', 'School', 'Score']
                            header_blit_list = []
                            item_width = width/5
                            for item in header_name_list:
                                leaderboard_header = dialogue_font.render(item, True, color.WHITE)
                                leaderboard_header_rect = leaderboard_header.get_rect(center=(int(item_width), int(height/4)))
                                header_blit_list.append((leaderboard_header, leaderboard_header_rect))
                                item_width += width/4 + 50
                            score_name_list = ['@EntryName', '@SchoolName', '@Score']
                            score_blit_list = []
                            
                            item_height = height/4 + 75
                            
                            for score in leaderboard_list:
                                if score is not None:
                                    item_width = width/5
                                    entry_color = next(color_pool)
                                
                                    for item in score_name_list:
                                        score_element = score_font.render(score.get(item), True, entry_color)
                                        score_element_rect = score_element.get_rect(center=(int(item_width), int(item_height)) )
                                        score_blit_list.append((score_element, score_element_rect))
                                        item_width += width/4 + 50
                                    item_height += 50
                            screen.fill(color.BLACK)
                            screen.blit(leaderboard_title, leaderboard_title_rect)
                            # screen.blit(game_start_prompt, game_start_prompt_rect)
                            
                            screen.blit(adi_logo, adi_logo_rect)
                            screen.blits(header_blit_list)
                            screen.blits(score_blit_list)

                            connected_laser_txt = small_font.render('Lasers Connected = '+str(receiver_connected.count(1)), True, color.WHITE)
                            connected_laser_txt_rect = connected_laser_txt.get_rect(center=(int(width)-300, int(height)-20))
                            screen.blit(connected_laser_txt, connected_laser_txt_rect)
                            
                            door_status_txt = small_font.render('Lasers Connected = '+str(receiver_connected.count(1)), True, color.WHITE)
                            door_status_txt_rect = connected_laser_txt.get_rect(center=(int(width)-600, int(height)-20))
                            screen.blit(door_status_txt, door_status_txt_rect)
                            pygame.display.update()
                            while game_status == STANDBY:
                                # Can only close window from Standby
                                screen.fill(color.BLACK)
                                screen.blit(leaderboard_title, leaderboard_title_rect)
                                # screen.blit(game_start_prompt, game_start_prompt_rect)
                                
                                screen.blit(adi_logo, adi_logo_rect)
                                screen.blits(header_blit_list)
                                screen.blits(score_blit_list)
                                
                                connected_laser_val = small_font.render('Lasers Connected = '+str(receiver_connected.count(1)), True, color.WHITE)
                                screen.blit(connected_laser_val, connected_laser_txt_rect)
                                door_closed_val = small_font.render("Exit Door " + door_status, True, color.WHITE)
                                screen.blit(door_closed_val, door_status_txt_rect)
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        pygame.display.quit()
                                        pygame.quit()
                                        print("Got quit")
                                    elif event.type == BLINK_EVENT:
                                        blink_surface = next(blink_surfaces)
                                        clock.tick(60)
                                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_f: 
                                        print("Toggle Fullscreen")
                                        pygame.display.toggle_fullscreen()
                                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                                        print("Entering game with keyboard input")
                                        game_status = IN_GAME
                                screen.blit(blink_surface, game_start_prompt_rect)
                                pygame.display.update()
                                #clock.tick(60)
                                sleep(0.2)
                                
                    else:
                        raise ConnectionError("Run Offline mode")
                except ConnectionError:
                    # ONLINE_MODE = False
                    print("Cannot connect to database - continuing with simple mode")
                    leaderboard_title = dialogue_font.render('Ready to Play Vault!', True, color.WHITE)
                    leaderboard_title_rect = leaderboard_title.get_rect(center=(int(width/2), int(height/2)))
                    screen.fill(color.BLACK)
                    
                    connected_laser_txt = small_font.render('Lasers Connected = '+str(receiver_connected.count(1)), True, color.WHITE)
                    connected_laser_txt_rect = connected_laser_txt.get_rect(center=(int(width)-300, int(height)-20))
                    screen.blit(connected_laser_txt, connected_laser_txt_rect)
                    
                    door_status_txt = small_font.render("Exit Door " + door_status, True, color.WHITE)
                    door_status_txt_rect = connected_laser_txt.get_rect(center=(int(width)-600, int(height)-20))
                    screen.blit(door_status_txt, door_status_txt_rect)
                    
                    screen.blit(leaderboard_title, leaderboard_title_rect)
                    pygame.display.update()
                    while game_status == STANDBY:
                        # Can only close window from Standby
                        screen.fill(color.BLACK)
                        screen.blit(leaderboard_title, leaderboard_title_rect)
                        connected_laser_val = small_font.render('Lasers Connected = '+str(receiver_connected.count(1)), True, color.WHITE)
                        screen.blit(connected_laser_val, connected_laser_txt_rect)
                        door_closed_val = small_font.render("Exit Door " + door_status, True, color.WHITE)
                        screen.blit(door_closed_val, door_status_txt_rect)
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.display.quit()
                                pygame.quit()
                                print("Got quit")
                            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f: 
                                print("Toggle Fullscreen")
                                pygame.display.toggle_fullscreen()
                            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                                print("Entering game with keyboard input")
                                game_status = IN_GAME
                        pygame.display.update()
                        sleep(0.2)
                    
            while game_status == IN_GAME:
                
                timer_txt = game_text_font.render('Time', True, color.WHITE)
                laser_break_txt = game_text_font.render('Lasers Tripped', True, color.WHITE)
                timer_score = game_score_font.render(str(display_time), True, color.WHITE)
                laser_break_score = game_score_font.render(str(int(laser_break)), True, color.WHITE)
                
                timer_txt_rect = timer_txt.get_rect(center=(int(width/2), int(height/4)))
                laser_break_txt_rect = laser_break_txt.get_rect(center=(int(width/2), int((height/4)*2.5)))
                timer_score_rect = timer_score.get_rect(center=(int(width/2), int(height/4) + 130))
                laser_break_rect = laser_break_score.get_rect(center=(int(width/2), int(height/4)*2.5 +130))
                screen.fill(color.BLACK)
                screen.blit( adi_logo, adi_logo_rect)
                screen.blit(timer_txt, timer_txt_rect)
                screen.blit(laser_break_txt, laser_break_txt_rect)
                

                pygame.display.update()
                while game_status == IN_GAME:
                    screen.fill(color.BLACK)
                    #print(timer)
                    timer_score = game_score_font.render(str(display_time), True, color.WHITE)
                    laser_break_score = game_score_font.render(str(int(laser_break)), True, color.WHITE)
                    
                    screen.fill(color.BLACK)
                    for line in lines:
                        draw_glowing_line(screen, RED, line[:2], line[2:],5)
                    screen.blit( adi_logo, adi_logo_rect)
                    screen.blit(timer_txt, timer_txt_rect)
                    screen.blit(laser_break_txt, laser_break_txt_rect)
                    timer_screen = screen.blit(timer_score, timer_score_rect)
                    laser_break_screen = screen.blit(laser_break_score, laser_break_rect)
                    screen.blit(timer_score, timer_score_rect)
                    pygame.display.update()
                    time.sleep(0.2)
                    
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                            game_status = STANDBY
                    
            while game_status == RESULTS:
                print("Showing Results GUI")
                results_color = next(color_pool)
                results_title = dialogue_font.render('Results', True, results_color)
                results_title_rect = results_title.get_rect(center=(int(width/2), 120))
                results_color = next(color_pool)
                score_txt = dialogue_font.render("Score", True, results_color)
                score_txt_rect = score_txt.get_rect(center=(int((width)/2), int(height/4)))
                    
                score_value = game_score_font.render(display_time, True, results_color)
                score_value_rect = score_value.get_rect(center=(int((width)/2), int(height/4)+130))
                results_blits = [(results_title, results_title_rect), (score_txt, score_txt_rect), (score_value, score_value_rect) ]
                
                name_color = next(color_pool)
                school_color = next(color_pool)
                while game_status == RESULTS:
                    # Get info from user
                    input_entry_name = pygame_textinput.TextInputVisualizer(font_color=name_color, font_object=dialogue_font, cursor_color=color.WHITE)
                    input_entry_name.value = 'Entry'
                    input_entry_school = pygame_textinput.TextInputVisualizer(font_color=school_color, font_object=dialogue_font, cursor_color=color.WHITE)
                    input_entry_school.value = 'School'
                    name_rect = input_entry_name.surface.get_rect(center = (int(width/2), int(height/2)))
                    school_rect = input_entry_school.surface.get_rect(center = (int(width/2), int(height/2)+100))
                    
                    screen.fill(color.BLACK)
                    
                    screen.blits(results_blits)
                    screen.blit(adi_logo, adi_logo_rect)
                    
                    # screen.blit(input_entry_school.surface, school_rect)
                    pygame.display.update()
                    if 1:# if ONLINE_MODE is True:
                        get_entry = 1
                        while get_entry == 1:
                            screen.fill(color.BLACK)
                            screen.blit(input_entry_name.surface, name_rect)
                            screen.blits(results_blits)
                            screen.blit(adi_logo, adi_logo_rect)
                            events = pygame.event.get()
                            input_entry_name.update(events)
                            pygame.display.update()
                            for event in events:
                                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                                    print("GOT Entry name: ", input_entry_name.value)
                                    get_entry = 2
                        
                        while get_entry == 2:
                            screen.fill(color.BLACK)
                            screen.blit(input_entry_name.surface, name_rect)
                            screen.blit(input_entry_school.surface, school_rect)
                            screen.blits(results_blits)
                            screen.blit(adi_logo, adi_logo_rect)
                            events = pygame.event.get()
                            input_entry_school.update(events)
                            pygame.display.update()
                            for event in events:                 
                                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                                    print("GOT School name: ", input_entry_school.value)
                                    get_entry = 3
                                    try:
                                        new_score = score_client.submit_score(entry_name=input_entry_name.value, school_name=input_entry_school.value, score=float(display_time))
                                        time.sleep(0.5)
                                    except ConnectionError:
                                        print("Failed to submit score - continuing")
                                    game_status = STANDBY
                    else:
                        while game_status == RESULTS:
                            events = pygame.event.get()
                            # Don't print socre entry if in offline mode - press enter to start new game
                            for event in events:                 
                                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                                    game_status = STANDBY
                                                
                    
    # Clean up GUI displays     
    finally:
        pygame.display.quit()
        pygame.quit()



BLINK_EVENT = pygame.USEREVENT + 0

timer = 0
laser_break = 0

score_client = ScoreClient(game_name="Vault", client_ip="169.254.75.231", host_ip="169.254.211.56")

gui_thread = threading.Thread(target=gameplay_gui)

    # Start GUI thread outsde loop. Can only be started once



#-----------------------------------------------------------------------
# GPIO and Sound Setup

#start = AudioSegment.from_wav("/home/vault/Documents/GIT/TheVaultBTYSE/Audio/3-2-1_GO.wav")
print("Loading Audio....")
mission_impossible = AudioSegment.from_mp3("/home/strimble/TheVaultBTYSE/Audio/Mission Impossible Themefull theme.mp3")
laser_pew = AudioSegment.from_mp3("/home/strimble/TheVaultBTYSE/Audio/Laser Sound Effect.mp3")

gui_thread.start()
GPIO.setmode(GPIO.BOARD)

door_sensor1_pin = 37

button_pin = 12

GPIO.setup(door_sensor1_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(button_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
#------------------------------------------------------------------------
# SPI and ADC Setup
spi = adc_spi.spi_open()

while True:
    m = alsaaudio.Mixer()
    m.setvolume(100)
    adc_spi.write_adc(spi,register_map['ADCMODE'],0x8600)
    sleep(0.1)
    adc_spi.write_adc(spi,register_map['IFMODE'],0x1040)
    sleep(0.1)
    adc_spi.write_adc(spi,register_map['GPIOCON'],0x2880)
    sleep(0.1)
    adc_spi.write_adc(spi,register_map['SETUPCON0'],0x420)
    sleep(0.1)
    adc_spi.write_adc(spi,register_map['CH0'],0x8010)
    sleep(0.1)
    adc_spi.write_adc(spi,register_map['CH1'],0x8030)
    sleep(0.1)
    adc_spi.write_adc(spi,register_map['CH2'],0x8050)
    sleep(0.1)
    adc_spi.write_adc(spi,register_map['CH3'],0x8070)
    sleep(0.1)
    adc_spi.write_adc(spi,register_map['CH4'],0x8090)
    sleep(0.1)
    adc_spi.write_adc(spi,register_map['CH5'],0x80B0)
    sleep(0.1)
    adc_spi.write_adc(spi,register_map['CH6'],0x80D0)
    sleep(0.1)
    adc_spi.write_adc(spi,register_map['CH7'],0x80F0)
    sleep(0.1)
    adc_spi.write_adc(spi,register_map['CH8'],0x8110)
    sleep(0.1)
    adc_spi.write_adc(spi,register_map['CH9'],0x8130)
    sleep(0.1)
    adc_spi.write_adc(spi,register_map['CH10'],0x8150)
    sleep(0.1)
    adc_spi.write_adc(spi,register_map['CH11'],0x8170)
    sleep(0.1)
    adc_spi.write_adc(spi,register_map['CH12'],0x8190)
    sleep(0.1)
    adc_spi.write_adc(spi,register_map['CH13'],0x81B0)
    sleep(0.1)
    adc_spi.write_adc(spi,register_map['CH14'],0x81D0)
    sleep(0.1)
    adc_spi.write_adc(spi,register_map['CH15'],0x81F0)
    sleep(0.1)

    response = adc_spi.read_adc(spi,register_map['ID'])

    byte0 = '{0:08b}'.format(response[1])
    byte1 = '{0:08b}'.format(response[2])
    byte2 = '{0:08b}'.format(response[3])

    if hex(int(str(byte0+byte1),2)) == "0x38de": #check ID matches expected ID
        print("Comms Connected")
    else:
        print("Comms Failed")
          
    #-------------------------------------------------------------------------------------------------
    # Disable un-connected receiver channels
    receiver_connected = [1]*16
    on_threshold = 200000

    for i in range (100):
        adc_spi.GPIO3_LO(spi)
        adc_spi.GPIO3_HI(spi)
        adc_spi.GPIO3_LO(spi)
        sleep(0.001)
        response = adc_spi.read_adc(spi,register_map['DATA'])
        byte0 = '{0:08b}'.format(response[1])
        byte1 = '{0:08b}'.format(response[2])
        byte2 = '{0:08b}'.format(response[3])
        val = int(str(byte0+byte1+byte0),2)
        if response[4] < 16:
            if val < on_threshold:
                adc_spi.write_adc(spi,register_map['CH{0}'.format(response[4])],0x0)# Disable Channel
                receiver_connected[response[4]] = 0
    print("Channels Connected = ", receiver_connected.count(1))
    print("Ready to Start")  
    #--------------------------------------------------------------------------------------------------
    # Ensure doors are closed before Start Button can be pressed
    while True:
        door1_status = GPIO.input(door_sensor1_pin)
        button_status = GPIO.input(button_pin)
        if door1_status == 1:
            #print('Exit Door Open')
            door_status = "Open"
            time.sleep(1)
        elif door1_status == 0 and button_status == 0:
            playback = _play_with_simpleaudio(mission_impossible)
            print('GAME START')
            game_status = IN_GAME
            break
        else:
            door_status = "Closed"
    #--------------------------------------------------------------------------------------------------
    # Game Loop
    adc_data = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    adc_diff = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    timer = 0
    penalty = 0
    threshold = -75000
    laser_break = 0
    last_seconds = 0
    lines = []

    while True:
        start = time.time()
        minutes,seconds = divmod(timer, 60)
        display_time = ("%02d.%02d"% (minutes,seconds))
        if int(seconds) != int(last_seconds):
            #print("%02d:%02d"% (minutes,seconds))
            last_seconds = int(seconds)
        door1_status = GPIO.input(door_sensor1_pin)
        if door1_status == 1:
            print('Game Complete')
            break
        adc_spi.GPIO3_LO(spi)
        adc_spi.GPIO3_HI(spi)
        adc_spi.GPIO3_LO(spi)
        sleep(0.001)
    #     print(x)
        response = adc_spi.read_adc(spi,register_map['DATA'])
    #     print(response)
        byte0 = '{0:08b}'.format(response[1])
        byte1 = '{0:08b}'.format(response[2])
        byte2 = '{0:08b}'.format(response[3])
        val = int(str(byte0+byte1+byte0),2)
        if response[4] < 16:
            adc_data[response[4]].append(val)
            tmp = adc_data[response[4]][-2:]
            if len(tmp) == 2:
                adc_diff[response[4]].append(tmp[1]-tmp[0])
                if adc_diff[response[4]][-1] < threshold:
                    penalty = 10
                    laser_break = laser_break + 1
                    playback1 = _play_with_simpleaudio(laser_pew)
                    x1 = random.randint(0, screen_width)
                    y1 = 0
                    x2 = random.randint(0, screen_width)
                    y2 = screen_height
                    lines.append((x1,y1,x2,y2))
                else:
                    penalty = 0
        end = time.time()
        timer = timer+(end-start)+penalty
        
    print("number of lasers tripped = ", laser_break)
    
#     for i in range(100,1,-1):
#         m.setvolume(i)
#         sleep(0.1)
    playback.stop()
    sleep(5)
    print(timer)
    leaderboard_list = score_client.get_top_10()
    if float(timer) < (float(leaderboard_list[-1]["@Score"])*100):
        print("new score")
        game_status = RESULTS
    else:
        game_status = STANDBY

# plt.figure(1)
# plt.plot(adc_diff[0])
# plt.plot(adc_diff[1])
# plt.plot(adc_diff[2])
# plt.plot(adc_diff[3])
# plt.plot(adc_diff[4])
# plt.plot(adc_diff[5])
# plt.plot(adc_diff[6])
# plt.plot(adc_diff[7])
# plt.plot(adc_diff[8])
# plt.plot(adc_diff[9])
# plt.plot(adc_diff[10])
# plt.plot(adc_diff[11])
# plt.plot(adc_diff[12])
# plt.plot(adc_diff[13])
# plt.plot(adc_diff[14])
# plt.plot(adc_diff[15])
# plt.grid()
# plt.show()
# plt.figure(2)
# plt.plot(adc_data[0])
# plt.plot(adc_data[1])
# plt.plot(adc_data[2])
# plt.plot(adc_data[3])
# plt.plot(adc_data[4])
# plt.plot(adc_data[5])
# plt.plot(adc_data[6])
# plt.plot(adc_data[7])
# plt.plot(adc_data[8])
# plt.plot(adc_data[9])
# plt.plot(adc_data[10])
# plt.plot(adc_data[11])
# plt.plot(adc_data[12])
# plt.plot(adc_data[13])
# plt.plot(adc_data[14])
# plt.plot(adc_data[15])
# plt.grid()
# plt.show()

adc_spi.spi_close(spi)




