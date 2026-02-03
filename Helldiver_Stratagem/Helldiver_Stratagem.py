#To Display the windows, and create an output
import tkinter as tk
from PIL import ImageTk,Image
import cairosvg
from pynput.keyboard import Controller, Key
from io import BytesIO
import os
import tkinter.font as tkFont


'''
installs:
pip install pillow pynput cairosvg
'''

#Global Variables
ctrl_held=False
images_hidden = False
keyboard=Controller()
    
#Garbage collection
image_refs = []
image_items = []
svgToImgArr = []

CurrentStratagem = ""
    #Stores the input from the left clicks from the program
StratagemStorage = []

#Stores all the stratagems in the game and the code
StratagemsDict = {
    
# Orbital Stratagems - Tested and working

"Orbital Precision Strike"             :     ["Right", "Right", "Up"], 
"Orbital Gatling Barrage"              :     ["Right", "Down", "Left", "Up", "Up"], 
"Orbital Airburst Strike"              :     ["Right", "Right", "Right"], 
"Orbital Napalm Barrage"               :     ["Right", "Right", "Down", "Left", "Right", "Up"], 
"Oribtal 120MM HE Barrage"             :     ["Right", "Right", "Down", "Left", "Right", "Down"], 
"Orbital Walking Barrage"              :     ["Right", "Down", "Right", "Down", "Right", "Down"],
"Orbital 380MM HE Barrage"             :     ["Right", "Down", "Up", "Up", "Left", "Down", "Down"],
"Orbital Railcannon Strike"            :     ["Right", "Up", "Down", "Down", "Right"],
"Orbital Laser"                        :     ["Right", "Down", "Up", "Right", "Down"], 
"Orbital EMS Strike"                   :     ["Right", "Right", "Left", "Down"], 
"Orbital Gas Strike"                   :     ["Right", "Right", "Down", "Right"],
"Orbital Smoke Strike"                 :     ["Right", "Right", "Down", "Up"],

# Eagle Stratagems - All tested and working

"Eagle 500KG Bomb"                     :     ["Up", "Right", "Down", "Down", "Down"],
"Eagle Strafing Run"                   :     ["Up", "Right", "Right"],
"Eagle 110MM Rocket Pods"              :     ["Up", "Right", "Up", "Left"],
"Eagle Airstrike"                      :     ["Up", "Right", "Down", "Right"],
"Eagle Cluster Bomb"                   :     ["Up", "Right", "Down", "Down", "Right"],
"Eagle Napalm Airstrike"               :     ["Up", "Right", "Down", "Up"],
"Eagle Smoke Strike"                   :     ["Up", "Right", "Up", "Down"],

# Supply Stratagems - Tested and working

"CQC-1 One True Flag"                  :     ["Down", "Left", "Right", "Right", "Up"],
"MG-43 Machine Gun"                    :     ["Down", "Left", "Down", "Up", "Right"], 
"M-105 Stalwart"                       :     ["Down", "Left", "Down", "Up", "Up", "Left"],
"MG-206 Machine Gun"                   :     ["Down", "Left", "Up", "Down", "Down"],
"RS-422 Railgun"                       :     ["Down", "Right", "Down", "Up", "Left", "Right"],
"APW-1 Anti-Materiel Rifle"            :     ["Down", "Left", "Right", "Up", "Down"],
"GL-21 Grenade Launcher"               :     ["Down", "Left", "Up", "Left", "Down"],
"GL-52 De-Escalator"                   :     ["Left", "Right", "Up", "Left", "Right"],
"TX-14 Sterlizer"                      :     ["Down", "Left", "Up", "Down", "Left"],
"FLAM-40 Flamethrower"                 :     ["Down", "Left", "Up", "Down", "Up"],
"LAS-98 Laser Cannon"                  :     ["Down", "Left", "Down", "Up", "Left"], 
"LAS-99 Quasar Cannon"                 :     ["Down", "Down", "Up", "Left", "Right"],
"ARC-3 Arc Thrower"                    :     ["Down", "Right", "Down", "Up", "Left", "Left"], 
"MLS-4X Commando"                      :     ["Down", "Left", "Up", "Down", "Right"],
"EAT-17 Expendable Anti-Tank"          :     ["Down", "Down", "Left", "Up", "Right"],
"AC-8 Autocannon"                      :     ["Down", "Left", "Down", "Up", "Up", "Right"],
"RLL-77 Airburst Rocket Launcher"      :     ["Down", "Up", "Up", "Left", "Right"], 
"FAF-14 Spear Launcher"                :     ["Down", "Down", "Up", "Down", "Down"],
"StA-X3 W.A.S.P. Launcher"             :     ["Down", "Down", "Up", "Down", "Right"],
"GR-8 Recoilless Rifle"                :     ["Down", "Left", "Right", "Right", "Left"],
"PLAS-45 Epoch"                        :     ["Down", "Left", "Up", "Left", "Right"], 
"EAT-700 Expendable Napalm"            :     ["Down", "Down", "Left", "Up", "Left"], 
"S-11 Speargun"                        :     ["Down", "Right", "Down", "Left", "Up", "Right"], 
"MS-11 Solo Silo"                      :     ["Down", "Up", "Right", "Down", "Down"], 
    "B╱MD C4 Pack"                     :     ["Down","Right","Up","Up","Right","Up"],

# Supply Backpacks - Tested and working
"SH-32 Shield Generator Pack"          :     ["Down", "Up", "Left", "Right", "Left", "Right"],
"SH-51 Directional Shield Backpack"    :     ["Down", "Up", "Left", "Right", "Up", "Up"],
"SH-20 Ballistic Shield Backpack"      :     ["Down", "Left", "Down", "Down", "Up", "Left"],
"LIFT-860 Hover Pack"                  :     ["Down", "Up", "Up", "Down", "Left", "Right"],
"B-1 Supply Pack"                      :     ["Down", "Left", "Down", "Up", "Up", "Down"],
"B-100 Portable Hellbomb"              :     ["Down", "Right", "Up", "Up", "Up"], 
"LIFT-850 Jump Pack"                   :     ["Down", "Up", "Up", "Down", "Up"],
"AX╱AR-23 “Guard Dog”"                 :     ["Down", "Up", "Left", "Up", "Right", "Down"], 
"AX╱LAS-5 “Guard Dog” Rover"           :     ["Down", "Up", "Left", "Up", "Right", "Right"], 
"AX╱TX-13 “Guard Dog” Dog Breath"      :     ["Down", "Up", "Left", "Up", "Right", "Up"],
"AX╱ARC-3 “Guard Dog” K-9"             :     ["Down", "Up", "Left", "Up", "Right", "Left"],
"LIFT-182 Warp Pack"                   :     ["Down", "Left", "Right", "Down", "Left", "Right"], 

# Vehicles - Tested and working

"M-102 Fast Recon Vehicle"             :     ["Left", "Down", "Right", "Down", "Right", "Down", "Up"],
"EXO-49 Emancipator Exosuit"           :     ["Left", "Down", "Right", "Up", "Left", "Down", "Up"],
"EXO-45 Patriot Exosuit"               :     ["Left", "Down", "Right", "Up", "Left", "Down", "Down"],

# Defensive Stratagems - Tested and working

"A╱G-16 Gatling Sentry"                :     ["Down", "Up", "Right", "Left"],
"A╱MG-43 Machine Gun Sentry"           :     ["Down", "Up", "Right", "Right", "Up"],
"E╱FLAM-40 Flame Sentry"               :     ["Down", "Up", "Right", "Down", "Up", "Up"], 
"A╱MLS-4X Rocket Sentry"               :     ["Down", "Up", "Right", "Right", "Left"], 
"A╱AC-8 Autocannon Sentry"             :     ["Down", "Up", "Right", "Up", "Left", "Up"],
"A╱M-23 EMS Mortar Sentry"             :     ["Down", "Up", "Right", "Down", "Right"], 
"A╱M-12 Mortar Sentry"                 :     ["Down", "Up", "Right", "Right", "Down"],
"FX-12 Shield Generator Relay"         :     ["Down", "Down", "Left", "Right", "Left", "Right"], 
"E╱GL-21 Grenadier Battlement"         :     ["Down", "Right", "Down", "Left", "Right"],
"E╱AT-12 Anti-Tank Emplacement"        :     ["Down", "Up", "Left", "Right", "Right", "Right"],
"E╱MG-101 HMG Emplacement"             :     ["Down", "Up", "Left", "Right", "Right", "Left"], 
"A╱ARC-3 Tesla Tower"                  :     ["Down", "Up", "Right", "Up", "Left", "Right"], 
"A╱LAS-98 Laser Sentry"                :     ["Down", "Up", "Right", "Down", "Up", "Right"], 


"MD-17 Anti-Tank Mines"                :     ["Down", "Left", "Up", "Up"], 
"MD-8 Gas Mines"                       :     ["Down", "Left", "Left", "Right"], 
"MD-6 Anti-Personnel Minefield"        :     ["Down", "Left", "Up", "Right"], 
"MD-I4 Incendiary Mines"               :     ["Down", "Left", "Left", "Down"], 

# Mission Stratagems - Tested and working

"Reinforcements"                            :     ["Up", "Down", "Right", "Left", "Up"], 
"SOS Beacon"                           :     ["Up", "Down", "Right", "Up"], 
"Resupply"                             :     ["Down", "Down", "Up", "Right"], 
"NUX-223 Hellbomb"                     :     ["Down", "Up", "Left", "Down", "Up", "Right", "Down", "Up"], 
"SSSD Delivery"                        :     ["Down", "Down", "Down", "Up", "Up"],
"Seismic Probe"                        :     ["Up", "Up", "Left", "Right", "Down", "Down"],
"Upload Data"                          :     ["Left", "Right", "Up", "Up", "Up"], 
"Eagle Rearm"                          :     ["Up", "Up", "Left", "Up", "Right"], 
"SEAF Artillery"                       :     ["Right", "Up", "Up", "Down"], 
"Super Earth Flag"                     :     ["Down", "Up", "Down", "Up"],
"Hive Breaker Drill"                   :     ["Left", "Up", "Down", "Right", "Down", "Down"],
"Super Destoryer"                      :     ["Up","Up","Down","Down","Left","Right","Left","Right"]
}

def main():
    

    #Functions
        #Used to delete Arrow, skull etc when displaying Stratagem Icon
    def hide_all_images():
        global images_hidden
        for item in image_items:
            canvas.delete(item)
        image_items.clear()
        image_refs.clear()
        images_hidden = True

        #Used to delete Stratagem Icon, textm and recreate all the Arrows, the skull and X
    def show_all_images():
        global images_hidden
        for item in svgToImgArr:
            canvas.delete(item)
        canvas.delete("Text")
        svgToImgArr.clear()
        #To see what these paramaters mean, scroll down to the bottom.
        ArrowCreation("Up_Arrow",    0.4,   0.5,   1,     0.4)
        ArrowCreation("Down_Arrow",  0.4,   0.5,   1,    1.6)
        ArrowCreation("Right_Arrow", 0.4,   0.5, 1.4,      1)
        ArrowCreation("Left_Arrow", 0.4,   0.5,  0.6,      1)
        ArrowCreation("Skull",0.3,0.4,1.75,1.75)
        ArrowCreation("X", 0.3, 0.4, .125, .125) 
        images_hidden = False

    
    def on_left_click(event):
        global ctrl_held, images_hidden, CurrentStratagem
    
        #Skull
        if abs(event.x - (width / 2 * 1.75)) <= (width / 2 * 0.3) / 2 * 1.5 and \
           abs(event.y - (height / 2 * 1.75)) <= (height / 2 * 0.4) / 2 * 1.5 and images_hidden == False:
            print("Clicked the Skull")
            StratagemStorage.clear()
            if not ctrl_held:
                #keyboard.press(Key.ctrl_l)
                ctrl_held=True
            else:
                #keyboard.release(Key.ctrl_l)
                ctrl_held=False

        #Up Arrow
        if abs(event.x - (width / 2 * 1)) <= (width / 2 * 0.4) / 2 * 1.5 and \
           abs(event.y - (height / 2 * 0.4)) <= (height / 2 * 0.5) / 2 * 1.5 and images_hidden == False:
            print("Clicked the Up Arrow")
            StratagemStorage.append("Up")
            keyboard.tap(Key.up)

        #Down Arrow
        if abs(event.x - (width / 2 * 1)) <= (width / 2 * 0.4) / 2 * 1.5 and \
           abs(event.y - (height / 2 * 1.6)) <= (height / 2 * 0.5) / 2 * 1.5 and images_hidden == False :
            print("Clicked the Down Arrow")
            StratagemStorage.append("Down")
            keyboard.tap(Key.down)

        #Right Arrow
        if abs(event.x - (width / 2 * 1.4)) <= (width / 2 * 0.4) / 2 * 1.5 and \
           abs(event.y - (height / 2 * 1)) <= (height / 2 * 0.5) / 2 * 1.5 and images_hidden == False:
            print("Clicked the Right Arrow")
            StratagemStorage.append("Right")
            keyboard.tap(Key.right)

        #Left Arrow
        if abs(event.x - (width / 2 * 0.6)) <= (width / 2 * 0.4) / 2 * 1.5 and \
           abs(event.y - (height / 2 * 1)) <= (height / 2 * 0.5) / 2 * 1.5 and images_hidden == False:
            print("Clicked the Left Arrow")
            StratagemStorage.append("Left")
            keyboard.tap(Key.left)
        #X
        if abs(event.x - (width / 2 * 0.125)) <= (width / 2 * 0.3) / 2 * 1 and \
           abs(event.y - (height / 2 * 0.125)) <= (height / 2 * 0.4) / 2 * 1 and images_hidden == False: 
                exit()
        show_all_images()

                #This is where the stratagem gets called, and determined
                #Checks to see if the provided combination matches with the dictonary
                #If it does, hide everything, display the icon and name of stratagem, then hide when the user clicks
                #or after 2 seconds
        for Stratagem, Code in StratagemsDict.items():
            if Code == StratagemStorage:
                print(f"{Stratagem} requested. Good hunting Helldiver.")
                #keyboard.release(Key.ctrl_l)
                CurrentStratagem = Stratagem
                hide_all_images()
                createStratagem()
                StratagemStorage.clear()
                root.after(2000, show_all_images)


        #params are Name, SizeWidthMult, SizeHeightMut, WidthLocationMult,HeightLocationMult

    def ArrowCreation(Name,sizeWithMult,sizeHeightMult,WidthLocationMult,HeightLocationMult):
            ArrowImage= Image.open(f'{os.getcwd()}/Arrows/{Name}.png')
            resized_image = ArrowImage.resize((int((width/2) *sizeWithMult), int((height/2) * sizeHeightMult)))
            newimg = ImageTk.PhotoImage(resized_image)
            img = canvas.create_image(int(width/2*WidthLocationMult),int(height/2*HeightLocationMult),image = newimg)
            image_refs.append(newimg)
            image_items.append(img)
            #print(image_refs) (Debug)

    #Changes the size of the images depending on the size of the window
    def on_resize(event):
        global CurrentStratagem
        nonlocal width, height
        width = root.winfo_width()
        height = root.winfo_height()
        if images_hidden == False:
            for item in image_items:
                canvas.delete(item)
            image_items.clear()
            image_refs.clear()
            #To see what these paramaters mean, scroll down to the bottom.
            ArrowCreation("Up_Arrow",    0.4,   0.5,   1,     0.4)
            ArrowCreation("Down_Arrow",  0.4,   0.5,   1,    1.6)
            ArrowCreation("Right_Arrow", 0.4,   0.5, 1.4,      1)
            ArrowCreation("Left_Arrow", 0.4,   0.5,  0.6,      1)
            ArrowCreation("Skull",0.3,0.4,1.75,1.75)
            ArrowCreation("X", 0.3, 0.4, .125, .125)
        else: 
            for item in svgToImgArr:
             canvas.delete(item)
            svgToImgArr.clear()
            canvas.delete("Text")
            createStratagem()

    #Displays the stratagem icon

    def createStratagem(): 
        nonlocal width, height
        width = root.winfo_width()
        height = root.winfo_height()
        StratagemName = CurrentStratagem
        #Get SVG File
        filename = f"{os.getcwd()}/Filtered/" + StratagemName + ".svg"

        #Get memory, then save converted SVG image to memory
        pngBytes = BytesIO()
        SVGimg = cairosvg.svg2png(url=filename, write_to=pngBytes, output_width= width /2, output_height = height/2)

        #Opens the image from memory, and converts it to RGBA (For transparency)
        img = Image.open(pngBytes).convert("RGBA")

        #variable for garb collection, then opens the image
        tk_img = ImageTk.PhotoImage(img)
        canvas.create_image(int(width/2),int(height/2.4),image = tk_img)
        #Text
        customSize= tkFont.Font(size = int((height - width) * 1/15) )
        canvas.create_text(width/2, (height/1.4), text=f'{StratagemName} requested. Good hunting Helldiver.', fill='white', tag="Text", font=customSize)
        print(width)  #x
        print(height) #y
        
        #Garb collection 
        svgToImgArr.append(tk_img)
        
    #Root Window
    root = tk.Tk()
    root.title("Helldiver Stratagem")

    #Goes fullscreen (Remove the comment to go full screen)
    #root.attributes('-fullscreen', True)

    #Chooses Resolution
    root.geometry('800x600')
        
    #updates with and height of root
    root.update_idletasks()
        
    #Root width and height
    width = root.winfo_width()
    height=root.winfo_height()
    
    #Detect presses
    root.bind("<Button-1>", on_left_click)
    root.bind("<Configure>", on_resize)

    #Canvas
    canvas = tk.Canvas(root,  bg='black')
    canvas.pack(fill=tk.BOTH, expand=True)


        
    #Arrow creation
    #params are Name, SizeWidthMult, SizeHeightMut, WidthLocationMult,HeightLocationMult
    #SizeWidthMult:      higher number makes Arrow wider.
    #SizeHeightmult:     higher number making Arrow taller
    #WidthLocationMult:  higher numbers makes move to the right
    #HeightLocationMult: higher value moves it the arrow down
            
    ArrowCreation("Up_Arrow",    0.4,   0.5,   1,     0.4)

    ArrowCreation("Down_Arrow",  0.4,   0.5,   1,    1.6)
    
    ArrowCreation("Right_Arrow", 0.4,   0.5, 1.4,      1)
    
    ArrowCreation("Left_Arrow", 0.4,   0.5,  0.6,      1)

    ArrowCreation("Skull",0.4,0.5,1.75,1.75)
    
    ArrowCreation("X", 0.3, 0.4, .125, .125)



    root.mainloop()

main()


