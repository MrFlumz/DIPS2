from Phidget22.Phidget import *
from Phidget22.Devices.VoltageRatioInput import *
import time
import paho.mqtt.client as mqtt

#Declare any event handlers here. These will be called every time the associated event occurs.
					
tslm = 0														#Time since last message
timeBetweenMessage = 60											#Time between messages in seconds
topic = "Daily Medicin Reminder"								#Topic used in MQTT broker
def onVoltageRatioChange(self, voltageRatio):					#Detech cabinet has been opened by voltage change in motion sensor
	#VoltageRatio is a float value
	global tslm													#TimeSinceLastMessage
	if(voltageRatio > 0.5): 									#Set trigger value
		if(time.time() - tslm > timeBetweenMessage):			#If X seconds since last message, post again
			tslm = time.time()									#Note time for, to ensure X time between messages
			#print("5 seconds elapsed")
			#print("VoltageRatio [" + str(self.getChannel()) + "]: " + str(voltageRatio))
			#print("Publishing message to MQTT broker, topic: "+str(topic))
			client.publish(topic, "Cabinet has been opened")	#Send message to MQTT Broker
    

def main():
	
	#Create your Phidget channels
	#voltageRatioInput0 = VoltageRatioInput()	#Humidity Sensor
	voltageRatioInput6 = VoltageRatioInput()	#Motion Sensor
	#voltageRatioInput7 = VoltageRatioInput()	#Temperature Sensor

	#Set addressing parameters to specify which channel to open (if any)
	#voltageRatioInput0.setChannel(0)
	voltageRatioInput6.setChannel(6)
	#voltageRatioInput7.setChannel(7)

	#Assign any event handlers you need before calling open so that no events are missed.
	#voltageRatioInput0.setOnVoltageRatioChangeHandler(onVoltageRatioChange)
	voltageRatioInput6.setOnVoltageRatioChangeHandler(onVoltageRatioChange)
	#voltageRatioInput7.setOnVoltageRatioChangeHandler(onVoltageRatioChange)

	#Open your Phidgets and wait for attachment
	#voltageRatioInput0.openWaitForAttachment(5000)
	voltageRatioInput6.openWaitForAttachment(5000)
	#voltageRatioInput7.openWaitForAttachment(5000)

	#Do stuff with your Phidgets here or in your event handlers.

	try:
		input("Press Enter to Stop\n")
		
	except (Exception, KeyboardInterrupt):
		pass

	#Close your Phidgets once the program is done.
	#voltageRatioInput0.close()
	voltageRatioInput6.close()
	#voltageRatioInput7.close()

client = mqtt.Client()
client.connect("81.211.22.123", 1883, 60)	
#client.publish(topic, "Motion Sensor System now online")
main()