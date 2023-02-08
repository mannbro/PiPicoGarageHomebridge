import time
from machine import Pin

class GarageDoor():

    #CONSTANTS
    STATE_OPEN=0
    STATE_CLOSED=1
    STATE_OPENING=2
    STATE_CLOSING=3
    STATE_STOPPED=4

    ACTION_NONE=0
    ACTION_OPEN=1
    ACTION_CLOSE=2

    #If the door hasn’t reached one of the end states after a certain amount of
    #time after an action is started, assume that it is obstructed or stuck
    #Adjust if your door is faster or slower
    OBSTRUCTED_THRESHOLD_SECONDS=40

    #GLOBALS
    lastSensedState=STATE_OPEN
    action=ACTION_NONE
    lastActionTime=time.time()

    def __init__(self, openSensorPin, closedSensorPin, triggerPin, pulseLength, obstructedThresholdSeconds):
        self.trigger = Pin(triggerPin, Pin.OUT)
        self.openSensor=Pin(openSensorPin, Pin.IN, Pin.PULL_UP)
        self.closedSensor=Pin(closedSensorPin, Pin.IN, Pin.PULL_UP)
        self.pulseLength=pulseLength
        self.obstructedThresholdSeconds=obstructedThresholdSeconds
        
        self.updateLastSensedState()
        self.updateAction()



    #Update lastSensedState based on current sensor state if either of the sensors
    #are currently sensing 
    def updateLastSensedState(self):
        if(self.isDoorClosed()):
            self.lastSensedState=self.STATE_CLOSED
        elif(self.isDoorOpen()):
            self.lastSensedState=self.STATE_OPEN

    #Reflect action based on what has happened
    def updateAction(self):
        #If either of the end states (open or closed) are reached,
        #set action to none
        if(self.isDoorOpen() or self.isDoorClosed()):
            self.action=self.ACTION_NONE
            
        #If the door is not in one of the end states, but no action is triggered,
        #assume that the door is being manually operated in the opposite direction
        #of the previous end state
        elif(self.action==self.ACTION_NONE):
            self.lastActionTime=time.time()
            if(self.lastSensedState==self.STATE_OPEN):
                self.action=self.ACTION_CLOSE
            else:
                self.action=self.ACTION_OPEN

    #Is the door open?
    def isDoorOpen(self):
        return self.openSensor.value()==0

    #Is the door closed?
    def isDoorClosed(self):
        return self.closedSensor.value()==0

    #If there is an action (not ACTION_NONE) and it’s been running for a longer
    #time than expected, assume the door is obstructed/stuck
    def isObstructed(self):
        print("isObstructed Debug  ", time.time(), self.lastActionTime, self.obstructedThresholdSeconds)
        
        return self.action!=self.ACTION_NONE and time.time()>self.lastActionTime+self.obstructedThresholdSeconds

    #Return the target state based on current action and sensor states
    def getTargetState(self):
        if(self.action==self.ACTION_OPEN or self.isDoorOpen()):
            return self.STATE_OPEN
        else:
            return self.STATE_CLOSED

    #Return the current state based on current action and sensor states
    def getCurrentState(self):
        if(self.isObstructed()):
            return self.STATE_STOPPED
        elif(self.isDoorOpen()):
            return self.STATE_OPEN
        elif(self.isDoorClosed()):
            return self.STATE_CLOSED
        elif(self.action==self.ACTION_OPEN):
            return self.STATE_OPENING
        elif(self.action==self.ACTION_CLOSE):
            return self.STATE_CLOSING

    #Return all relevant states as a JSON
    def getStates(self):
        #Reflect LastSensoreState
        self.updateLastSensedState()
        #Reflect Action
        self.updateAction()

        #Return JSON
        retval='{"success": true'+', "currentState": '+str(self.getCurrentState())+', "targetState": '+str(self.getTargetState())+', "obstructed": '+str(self.isObstructed()).lower()+', "debugInfo": {'+'"action": '+str(self.action)+', "isDoorOpen": '+str(self.isDoorOpen()).lower()+', "isDoorClosed": '+str(self.isDoorClosed()).lower()+', "secondsSinceLastAction": '+str(time.time()-self.lastActionTime)+'}'+'}'
        return retval

    def start(self, newAction):
        #Don’t start the door if it’s already moving (and not obstructed),
        #don't open if it's already open,
        #don't close if it's already closed
        if((self.isDoorOpen() and newAction==self.ACTION_CLOSE) or (self.isDoorClosed() and newAction==self.ACTION_OPEN) or self.isObstructed()):
            self.action=newAction
            self.lastActionTime=time.time()

            self.trigger.value(1)
            time.sleep_ms(self.pulseLength)
            self.trigger.value(0)
            
        return self.getStates()
