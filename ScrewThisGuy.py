import time
import sys
import RPi.GPIO as GPIO
import json 
import threading
import traceback

from menu import MenuItem, Menu, Back, MenuContext, MenuDelegate
from drinks import drink_list, drink_options

sys.path.insert(0, r'C:\Users\s1657228\source\repos\Gmail API')

GPIO.setmode(GPIO.BCM)


FLOW_RATE = 60.0/100.0

class Bartender(MenuDelegate): 
	
    def __init__(self):
        self.possibleDrinks = drink_list
        self.running = False
        # load the pump configuration from file
        self.pump_configuration = Bartender.readPumpConfiguration()
        for pump in self.pump_configuration.keys():
            #Finding the pin numbers per pump and seting up the GPIO
            GPIO.setup(self.pump_configuration[pump]["pin"], GPIO.OUT, initial=GPIO.HIGH)

        print("Done initializing")

    @staticmethod
    def readPumpConfiguration():
        return json.load(open('pump_config.json'))


    def clean(self):
        waitTime = 20
        pumpThreads = []

        # cancel any button presses while the drink is being made
        # self.stopInterrupts()
        self.running = True

        for pump in self.pump_configuration.keys():
            pump_t = threading.Thread(target=self.pour, args=(self.pump_configuration[pump]["pin"], waitTime))
            pumpThreads.append(pump_t)

        # start the pump threads
        for thread in pumpThreads:
            thread.start()

        # start the progress bar
        self.progressBar(waitTime)

        # wait for threads to finish
        for thread in pumpThreads:
            thread.join()

        # show the main menu
        self.menuContext.showMenu()

        # sleep for a couple seconds to make sure the interrupts don't get triggered
        time.sleep(2)

        # reenable interrupts
        # self.startInterrupts()
        self.running = False

    def displayMenuItem(self, menuItem):
        print(menuItem.name)

    def pour(self, pin, waitTime):
        GPIO.output(pin, GPIO.LOW)
        time.sleep(waitTime)
        GPIO.output(pin, GPIO.HIGH)


    def makeDrink(self, ingredients):
        # cancel any button presses while the drink is being made
        # self.stopInterrupts()
        #The drink parameter is a string that represents the name of the drink being made 
        #ingredients is a dictionary where the keys are strings representing the names of the ingredients and the values are floats representing the amount of each ingredient required to make the drink.
        #For example a drink like half and half 50% coffee and 50% milk
        #Would have ingredients 'Coffee' : 50, 'Milk' :50

        self.running = True

        maxTime = 0
        pumpThreads = []
        #This loop goes though each ingredient 
        for ing in ingredients.keys():
            #This loop looks though each pump in the pump config to see if there is one that matches the label of the ingredent we are attempting to add
            for pump in self.pump_configuration.keys():
                if ing == self.pump_configuration[pump]["value"]:
                    #This finds how long we should pour the drink for
                    waitTime = ingredients[ing] * FLOW_RATE
                    if (waitTime > maxTime):
                        maxTime = waitTime
                    #Bro really worte it weird for no reason but args is just the paramenters for the pour method
                    #So this opens a thread which goes to the pour method for each ingredient
                    #THE THREADS HAVENT STARTED YET
                    #Then it adds them to a list of not started threads 
                    pump_t = threading.Thread(target=self.pour, args=(self.pump_configuration[pump]["pin"], waitTime))
                    pumpThreads.append(pump_t)

        # start the pump threads
        for thread in pumpThreads:
            thread.start()

        # start the progress bar
        #I dont think we need this
        #self.progressBar(maxTime)

        # wait for threads to finish
        for thread in pumpThreads:
            thread.join()

        # show the main menu
        #Don't think we need this either 
        #self.menuContext.showMenu()


        # sleep for a couple seconds to make sure the interrupts don't get triggered
        time.sleep(2);

        # reenable interrupts
        # self.startInterrupts()
        self.running = False


    #WTF does this code do
    def run(self):
        self.startInterrupts()
        # main loop
        try:  
            while True:
                time.sleep(0.1)
            
        except KeyboardInterrupt:  
            GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
        GPIO.cleanup()           # clean up GPIO on normal exit 

        traceback.print_exc()

    def ChooseDrink(self, drinkName):
        for drink in self.possibleDrinks:
            if drink['name'] == drinkName:
                return drink['ingredients']



bartender = Bartender()

#My best guess as to what making a drink would look like

SomethingNasty = {'Milk' : 1, 'Water' : 1}
bartender.makeDrink(SomethingNasty)

#If that works test this
#test2 = bartender.ChooseDrink('Hot Water')
#bartender.makeDrink(test2)

#If that works we just need to connect up the text API

#If we want to clean the pumps attach water to them and run this code
#bartender.clean()

#WTF Does this code do?
#bartender.buildMenu(drink_list, drink_options)
#bartender.run()



