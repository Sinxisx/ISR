
from sr.robot import *

import time

SEARCHING, DRIVING = range(2)

R = Robot()

MARKER_TOKENS = (MARKER_TOKEN, MARKER_TOKEN_A, MARKER_TOKEN_B, MARKER_TOKEN_C)

token_filter = lambda m: m.info.marker_type in MARKER_TOKENS

def drive(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def angleR(theta):
    R.motors[0].m0.power = 60
    R.motors[0].m1.power = -60
    seconds = theta*0.0055555555555555555555556
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def angleL(theta):
    R.motors[0].m0.power = -60
    R.motors[0].m1.power = 60
    seconds = theta*0.0055555555555555555555556
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

state = SEARCHING

while True:
    if state == SEARCHING:
        print "Searching..."
        tokens = filter(token_filter, R.see())
        if len(tokens) > 0:
            m = tokens[0]
            print "Token sighted. {0} is {1}m away, bearing {2} degrees." \
                  .format(m.info.offset, m.dist, m.rot_y)
            state = DRIVING

        else:
            print "Can't see anything."
            turn(25, 0.3)
            time.sleep(0.2)

    elif state == DRIVING:
        print "Aligning..."
        tokens = filter(token_filter, R.see())
        if len(tokens) == 0:
            state = SEARCHING

        else:
            m = tokens[0]
            if m.dist < 0.4:
                print "Found it!"
                if R.grab():
                    print "Gotcha!"
                    drive(50, 1)
                    R.release()
                    drive(-50, 0.5)
                    angleR(180)
                    drive(50,1)
                    angleL(90)
                    drive(50,1)
                else:
                    print "Aww, I'm not close enough."



            elif -15 <= m.rot_y <= 15:
                print "Ah, that'll do."
                drive(50, 0.5)

            elif m.rot_y < -15:
                print "Left a bit..."
                turn(-12.5, 0.5)

            elif m.rot_y > 15:
                print "Right a bit..."
                turn (12.5, 0.5)
