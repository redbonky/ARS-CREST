import math
import time
import keyboard
import os
import copy
import msvcrt
import ctypes
gravityconst = 6.674e-11
keyboard.send('F11')
time.sleep(0.1)
kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 128)
scale = 64
simspeed = 1
camy = 0
camx = 0
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
               "particlespeed":2,
               "gravitationalforce":3,
               "gravitationalforce2":4,
               "particledist":5,
               "speedmeasure":6,
               "orbitdist":7}
def input2(text=""):
    while msvcrt.kbhit():
        msvcrt.getch()
    val = input(text)
    return val
def print2(*args):
    print(*args,sep="",end="")
    return
def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))
def getWindow():
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
    buff = ctypes.create_unicode_buffer(length + 1)
    ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
    return (buff.value, hwnd)
os.system("title Orbit Sim")
print2('\033[?25l')
try:
    open("settings.txt","x")
except FileExistsError:
    pass
filedata = open("settings.txt","r").readlines()
if len(filedata) != 2:
    filedata = ""
    print2("\033[2J")
    border = [209,56]
    while True:
        if keyboard.is_pressed("w"):
            border[1] -= 1
            print2("\033[2J")
        if keyboard.is_pressed("s"):
            border[1] += 1
            print2("\033[2J")
        if keyboard.is_pressed("a"):
            border[0] -= 1
            print2("\033[2J")
        if keyboard.is_pressed("d"):
            border[0] += 1
            print2("\033[2J")
        if keyboard.is_pressed("space"):
            windowsize = [border[0],border[1]]
            break
        print2("\033[",round(border[1]/2),"H")
        print2("\033[",round(border[0]/2),"GWindow height: ",border[1],"\n")
        print2("\033[",round(border[0]/2),"GWindow width: ",border[0],"\n")
        print2("\033[",round(border[0]/2),"GUse WASD to move borders until they're at the furthest corners\n")
        print2("\033[",round(border[0]/2),"Gof your screen while staying fully visible and not glitching\n")
        print2("\033[",round(border[0]/2),"GUse spacebar to confirm screen size\n")
        print2("\033[",round(border[0]/2),"G(on the computers I expect this to be used on the width should be 209 and height 56)")
        print2("\033[H+------\n")
        for a in range(4):
            print2("|\n")
        print2("\033[",border[1]-5,"H")
        for a in range(4):
            print2("|\n")
        print2("+------\n\033[H")
        print2("\033[",border[0]-6,"G------+\n")
        for a in range(4):
            print2("\033[",border[0],"G|\n")
        print2("\033[",border[1]-5,"H")
        for a in range(4):
            print2("\033[",border[0],"G|\n")
        print2("\033[",border[0]-6,"G------+\n")
        time.sleep(0.1)
    filedata += str(windowsize[0])+"\n"
    filedata += str(windowsize[1])+"\n"
    with open("settings.txt","w") as file:
        for row in filedata:
            file.write(row)
with open("settings.txt","r") as file:
    content = file.readlines()
    windowsize = (int(content[0].strip()),int(content[1].strip()))
width = int(windowsize[0]/2)-1
height = windowsize[1]-10
os.system("cls")
while True:
    try:
        (particlecode,requestcode) = input2("Input particle and data combination code:").split('; ')
        particlecode = particlecode.split(', ')
        particles = []
        #Y, X, Y Velocity, X Velocity, Mass, Color, Name
        for i in range(len(particlecode)):
            particlecode[i] = particlecode[i].split('.')
            particles += [[int(float(particlecode[i][0])),int(float(particlecode[i][1])),int(float(particlecode[i][2])),int(float(particlecode[i][3])),int(float(particlecode[i][4])),colors[particlecode[i][5].lower()],particlecode[i][6]]]
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
                case 7: #ID, Target 1, Target 2, 3-8 stuff, Show Orbit, Orbit Color
                    requests += [[requestlist[requestcode[i][0]],int(requestcode[i][1]),int(requestcode[i][2]),0,0,0,1e100,0,0,int(requestcode[i][3]),colors[requestcode[i][4].lower()]]]
    except:
        print2("\nInvalid code, read the included guide\n")
    else:
        break
requestsorig = copy.deepcopy(requests)
os.system("cls")
while True:
    while getWindow()[0] != "Orbit Sim":
        time.sleep(0.1)
    if keyboard.is_pressed("q"):
        scale /= 2
    if keyboard.is_pressed("e"):
        scale *= 2
    if keyboard.is_pressed("z"):
        simspeed /= 2
    if keyboard.is_pressed("c"):
        simspeed *= 2
    if keyboard.is_pressed("w"):
        camy += 1
    if keyboard.is_pressed("s"):
        camy -= 1
    if keyboard.is_pressed("d"):
        camx += 1
    if keyboard.is_pressed("a"):
        camx -= 1
    if keyboard.is_pressed("r"):
        camx = 0
        camy = 0
    if keyboard.is_pressed("p"):
        requests = copy.deepcopy(requestsorig)
    scale = clamp(scale,1,scale)
    simspeed = clamp(simspeed,1,512)
    for i in range(height,0,-1):
        for j in range(width):
            placed = False
            for k in range(len(particles)):
                if i == round(particles[k][0]/scale-camy+height/2) and j == round(particles[k][1]/scale-camx+width/2) and placed == False:
                    print2(particles[k][5])
                    print2('.')
                    print2(colors["white"],' ')
                    placed = True
            for g in range(len(requests)):
                if requests[g][0] == 7:
                    if requests[g][9] == 1 and placed == False:
                        if (i == round(requests[g][4]/scale-camy+height/2) and j == round(requests[g][5]/scale-camx+width/2)) or (i == round(requests[g][7]/scale-camy+height/2) and j == round(requests[g][8]/scale-camx+width/2)):
                            print2(requests[g][10])
                            print2(',')
                            print2(colors["white"],' ')
                            placed = True
            if placed == False:
                print2('  ')
        print2('\n')
    for k in range(len(particles)):
        for b in range(len(particles)):
            if k != b:
                #Distance between objects
                particledist = ((particles[k][0]-particles[b][0])**2+(particles[k][1]-particles[b][1])**2)**0.5
                #Overall gravity affecting both objects
                gengravity = gravityconst*(particles[k][4]*particles[b][4])/(particledist**2)
                #Find the x portion and y portion of the distance between two particles as fractions
                yfrac = ((particles[k][0]-particles[b][0])**2)/((particles[k][0]-particles[b][0])**2+(particles[k][1]-particles[b][1])**2)
                xfrac = ((particles[k][1]-particles[b][1])**2)/((particles[k][0]-particles[b][0])**2+(particles[k][1]-particles[b][1])**2)
                #Find the amount the gravity is affecting the particle in each direction
                ypart = (yfrac*gengravity)/particles[k][4]
                xpart = (xfrac*gengravity)/particles[k][4]
                #Apply direction of gravity based on position
                if particles[k][0] > particles[b][0]:
                    #particle K is above particle B
                    particles[k][2] -= ypart/20*simspeed
                elif particles[k][0] < particles[b][0]:
                    #particle K is below particle B
                    particles[k][2] += ypart/20*simspeed
                if particles[k][1] > particles[b][1]:
                    #particle K is to the right of particle B
                    particles[k][3] -= xpart/20*simspeed
                elif particles[k][1] < particles[b][1]:
                    #particle K is to the left of particle B
                    particles[k][3] += xpart/20*simspeed
    for k in range(len(particles)):
        particles[k][0] += particles[k][2]/20*simspeed
        particles[k][1] += particles[k][3]/20*simspeed
    for i in range(len(requests)):
        k = requests[i][1]
        match requests[i][0]:
            case 0:
                print2(f"Camera vector:({camx},{camy}) scale:{int(scale)} speed:{int(simspeed)}")
                for l in range(len(particles)):
                    print2(f", {particles[l][6]} vector:({round(particles[l][1]/scale-camx)},{round(particles[l][0]/scale-camy)})")
                print2("\033[K\n")
            case 1: #Target 1
                print2(f"{particles[k][6]} position:({particles[k][1]:.2e},{particles[k][0]:.2e}) \033[K\n")
            case 2: #Target 1
                speed = (particles[k][2]**2+particles[k][3]**2)**0.5
                print2(f"{particles[k][6]} speed:{speed:.2e}m/s \033[K\n")
            case 3: #Target 1, Target 2
                b = requests[i][2]
                particledist = ((particles[k][0]-particles[b][0])**2+(particles[k][1]-particles[b][1])**2)**0.5
                tempgrav = (gravityconst*(particles[k][4]*particles[b][4])/(particledist**2))
                print2(f"Shared gravitational force between {particles[k][6]} and {particles[b][6]}:{tempgrav:.2e}N \033[K\n")
            case 4: #Target 1, Target 2
                b = requests[i][2]
                particledist = ((particles[k][0]-particles[b][0])**2+(particles[k][1]-particles[b][1])**2)**0.5
                tempgrav = (gravityconst*(particles[k][4]*particles[b][4])/(particledist**2))/particles[k][4]
                print2(f"{particles[k][6]} gravitational force with {particles[b][6]}, adjusted for {particles[k][6]}'s mass:{tempgrav:.2e}N \033[K\n")
            case 5: #Target 1, Target 2
                b = requests[i][2]
                particledist = ((particles[k][0]-particles[b][0])**2+(particles[k][1]-particles[b][1])**2)**0.5
                print2(f"Distance between {particles[k][6]} and {particles[b][6]}:{particledist:.2e}m \033[K\n")
            case 6: #Target 1, Max Speed, Min Speed
                speed = (particles[k][2]**2+particles[k][3]**2)**0.5
                if speed > requests[i][2]:
                    requests[i][2] = speed
                if speed < requests[i][3]:
                    requests[i][3] = speed
                print2(f"{particles[k][6]} Minimum speed:{requests[i][3]:.2e}m/s Maximum speed:{requests[i][2]:.2e}m/s \033[K\n")
            case 7: #Target 1, Target 2, Apoapsis dist, y, x, Periapsis dist, y, x, show orbit, periapsis and apoapsis color
                b = requests[i][2]
                particledist = ((particles[k][0]-particles[b][0])**2+(particles[k][1]-particles[b][1])**2)**0.5
                if particledist > requests[i][3]:
                    requests[i][3] = particledist
                    requests[i][4] = particles[k][0]
                    requests[i][5] = particles[k][1]
                if particledist < requests[i][6]:
                    requests[i][6] = particledist
                    requests[i][7] = particles[k][0]
                    requests[i][8] = particles[k][1]
                print2(f"Of {particles[k][6]} relative to {particles[b][6]}, Est. Apoapsis:({requests[i][5]:.2e},{requests[i][4]:.2e}),{requests[i][3]:.2e}m Est. Periapsis:({requests[i][8]:.2e},{requests[i][8]:.2e}),{requests[i][6]:.2e}m \033[K\n")
                #print2(f"{requests[i][3]+requests[i][6]:.2e},{((requests[i][5]-requests[i][7])**2+(requests[i][4]-requests[i][8])**2)**0.5:.2e}")
    time.sleep(0.05)
    print2("\033[J")
    print2("\033[100A")
