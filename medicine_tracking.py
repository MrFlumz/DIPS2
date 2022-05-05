# Connect to MQTT server
# Subscribe to the topic "medicine_tracking"
# Publish a message to the topic "medicine_tracking"

import paho.mqtt.client as mqtt
import time

import telegram_send

simulation_time = time.strftime("%H:%M")


def get_current_time(): # Makes it possible to change the time in the program for testing
    #return simulation_time # Using a simulated time instead of real time
    return time.strftime("%H:%M") # Use this line to use real time

def send_telegram_message(message):
    telegram_send.send(messages=[message])

Medicide_taken_today = False
time_medicine_taken = '00:00'
# Function to check if it's morning
def is_morning():
    hour = int(time.strftime("%H"))
    if hour >= 7 and hour < 14: #______________________________________________________________________________________________________________________________
        return True
    else:
        return False


# Connect to MQTT server
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc)) 
    # Result code meaning: 0 - Connection successful, 1 - Connection refused (unacceptable protocol version), 2 - Connection refused (identifier rejected), 3 - Connection refused (broker unavailable), 4 - Connection refused (bad user name or password)
    client.subscribe("Daily Medicin Reminder")
    
    
# Receive message from MQTT server
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    # Check if the message is "medicine_taken"
    Medicide_taken_today = True
    # Set time when medicine was taken
    global time_medicine_taken
    time_medicine_taken = time.strftime("%H:%M")
    print("Medicine taken at: " + time_medicine_taken)
    send_telegram_message("Medicine taken at: " + time_medicine_taken + " - Fast started")
        
    
# Calculate minutes between 2 times
def time_difference(time1, time2):
    time1 = time1.split(":")
    time2 = time2.split(":")
    time1 = int(time1[0])*60 + int(time1[1])
    time2 = int(time2[0])*60 + int(time2[1])
    
    return abs(time1 - time2)

    
    
# Test connection
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("81.211.22.123", 1883, 60)
#Subscribe to the topic "hej"
client.subscribe("Daily Medicin Reminder")
# Publish a message to the topic "hej"
#client.publish("hej", "hejsan")

user_notified = False
Medicide_taken_today = False

while True:
    # If it's 8 in the morning and the medicine has not been taken, send a message to the user
    if is_morning() and not Medicide_taken_today and not user_notified:
        send_telegram_message("You have to take your medicine now!")
        user_notified = True
        print("User reminded to take medicine")
    
    # At midnight, reset the variable
    if time.strftime("%H:%M") == "00:00":
        Medicide_taken_today = False
        User_notified = False
        print("Reset time and user notified")
        time.sleep(60)
        
    # if an hour has passed since the medicine was taken, send a message to the user
    if time_difference(time_medicine_taken, time.strftime("%H:%M")) == 1:
        send_telegram_message("Your fast is over!")
        print("User notified of fast over")
        time.sleep(60)
    
    # sleep to avoid 100% CPU usage
    time.sleep(2)
    
    # Check if the medicine has been taken
    client.loop() # Check for messages
    print("Checking for messages")
    print(time_difference(time_medicine_taken, time.strftime("%H:%M")))
    



    
    
