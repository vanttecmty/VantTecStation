from bluetooth import *
import os
import io
from PIL import Image
from array import array
####
## 29.153847
## -81.015432
###
socketBusy = False

'''
    Receive images when you send the takeoff message to the drone
'''
def beginMission():

    action = "takeoff"
    actionBytes = action.encode('utf-8')
    client_sock.send(actionBytes)
    
    #Se bloquea el socket para evitar mensajes inesperados
    global socketBusy
    socketBusy = True

    data = bytes()
    moreImages = True
    photoCount = 1
    while(moreImages):
        try:
            image_bytes = bytes()
            moreBytes = True
            print("waiting for image..")
            while(moreBytes):
                
                data = client_sock.recv(1024)
                if len(data) == 0:
                    break
                
                if(data == bytes("endimage", 'utf-8')):
                    moreBytes = False
                    print("Recieved image..")
                    break

                if(data == bytes("finish", 'utf-8')):
                    print("Finished getting images...")
                    moreBytes = False
                    moreImages = False
                    break

                print(data)
                
                image_bytes += data
            
            if not moreImages:
                break

            image = Image.open(io.BytesIO(image_bytes))
            image.save("DronePhoto" + str(photoCount) + ".jpg")
            #image.show()
            
            photoCount += 1
        except IOError as e:
            print("I/O error")
            pass
    
    waitForLand()

'''

'''
def waitForLand():
    print("Waiting for the drone to land...")
    try:
        data = client_sock.recv(1024)
        if len(data) == 0:
            print("nada")
            
        land = data.decode("utf-8")

        if(land == "land"):
            print("Drone landed...")
            #Volver a mover barco
        
    except IOError as e:
        print("I/O error")
        pass
    
    # Se libera el socket
    global socketBusy
    socketBusy = False


'''
    Recibe las coordenadas gps del dron, se debe bloquear la 
    llamada a esta función cuando el dron está volando porque
    se podrían recibir datos no esperados
'''
def getDroneGPS():
    if(not socketBusy):
        try:
            data = client_sock.recv(1024)
            if len(data) == 0:
                print("nada")
                
            coords = data.decode("utf-8")

            # Las coordenadas se mandan en la forma "22.1342,-100.21341"
            latitude, longitude = coords.split(",")

            # Si se necesitan en tipo float, descomentar lo siguiente
            latitudeFloat = float(latitude)
            longitudeFloat = float(longitude)

            print("Latitude: " + latitude)
            print("Longitude: " + longitude)

            ## Hacer algo con las coordenadas
            #
            #
            #
        except IOError as e:
            print("I/O error")
            pass



server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "fa87c0d0-afac-11de-8a39-0800200c9a66"

advertise_service( server_sock, "SampleServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ], 
#                   protocols = [ OBEX_UUID ] 
                    )

print("Waiting for connection on RFCOMM channel %d" % port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from ", client_info)


# Flujo: Primero se manda un mensaje con el string "takeoff"
#       para después pasar a un estado donde espera las imagenes
#       - Cuando termina de recibir una, el android manda el string "endimage"
#       - Cuando termina de recibir todas las imagenes, el android manda el string "finish"
#       - Cuando el dron aterriza, android manda el string "land"
#       - Cuando los dos booleanos estan en true, el barco puede continuar

moreMessages = True
'''
while(moreMessages):
    action = input()
    actionBytes = action.encode('utf-8')
    client_sock.send(actionBytes)
    if action == "takeoff":
        print("Mission in progress...")
        beginMission()
    elif action == "gps":
        print("Getting drone coords...")
        getDroneGPS()
    elif action == "emergency":
        print("Returning to home...")
    elif action == "bye":
        moreMessages = False
        print("Bye")

'''

def disconnect():
    ## Al final se desconecta y se deben cerrar los sockets.
    print("disconnected")

    client_sock.close()
    server_sock.close()
    print("all done")