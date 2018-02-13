'''Test server module'''
import time # allow wait time in python
import requests # allow http requests in python
from datetime import datetime

OBSTACLE_AVOIDANCE = "http://127.0.0.1:5000/obstacleAvoidance/courseA/VNTEC"
AUTOMATED_DOCKING = "http://127.0.0.1:5000/automatedDocking/courseA/VNTEC"
HEARTBEAT = "http://localhost:5000/heartbeat/courseA/VNTEC"


def obstacleAvoidance():
    '''Funcion de prueba de obstacle avoidance'''
    boatInfo = {"challenge": "OBSTACLE AVOIDANCE"}

    for i in range(5):
        r = requests.get(OBSTACLE_AVOIDANCE)
        print("------------- Heading to: ----------------")
        data = r.json()
        print(data)
        for x in range(2):
            boatInfo["timestamp"] = datetime.now()
            print("------------- HEARTBEAT --------------")
            print(boatInfo)
            print("--------------------------------------")
            r = requests.post(url=HEARTBEAT, data=boatInfo)
            time.sleep(0.4)
        time.sleep(2)
    print("------------ Finished obstacle avoidance -----------")


def automatedDocking():
    '''Funcion de prueba de automated docking'''
    boatInfo = {"challenge": "AUTOMATED DOCKING"}
    r = requests.get(AUTOMATED_DOCKING)
    data = r.json()
    print(data)

    for i in range(10):
        boatInfo["timestamp"] = datetime.now()
        print("------------- HEARTBEAT --------------")
        print(boatInfo)
        time.sleep(0.5)
    print("--------- Finished automated docking -------------")



def test():
    '''Funcion para probar el server'''
    print("---------- Starting test ------------")
    time.sleep(2)
    print("---------- Engines ready ----------")
    time.sleep(1)
    print("---------- Heading to obstacle avoidance ----------")
    obstacleAvoidance()
    print("---------- Heading to automated docking ----------")
    automatedDocking()

test()
