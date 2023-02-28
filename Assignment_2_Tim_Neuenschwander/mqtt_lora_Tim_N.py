import time
import ttn
import json
from base64 import b64decode,b64encode
from datetime import datetime,timezone
import requests
import struct
from yawigle import client


# --- TTN VARIABLES --------------------------
app_id = "lr1110_tracking"
access_key = "ttn-account-v2.TuVkiEtlXdJhXZMuER2YGqNqIUZc0QIewLHk5avvPxs"

# --- LORA CLOUD VARIABLES --------------------------
DMS_APITOKEN = "AQEA56zNfcSA4qjgOQRvtA0JisEwAqfFOr1dOMSlPp3C4FnhNCVr"
DMS_HOST     = "https://das.loracloud.com"
DMS_PORT     = 199
DMSAPI_UPLINK_SEND = {
    'method' : 'POST',
    'url'    : f"{DMS_HOST}/api/v1/uplink/send"
}

#Constants
WIFI_PACKET_TYPE = "08"
ACC_PACKET_TYPE = "09"

# Functions
iso2ts   = lambda iso: datetime.strptime(iso, '%Y-%m-%dT%H:%M:%S.%f').replace(tzinfo=timezone.utc).timestamp()
hwid2eui = lambda hwid: '-'.join(hwid[2*i:2*i+2] for i in range(8))

def queryWIGLE(macs,rssi_list):
    c = client('YOUR-API-NAME','YOUR-API-TOKEN')
    #TODO: Query WIGLE API

def decodeWifi(encoded):
    print(encoded)
    mac = []
    rssi = []
    #TODO: Decode and print WiFi Data
    
    import struct
    import binascii
    print("")
    print("Decoded WIFI Packet:")
    print("")
    #byte1 length
    byte1 = encoded[0:2]
    byte1 = binascii.unhexlify(byte1)
    s = struct.Struct('b')
    unpacked_data1 = s.unpack(byte1)[0]
    print("Length of the WIFI packet:", unpacked_data1)
    
    #byte2-8 rssi and mac address
    byte2infinity = encoded[2:]
    split1 = []
    split2 = []
    n = 14
    for index in range(0,len(byte2infinity), n):
        byte2 = binascii.unhexlify(byte2infinity[index : index + 2])
        s = struct.Struct('b')
        unpacked_data2 = s.unpack(byte2)[0]
        split1.append(unpacked_data2)
        split2.append(byte2infinity[index + 2  : index + n])
    
    print("RSSI per WIFI AP:", split1)
    print("MAC Address per WIFI AP:", split2)
    
    mac = split2
    rssi = split1
    
    return [mac,rssi]

def decodeAcc(encoded):
    print(encoded)
    acc = []
    #TODO: Decode and print Accelerometer Data
    import struct
    import binascii
    print("")
    print("Decoded ACC Packet:")
    print("")
    #byte1 
    byte1 = encoded[0:2]
    byte1 = binascii.unhexlify(byte1)
    s = struct.Struct('b')
    unpacked_data11 = s.unpack(byte1)[0]
    print("Length of the ACC packet (constant):", unpacked_data11)
    #byte2 
    byte2 = encoded[2:4]
    byte2 = binascii.unhexlify(byte2)
    s = struct.Struct('b')
    unpacked_data22 = s.unpack(byte2)[0]
    print("Move History of the ACC packet (constant):", unpacked_data22)
    
    #bytes1 
    bytes1 = encoded[4:8]
    #print(bytes1)
    bytes1 = binascii.unhexlify(bytes1)
    s = struct.Struct('>h')
    unpacked_data1 = s.unpack(bytes1)[0]
    print("ACC X:", unpacked_data1)
    
    #bytes2 
    bytes2 = encoded[8:12]
    #print(bytes2)
    bytes2 = binascii.unhexlify(bytes2)
    s = struct.Struct('>h')
    unpacked_data2 = s.unpack(bytes2)[0]
    print("ACC Y:", unpacked_data2)
    
    #bytes3 
    bytes3 = encoded[12:16]
    #print(bytes3)
    bytes3 = binascii.unhexlify(bytes3)
    s = struct.Struct('>h')
    unpacked_data3 = s.unpack(bytes3)[0]
    print("ACC Z:", unpacked_data3)
    
    return [acc]

def extractPacket(raw_data):
    packet_type = []
    packet_data = []

    try:
        packet_num = raw_data[0][0]
        packet_full = raw_data[0][1]
        #Extract packet data
        packet_type = packet_full[0:2]
        packet_data = packet_full[2:]
    except:
        # Empty Packet
        print("Received empty payload")

    return [packet_type, packet_data]

def uplink_callback(data, client):
    print("\nReceived uplink from ", data.dev_id)

    if(data.payload_raw is None):
        print("Empty Payload")
        return
    
    payload = b64decode(data.payload_raw).hex() 
    deveui = hwid2eui(data.hardware_serial)

    dmsmsg = json.dumps({
    deveui: {
        "fcnt":       data.counter,
        "port":       data.port,
        "payload":    payload,
        "dr":         0,
        "freq":       int(data.metadata.frequency),
        "timestamp":  iso2ts(data.metadata.time[:26])
    }
    })
    headers   = {'Authorization': DMS_APITOKEN}

    # Send raw data to LoRa Cloud
    resp = requests.post(f"{DMS_HOST}/api/v1/uplink/send",data = dmsmsg, headers=headers)

    # Receive LoRa Cloud response, and select data belong to our device's unique id
    rjs = json.loads(resp.text)
    lora_data = rjs['result'].get(deveui)['result']

    #If the lora cloud data contained WIFI or Accelerometer records, process them
    if(lora_data):
        if(lora_data['stream_records']):
            # Extract packet type and packet data
            [packet_type, packet_data] = extractPacket(lora_data['stream_records'])

            if(packet_type==WIFI_PACKET_TYPE):
                print("Received Wifi Data")
                [wifi_mac,rssi] = decodeWifi(packet_data)
                #TODO: Query WIGLE using the following function
                #queryWIGLE(wifi_mac, rssi)
            if(packet_type==ACC_PACKET_TYPE):
                print("Received Accelerometer Data")
                acc_values = decodeAcc(packet_data)

# create ttn connection
handler = ttn.HandlerClient(app_id, access_key)
# use mqtt client
mqtt_client = handler.data()
mqtt_client.set_uplink_callback(uplink_callback)
mqtt_client.connect()
time.sleep(60000)
mqtt_client.close()