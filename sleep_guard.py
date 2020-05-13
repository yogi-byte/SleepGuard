import uuid
from firebase import firebase
firebase = firebase.FirebaseApplication('https://sleepguard-e6844.firebaseio.com/', None)
import paho.mqtt.client as mqtt
import datetime
Motion=0

mqtt_user_name = 'oauth2-user'
mqtt_password = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJuczAxIiwic3ViIjoiMjcyNSIsInVzZXJfbmFtZSI6Im5la2lhcnkwN0BnbWFpbC5jb20iLCJzY29wZSI6WyJyZWFkLW9ubHkiXSwiZXhwIjoxNjI4NTEyNDYzLCJhdXRob3JpdGllcyI6WyJST0xFX1VTRVIiXSwianRpIjoiZGYxN2MxMDctMTZjOS00NWY4LTlhYzktNDc1Mjg5YzIyMjk1IiwiY2xpZW50X2lkIjoicmVhZC1vbmx5In0.OwNii06ZqQTvwtx30Mb8NXXSIKpn-ynGQeS8-65iiwc'  # copy and paste here external access token from your account
user_id = '2725' # copy and paste here your user id
device_id = 'TO136-02021000010010F5' # copy and paste here your device id


#norm_datasource_topic = '/v1/users/{user_id}/in/devices/{device_id}/datasources/MOTION'.format(user_id=user_id,device_id=device_id)
humidity_temperature = '/v1/users/{user_id}/in/devices/{device_id}/datasources/HUMIDITY_TEMPERATURE'.format(user_id=user_id,device_id=device_id)

ca_cert_path = 'cacert.crt'

def on_connect(client, userdata, flags, rc):
    print('Sleep Guard'.format(code=rc))

def on_message(client, userdata, msg):
               #x=int(str(msg.payload).split(',')[7].split(':')[1])
               print('Msg received from topic={topic}\n{content}'.format(topic=msg.topic, content=str(msg.payload)))
               Motion+=1
               today = datetime.datetime.today()
               current_day= today.weekday()
               print("day"+current_day)
               firebase.put(current_time,"current_day")
               firebase.put('count',"Motion",Motion)

def main():
    client = mqtt.Client(client_id=str(uuid.uuid4()), transport='websockets')
    
    client.on_connect = on_connect
    client.on_message = on_message

    client.tls_set(ca_certs="/home/pi/Downloads/cacert.crt")#setting location for the certificate
    client.username_pw_set(mqtt_user_name, mqtt_password)

    client.connect('ns01-wss.brainium.com', 443)

    
    #client.subscribe(norm_datasource_topic)
    client.subscribe(humidity_temperature)

    client.loop_forever()

if __name__ == "__main__":
    main()



    


    
