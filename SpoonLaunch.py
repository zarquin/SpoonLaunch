#launchSpoon

import traceback
import better_exceptions
import launchpad

import argparse
import random
import time
from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import osc_message_builder
from pythonosc import udp_client


###########################################
class LaunchpadState():
    
    def __init__(self, client, launch_ctrl):
        self.slice_modes  =   ['PLY','MTE','SKP','RVS','RND','DBL','HLF']
        # play green  64
        # mute red  5
        # skip black 0 
        # reverse yellow not 8
        # rand dark blue 67?
        # double pink  54
        # half cyan 40
        self.slice_mode_codes = [64,5,0,9,67,54,40]
        self.loop_modes = ['STOP','PLAY','REVS','RAND']
        self.loop_mode_codes = [0,64,54,67]
        self.slice_states = []
        self.osc_client = client
        self.launchpad = launch_ctrl
        self.cs = {'PLY':0, 'MTE':1, 'SKP':2, 'RVS':3, 'RND':4, 'DBL':5, 'HLF':6}
        
        self.osc_slice_string = "/loop/{}/slice/{}"
        
        for i in range(0,4):
            temp=[]
            for j in range(0,8):
                temp.append(0)
            
            self.slice_states.append(temp)
        
        self.loop_states = [0,0,0,0]
        
        print("finished setting up state")
        return
    
    def send_load_change(self, loop_message,new_index):
        temp_s = loop_message
        temp_m = new_index
        self.osc_client.send_message(temp_s, temp_m  )
        print("sent message : {}   {}".format(temp_s, temp_m))
        #We don't know if the file load was sucessful or not.  
        # We need to send all the slice states for this loop to 
        #make it match what we're displaying

        #sleep for a little bit. Loading a file seems to get messages lost.
        time.sleep(0.1)

        loopi_i=int(loop_message[6])-1

        for j in range(0,8):
            temp_s = self.osc_slice_string.format(loopi_i+1,j)
            temp_m = self.slice_modes[self.slice_states[loopi_i][j]]
            self.osc_client.send_message(temp_s,temp_m)
            print("sent message: {} {}".format(temp_s, temp_m))
        
        #send the current playing mode.
        temp_s = "/loop/{}/mode".format(loopi_i+1)
        temp_m = self.loop_modes[self.loop_states[loopi_i]]
        self.osc_client.send_message(temp_s,temp_m)
        print("sent message {} {}".format(temp_s, temp_m))


        return
        
    
    def set_slice_led(self,loop_i, slice_i):
        state = self.slice_states[loop_i][slice_i]
        led_code = self.slice_mode_codes[state]
        self.launchpad.LedCtrlXYByCode(slice_i,loop_i+1,led_code)
    
    def set_loop_led(self,loop_i):
        state = self.loop_states[loop_i]
        led_code = self.loop_mode_codes[state]
        self.launchpad.LedCtrlXYByCode(8, loop_i+1,led_code)
    
    def update_all_states(self):
        """transmit teh current states of all slices and loops"""
        
        for l in range(0,4):
            temp_s = "/loop/{}/mode".format(l+1) # stupid using loop 1 to 4
            temp_m = self.loop_modes[self.loop_states[l]]
            self.osc_client.send_message(temp_s,temp_m)
            print("sent_message {} {}".format(temp_s,temp_m))
            self.set_loop_led(l)
        
        for l in range(0,4):
            for s in range(0,8):
                temp_s = self.osc_slice_string.format(l+1,s)
                temp_m = self.slice_modes[self.slice_states[l][s] ]
                self.osc_client.send_message(temp_s,temp_m)
                print("sent message {} {}".format(temp_s, temp_m))
                self.set_slice_led(l,s)
        return
        
    def next_slice_mode(self,loop_number, slice_number, new_mode):
        # increment slice
        vol_vals=[0.,0.1,0.3,0.4,0.5,0.6,0.8,1.0]
        if(new_mode=="VOL"):
        # send a volume message!
            temp_s = "/loop/{}/volume".format(loop_number+1)
            temp_m = vol_vals[slice_number]
            self.osc_client.send_message(temp_s, temp_m  )
            print("sent message : {}   {}".format(temp_s, temp_m))
            return
        
        if new_mode == None:
            val = self.slice_states[loop_number][slice_number]
            val+=1
        else:
            if(new_mode in self.cs.keys()):
                val = self.cs[new_mode]
            else:
                val =0 
        # check if we've wrapped
        if(val>6):
            val=0
            
        self.slice_states[loop_number][slice_number] = val
            
        #send OSC message
        temp_s = self.osc_slice_string.format(loop_number+1,slice_number)
        temp_m = self.slice_modes[val]
        self.osc_client.send_message(temp_s, temp_m  )
        self.set_slice_led(loop_number,slice_number)
        print("sent message : {}   {}".format(temp_s, temp_m))
        return
    
    def send_loop_reset(self, loop_number):
        temp_s = "/loop/{}/jump".format(loop_number+1)
        temp_m = 0
        self.osc_client.send_message(temp_s, temp_m)
        self.set_loop_led(loop_number)
        print("sent message {} {}".format(temp_s,temp_m))
        return
    
    def set_loop_mode_stop(self,loop_number):
        # if already stopped, do a reset
        if(self.loop_states[loop_number] == 0):
            self.send_loop_reset(loop_number)
            return
    
        self.loop_states[loop_number]=0
        #send OSC message
        temp_s = "/loop/{}/mode".format(loop_number+1)
        temp_m = self.loop_modes[self.loop_states[loop_number]]
        self.osc_client.send_message(temp_s, temp_m)
        self.set_loop_led(loop_number)
        print("sent message {} {}".format(temp_s,temp_m))
        return
    
    def next_loop_mode(self, loop_number):
        self.loop_states[loop_number]+=1
        if(self.loop_states[loop_number]>3):
            self.loop_states[loop_number]=0
        
        #send OSC message
        temp_s = "/loop/{}/mode".format(loop_number+1)
        temp_m = self.loop_modes[self.loop_states[loop_number]]
        self.osc_client.send_message(temp_s, temp_m)
        self.set_loop_led(loop_number)
        print("sent message {} {}".format(temp_s,temp_m))
        return
        
    def send_all_loop_jump(self, new_slice_number):
        for i in range(0,4):
            temp_s="/loop/{}/jump".format(i+1)
            temp_m = self.osc_client.send_message(temp_s, new_slice_number)
            print("sent message {} {}".format(temp_s,new_slice_number))
        return

#########################################################

held_button = None

#dictionary of messages that can be sent.
tete = {0:'PLY',1:'MTE',2:'SKP',3:'RVS',4:'RND',5:'DBL',6:'HLF', 9:'VOL' , 
    100:'/loop/1/file', 101:'/loop/2/file',102:'/loop/3/file', 103:'/loop/4/file'}
#associated colour codes
colours = {0:64, 1:5, 2:0, 3:9, 4:67, 5:54, 6:40}

def draw_hold_buttons():
    """draw the 7 buttons that are the hold down"""
    start_x = 0
    start_y = 6
    # [64,5,0,9,67,54,40]
    lp.LedCtrlXYByCode(start_x,start_y,64) # play colour
    lp.LedCtrlXYByCode(start_x+1,start_y,5) # mute
    lp.LedCtrlXYByCode(start_x+2,start_y,0) # skip
    lp.LedCtrlXYByCode(start_x+3,start_y,9) # reverse
    lp.LedCtrlXYByCode(start_x+4,start_y,67) # random
    lp.LedCtrlXYByCode(start_x+5,start_y,54) # random
    lp.LedCtrlXYByCode(start_x+6,start_y,40) # random
    return
    
def track_loading_buttons(midi_message):
    global held_button, tete
    # track load buttons are 0-3 for tracks 1-4
    btn_x = midi_message[0]
    
    #if velocity = 0 set held_button to None
    if(midi_message[2]<10):
        held_button = None
        return
    
    if (btn_x<0 or btn_x>3):
        # do nothing 
        
        return
    offset = btn_x+100
    held_button = tete[offset]
    print("setting load mode {}".format(held_button))
    return

def change_track_load(midi_message, lpsnst):
    global held_button
    # convert x y to a number
    btn_x = midi_message[0]
    btn_y = midi_message[1]-1
    file_index = btn_y*8+btn_x
    # send file index 
    lpsnst.send_load_change(held_button, file_index)
    return
    
    
    
def track_hold_buttons(midi_message):
    global held_button, tete, colours
    modes=['PLY','MTE','SKP','RVS','RND','DBL','HLF']
    btn_x = midi_message[0]
    
    if(btn_x not in tete.keys() ):
        held_button = None
        print("button abort release {} {}".format(midi_message,held_button))
        return
    
    if(midi_message[2]==0):
        held_button = None
        print("button released {}".format(held_button))
    else:
        held_button = tete[ midi_message[0] ]
        print("button held {} {}".format(midi_message, held_button))
    return

def decode_xy(midi_message, lnchpdState, verbose_mode):
    # if button is one of the hold buttons, then have it handled.
    poorpractice=['/loop/1/file', '/loop/2/file','/loop/3/file', '/loop/4/file']
    if(verbose_mode):
        print("button recieved {}".format(midi_message))
    
    if(midi_message[1] == 6):
        track_hold_buttons(midi_message)
        return
    #file loading we need to do something fancy here.    
    if(midi_message[1] == 9):
        track_loading_buttons(midi_message)
        return
    
    
    # check velocity if 0 do nothing
    if(midi_message[2] <10):
        return
        
    if(held_button in poorpractice):
        change_track_load(midi_message, lnchpdState)
        return
    
    val_x = midi_message[0] # 0 -9 0-7 are slices, 8 and 9 are loops 
    val_y = midi_message[1] # 1-4
    # if x out of range, do nothing
    if(val_x <0 or val_x > 9):
        return
    # if y out of range, do nothing
    if(val_y <0 or val_y > 4): #1-4 are slices.  0 is top row for all jump
        return
    # because i'm a numpty, update val_y to 0-3
    
    if(val_y==0):
        # do an all slice jump
        if(val_x<0 or val_x>7):
            # error,
            print("error")
            return
        lnchpdState.send_all_loop_jump(val_x)
        return
    
    val_y=val_y-1
    # print("y {} x {}".format(val_y,val_x))
    if(val_x == 8):
        lnchpdState.next_loop_mode(val_y)
        return
    if(val_x == 9):
        lnchpdState.set_loop_mode_stop(val_y)
    else:
        lnchpdState.next_slice_mode(val_y,val_x, held_button)
    return


def main(verbose_mode):
    """the main loop"""
    while True:
        # 500Hz refresh rate
        time.sleep(0.002)
        ret_d = lp.ButtonStateXY()
        # only do som
        if(len(ret_d)>0):
            # print(ret_d)
            decode_xy(ret_d, lps,verbose_mode) 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1",
        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=5080,
        help="The port the OSC server is listening on")
    
    parser.add_argument("--print_messages",action="store_true",help="print the midi message recieved")
    
    args = parser.parse_args()
    client = udp_client.SimpleUDPClient(args.ip, args.port)
    
    lp = launchpad.LaunchpadPro()
    #not very complex.  only expecting one to be here
    
    lp.Open(0)
    
    lp.LedAllOn()
    time.sleep(0.1)
    lp.Reset()
    lp.ButtonFlush()
    
    #do the initialisation
    lps = LaunchpadState(client, lp) 
    lps.update_all_states()
    
    draw_hold_buttons()
    
    #start endless loop
    main(args.print_messages)
