import math
import time
import keyboard
import os
import msvcrt as key
os.system('cls')
gravityconst = 6.674e-11
keyboard.send('F11')
zoom = 100
camy = 0
camx = 0
mindist = 1e100
maxdist = 0
minspeed = 1e100
maxspeed = 0
#Y,X,Y Velocity,X Velocity,Mass,Gravitational Force,Ansi code
bodies = [[2000,3000,-20,0,1e15,0,"\033[96m"],
          [2000,5000,20,0,1e15,0,"\033[92m"],
          [2000,4000,0,0,1e16,0,"\033[97m"]]
while True:
    button = []
    while key.kbhit():
        button += [key.getch().decode("ASCII")]
    for i in button:
        if i == "q":
            zoom /= 10
        elif i == "e":
            zoom *= 10
        elif i == "w":
            camy -= 1
        elif i == "s":
            camy += 1
        elif i == "d":
            camx -= 1
        elif i == "a":
            camx += 1
        elif i == "r":
            camx = 0
            camy = 0
        elif i == "v":
            zoom = int(input("Input zoom level"))
    print('\033[100A',end='')
    for i in range(50,0,-1):
        for j in range(104):
            placed = False
            for k in range(len(bodies)):
                if i == round(bodies[k][0]/zoom+camy) and j == round(bodies[k][1]/zoom+camx):
                    print(bodies[k][6],end='')
                    print('.',end='')
                    print("\033[97m",end=' ')
                    placed = True
            if placed == False:
                print(' ',end=' ')
        print('')
    for k in range(len(bodies)):
        for b in range(len(bodies)):
            if k != b:
                #Distance between objects
                bodydist = math.sqrt((bodies[k][0]-bodies[b][0])**2+(bodies[k][1]-bodies[b][1])**2)
                if bodydist > maxdist:
                    maxdist = bodydist
                if bodydist < mindist:
                    mindist = bodydist
                #Overall gravity affecting both objects
                gengravity = gravityconst*(bodies[k][4]*bodies[b][4])/(bodydist**2)
                #Set gravitational force for measurement
                bodies[k][5] = gengravity/bodies[k][4]
                #Find the x portion and y portion of the distance between two bodies as fractions
                yfrac = ((bodies[k][0]-bodies[b][0])**2)/((bodies[k][0]-bodies[b][0])**2+(bodies[k][1]-bodies[b][1])**2)
                xfrac = ((bodies[k][1]-bodies[b][1])**2)/((bodies[k][0]-bodies[b][0])**2+(bodies[k][1]-bodies[b][1])**2)
                #Find the amount the gravity is affecting the body in each direction
                ypart = (yfrac*gengravity)/bodies[k][4]
                xpart = (xfrac*gengravity)/bodies[k][4]
                #Apply direction of gravity based on position
                if bodies[k][0] > bodies[b][0]:
                    #Body K is above Body B
                    bodies[k][2] -= ypart
                elif bodies[k][0] < bodies[b][0]:
                    #Body K is below Body B
                    bodies[k][2] += ypart
                if bodies[k][1] > bodies[b][1]:
                    #Body K is to the right of Body B
                    bodies[k][3] -= xpart
                elif bodies[k][1] < bodies[b][1]:
                    #Body K is to the left of Body B
                    bodies[k][3] += xpart
    for k in range(len(bodies)):
        bodies[k][0] += bodies[k][2]
        bodies[k][1] += bodies[k][3]
    speed = math.sqrt(bodies[1][2]**2+bodies[1][3]**2)
    if speed > maxspeed:
        maxspeed = speed
    if speed < minspeed:
        minspeed = speed
    print(f"Sun gravitational force:{bodies[0][5]:.2e}                              ")
    print(f"Earth gravitational force:{bodies[1][5]:.2e}                              ")
    print(f"Current distance:{bodydist:.2e}                              ")
    print(f"Periapsis distance:{mindist:.2e} Apoapsis distance:{maxdist:.2e}                              ")
    print(f"Current Earth speed:{speed:.2e}                              ")
    print(f"Minimum Earth speed:{minspeed:.2e} Maximum speed:{maxspeed:.2e}                              ")
    print('\033[100A',end='')
    print('\033[?25l',end='')
    
    
