import math
import time
import keyboard
import os
import copy
import msvcrt as key
gravityconst = 6.674e-11
height = 49
width = 118
keyboard.send('F11')
scale = 100
camy = 0
camx = 0
framerate = 0
frames = 0
time1 = time.time()
colors = {"black":"\033[38;5;0m",
          "red":"\033[38;5;1m",
          "green":"\033[38;5;2m",
          "yellow":"\033[38;5;3m",
          "blue":"\033[38;5;4m",
          "purple":"\033[38;5;5m",
          "cyan":"\033[38;5;6m",
          "silver":"\033[38;5;7m",
          "grey":"\033[38;5;8m",
          "brightred":"\033[38;5;9m",
          "brightgreen":"\033[38;5;10m",
          "brightyellow":"\033[38;5;11m",
          "brightblue":"\033[38;5;12m",
          "pink":"\033[38;5;13m",
          "brightcyan":"\033[38;5;14m",
          "white":"\033[38;5;15m"}
requestlist = {"camhelper":0,
               "pos":1,
               "bodyspeed":2,
               "gravitationalforce":3,
               "gravitationalforce2":4,
               "bodydist":5,
               "speedmeasure":6,
               "orbitdist":7}
while True:
    try:
        (bodycode,requestcode) = input("Input body and data combination code:").split('; ')
        bodycode = bodycode.split(', ')
        bodies = []
        #Y, X, Y Velocity, X Velocity, Mass, Color, Name
        for i in range(len(bodycode)):
            bodycode[i] = bodycode[i].split('.')
            bodies += [[int(float(bodycode[i][0])),int(float(bodycode[i][1])),int(float(bodycode[i][2])),int(float(bodycode[i][3])),int(float(bodycode[i][4])),colors[bodycode[i][5].lower()],bodycode[i][6]]]
        requestcode = requestcode.split(', ')
        requests = []
        for i in range(len(requestcode)):
            requestcode[i] = requestcode[i].split('.')
            match requestlist[requestcode[i][0]]:
                case 0: #ID
                    requests += [[requestlist[requestcode[i][0]],0]]
                case 1|2: #ID, Target 1
                    requests += [[requestlist[requestcode[i][0]],int(requestcode[i][1])]]
                case 3|4|5: #ID, Target 1, Target 2
                    requests += [[requestlist[requestcode[i][0]],int(requestcode[i][1]),int(requestcode[i][2])]]
                case 6:
                    requests += [[requestlist[requestcode[i][0]],int(requestcode[i][1]),0,1e100]]
                case 7: #ID, Target 1, Target 2, 3-8 bullshit, Show Orbit, Orbit Color
                    requests += [[requestlist[requestcode[i][0]],int(requestcode[i][1]),int(requestcode[i][2]),0,0,0,1e100,0,0,int(requestcode[i][3]),colors[requestcode[i][4].lower()]]]
    except:
        print("Invalid code, read the included guide")
    else:
        break
requestsorig = copy.deepcopy(requests)
os.system('cls')
print('\033[?25l',end='')
while True:
    button = []
    while key.kbhit():
        button += [key.getch().decode("ASCII")]
    for i in button:
        match i:
            case "q":
                scale /= 10
            case "e":
                scale *= 10
            case "w":
                camy += 1
            case "s":
                camy -= 1
            case "d":
                camx += 1
            case "a":
                camx -= 1
            case "r":
                camx = 0
                camy = 0
            case "v":
                scale = int(input("Input scale level"))
            case "p":
                requests = copy.deepcopy(requestsorig)
    for i in range(height,0,-1):
        for j in range(width):
            placed = False
            for k in range(len(bodies)):
                if i == round(bodies[k][0]/scale-camy+height/2) and j == round(bodies[k][1]/scale-camx+width/2) and placed == False:
                    print(bodies[k][5],end='')
                    print('.',end='')
                    print(colors["white"],end=' ')
                    placed = True
            for g in range(len(requests)):
                if requests[g][0] == 7:
                    if requests[g][9] == 1 and placed == False:
                        if (i == round(requests[g][4]/scale-camy+height/2) and j == round(requests[g][5]/scale-camx+width/2)) or (i == round(requests[g][7]/scale-camy+height/2) and j == round(requests[g][8]/scale-camx+width/2)):
                            print(requests[g][10],end='')
                            print(',',end='')
                            print(colors["white"],end=' ')
                            placed = True
            if placed == False:
                print(' ',end=' ')
        print('')
    for k in range(len(bodies)):
        for b in range(len(bodies)):
            if k != b:
                #Distance between objects
                bodydist = ((bodies[k][0]-bodies[b][0])**2+(bodies[k][1]-bodies[b][1])**2)**0.5
                #Overall gravity affecting both objects
                gengravity = gravityconst*(bodies[k][4]*bodies[b][4])/(bodydist**2)
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
    for i in range(len(requests)):
        k = requests[i][1]
        match requests[i][0]:
            case 0:
                print(f"Camera vector:({camx},{camy}) scale:{int(scale)}",end='')
                for l in range(len(bodies)):
                    print(f", {bodies[l][6]} vector:({round(bodies[l][1]/scale-camx)},{round(bodies[l][0]/scale-camy)})",end='')
                print("\033[K")
            case 1: #Target 1
                print(f"{bodies[k][6]} position:({bodies[k][1]:.2e},{bodies[k][0]:.2e}) \033[K")
            case 2: #Target 1
                speed = (bodies[k][2]**2+bodies[k][3]**2)**0.5
                print(f"{bodies[k][6]} speed per tick:{speed:.2e}m \033[K")
            case 3: #Target 1, Target 2
                b = requests[i][2]
                bodydist = ((bodies[k][0]-bodies[b][0])**2+(bodies[k][1]-bodies[b][1])**2)**0.5
                tempgrav = (gravityconst*(bodies[k][4]*bodies[b][4])/(bodydist**2))
                print(f"Shared gravitational force between {bodies[k][6]} and {bodies[b][6]}:{tempgrav:.2e}N \033[K")
            case 4: #Target 1, Target 2
                b = requests[i][2]
                bodydist = ((bodies[k][0]-bodies[b][0])**2+(bodies[k][1]-bodies[b][1])**2)**0.5
                tempgrav = (gravityconst*(bodies[k][4]*bodies[b][4])/(bodydist**2))/bodies[k][4]
                print(f"{bodies[k][6]} gravitational force with {bodies[b][6]}, adjusted for {bodies[k][6]}'s mass:{tempgrav:.2e}N \033[K")
            case 5: #Target 1, Target 2
                b = requests[i][2]
                bodydist = ((bodies[k][0]-bodies[b][0])**2+(bodies[k][1]-bodies[b][1])**2)**0.5
                print(f"Distance between {bodies[k][6]} and {bodies[b][6]}:{bodydist:.2e}m \033[K")
            case 6: #Target 1, Max Speed, Min Speed
                speed = (bodies[k][2]**2+bodies[k][3]**2)**0.5
                if speed > requests[i][2]:
                    requests[i][2] = speed
                if speed < requests[i][3]:
                    requests[i][3] = speed
                print(f"{bodies[k][6]} Minimum speed per tick:{requests[i][3]:.2e}m Maximum speed per tick:{requests[i][2]:.2e}m \033[K")
            case 7: #Target 1, Target 2, Apoapsis dist, y, x, Periapsis dist, y, x, show orbit, periapsis and apoapsis color
                b = requests[i][2]
                bodydist = ((bodies[k][0]-bodies[b][0])**2+(bodies[k][1]-bodies[b][1])**2)**0.5
                if bodydist > requests[i][3]:
                    requests[i][3] = bodydist
                    requests[i][4] = bodies[k][0]
                    requests[i][5] = bodies[k][1]
                if bodydist < requests[i][6]:
                    requests[i][6] = bodydist
                    requests[i][7] = bodies[k][0]
                    requests[i][8] = bodies[k][1]
                print(f"Of {bodies[k][6]} relative to {bodies[b][6]}, Est. Apoapsis:({requests[i][5]:.2e},{requests[i][4]:.2e}),{requests[i][3]:.2e}m Est. Periapsis:({requests[i][8]:.2e},{requests[i][8]:.2e}),{requests[i][6]:.2e}m \033[K")
                #print(f"{requests[i][3]+requests[i][6]:.2e},{((requests[i][5]-requests[i][7])**2+(requests[i][4]-requests[i][8])**2)**0.5:.2e}")
    frames += 1
    if frames == 10:
        framerate = int(1/((time.time()-time1)/10))
        time1 = time.time()
        frames = 0
    print(f"FPS: {framerate} \033[K")
    print(requestsorig)
    print("\033[J")
    print('\033[100A')
