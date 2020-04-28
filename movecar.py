#I have a main.py on my esp32 with one simple line " import movecar "
#I haven't worked out how to have lines of code move onto a new line when they become too long in IDLE yet :(
from machine import Pin,ADC
from time import sleep_ms

# y and x joystick input pins
y=ADC(Pin(33))# Left and Right axis Anolag to digital conversion, current voltage range is 1 volt or 1024
y.atten(ADC.ATTN_11DB) # Change the maxium input range or voltage to 3.6v, im using 3.3 volts so it should read around 3350
x=ADC(Pin(32)) # Forwards and backwards, same as above
x.atten(ADC.ATTN_11DB)# Same as above

# Push button on the joystick to change modes, i'm going to swap this out for a off/on switch connecting ground and Pin 34 when switched on
push=ADC(Pin(34))# Same as above
push.atten(ADC.ATTN_11DB)
push_value=False # Set the starting controller mode to drive with Forwards,backwards,Left and right. When push_value==True Left and right will swap for sideways movements

# Label Pin 23 as a led to see which mode the push_value is in, when push_value==True the led on Pin 23 will turn on
led=Pin(23,Pin.OUT)# Label Pin 23 as an output Pin
led.off()# Turn off Pin 23 as for some reason some pins always start with 3.3v as there base value.

#Label my motors
motor_left_front1=Pin(2,Pin.OUT)#Pins are grouped in groups of 2, as you need to switch the two pins to be opposite on a motor to drive it. eg; off and on
motor_left_front2=Pin(4,Pin.OUT)

motor_left_back1=Pin(18,Pin.OUT)
motor_left_back2=Pin(19,Pin.OUT)

motor_right_front1=Pin(13,Pin.OUT)
motor_right_front2=Pin(27,Pin.OUT)

motor_right_back1=Pin(26,Pin.OUT)
motor_right_back2=Pin(25,Pin.OUT)

#Turning all the motor pins off because some will start in on position, this code can be put in the main.py "labeling the pins and turning them off"
motor_left_front1.off()
motor_left_front2.off()
motor_left_back1.off()
motor_left_back2.off()
motor_right_front1.off()
motor_right_front2.off()
motor_right_back1.off()
motor_right_back2.off()

#Turn off all motors
def stop():
	motor_right_front1.off()	
	motor_right_back1.off()	
	motor_right_front2.off()	
	motor_right_back2.off()	
	motor_left_front1.off()
	motor_left_back1.off()	
	motor_left_front2.off()
	motor_left_back2.off()

#Turn on its centre mass in counter clock wise
def mass_ccw():
	motor_left_back2.on()
	motor_right_front1.on()

#Turn on its centre mass in clock wise
def mass_cw():
        motor_left_front1.on()
        motor_right_back2.on()

#Move sideways towards the right ##Added turn off to all none needed motors at the start of all movements to enable quick changing of direction.
def right_sideways():
	motor_right_front2.off()	
	motor_right_back1.off()
	motor_left_front1.off()
	motor_left_back2.off()
        
	motor_right_front1.on()	
	motor_right_back2.on()
	motor_left_front2.on()
	motor_left_back1.on()

#Move sideways towards the left
def left_sideways():
	motor_right_front1.off()
	motor_right_back2.off()	
	motor_left_front2.off()
	motor_left_back1.off()
        
	motor_right_front2.on()
	motor_right_back1.on()	
	motor_left_front1.on()
	motor_left_back2.on()

#Move forwards
def forwards():
        motor_right_front2.off()	
	motor_right_back2.off()
	motor_left_front2.off()
	motor_left_back2.off()
	
	motor_right_front1.on()	
	motor_right_back1.on()
	motor_left_front1.on()
	motor_left_back1.on()

#Move backwards
def backwards():
	motor_right_front1.off()
	motor_right_back1.off()	
	motor_left_front1.off()
	motor_left_back1.off()
        
	motor_right_front2.on()
	motor_right_back2.on()	
	motor_left_front2.on()
	motor_left_back2.on()	

#Turn right
def right():
	motor_right_front2.off()	
	motor_right_back2.off()        
	motor_left_front1.off()		
	motor_left_back1.off()
        
	motor_right_front1.on()	
	motor_right_back1.on()        
	motor_left_front2.on()		
	motor_left_back2.on()

#Turn left
def left():
	motor_right_front1.off()
	motor_right_back1.off()        
	motor_left_front2.off()	
	motor_left_back2.off()
        
	motor_right_front2.on()
	motor_right_back2.on()        
	motor_left_front1.on()	
	motor_left_back1.on()	
sleep_ms(1000) #Sleep delay to allow for usb connection before it's trapped in the while loop

while True: #Loop forever
        sleep_ms(2)# Smallest amount of delay to allow the motors to turn on
        if push.read()==0: # Check if Pin 34 has been pushed down with a 0v reading
                push_value=True # push_value=True means it is in sideways drive mode
                led.on() # Turn on the led to reflect which mode it is in
        else: # The first time the joystick push down button is pressed it enter's this, changing the controller mode to sideways
                push_value=False # push_value=False means it is in normal drive mode
                led.off() # Turn off the led to reflect which mode it is in

	if y.read() <=50: # Check Pin 33, if the value is less than 150 the joystick has been pushed right
                if push_value==True: # Check the controller mode
                        right_sideways() # Move sideways to the right if it's True
                else: # if push_value==False turn right
                        right()

	elif y.read()>=3250: # Check Pin 33, if the value is greater than 3150 the joystick has been pushed left
                if push_value==True: # Check the controller mode
                        left_sideways() # Move sideways to the left if it's True
                else: # if push_value==False turn left
                        left()

	elif x.read() <=50: # Check Pin 32, if the value is less than 150 the joystick has been pushed backwards
                #if push_value==True: #Commented out because it's currently not working, the motors are coded right though
                        #mass_ccw() # Correct motor directions currently not working though
                #else:
                backwards() # Move backwards
	elif x.read() >=3250:
                #if push_value==True: # Same as above
                        #mass_cw() # Same as above
                #else:
                forwards() # Move forwards
	else: # if all of the above conditions aren't met turn the motors off
		stop() # Turns the motors off
