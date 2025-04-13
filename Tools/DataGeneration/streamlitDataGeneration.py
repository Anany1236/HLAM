import streamlit as st
import uuid
import pyperclip
from datetime import datetime
import json

# Dictionary to store UUIDs for locations and rooms
location_room_uuids = {}
location_uuids = {}

# Function to generate a JSON object based on the input parameters
def generate_device_json(device_name, device_type, device_status, location_name, room_name):
    global location_room_uuids
    global location_uuids

    device_id = str(uuid.uuid4())
    # Check if the location and room combination already exists in the dictionary
    if (location_name, room_name) in location_room_uuids:
        location_id, room_id = location_room_uuids[(location_name, room_name)]
    else:
        if location_name in location_uuids:
            location_id = location_uuids[location_name]
        else:
            location_id = str(uuid.uuid4())
            location_uuids[location_name] = location_id
        room_id = str(uuid.uuid4())
        
        # Store the UUIDs in the dictionary
        location_room_uuids[(location_name, room_name)] = (location_id, room_id)
    
    return {
        "deviceId": device_id,
        "deviceName": device_name,
        "deviceType": device_type,
        "deviceStatus": device_status,
        "location": {
            "locationName": location_name,
            "locationId": location_id,
            "roomName": room_name,
            "roomId": room_id
        }
    }

# Streamlit App
st.title("Device JSON Generator")
st.subheader("Home Context Devices")

# Input parameters
device_names = st.text_input("Device Names (comma separated)", "Outside light, Light 1, Light 2, Kitchen light")
device_types = st.text_input("Device Types (comma separated)", "light, light, light, light")
device_statuses = st.text_input("Device Statuses (comma separated)", "off, off, off, off")
location_names = st.text_input("Location Names (comma separated)", "house, house, house, house")
room_names = st.text_input("Room Names (comma separated)", "Balcony, Living room, Living room, Kitchen")

st.subheader("Utterance")
utterance = st.text_input("Utterance", "turn on the lights")

st.subheader("Functions")

function_names = st.text_input("FunctionNames (comma separated)", "device_turnOff, device_turnOff")
function_arguments_names = st.text_input("Arguments_names (comma separated for particular function, semicolon separated between functions)", "device, room; device, room")
function_arguments_values = st.text_input("Arguments_names (comma separated for particular function, semicolon separated between functions)", "Outside light, Balcony; Light 1, Living room")


st.subheader("Expected NLG")

expected_nlg = st.text_input("Expected NLG", "I have turned on the tv")


# FINAL_OUTPUT JSON template
FINAL_OUTPUT = """
{
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant with access to the following functions to help the user. You can use the functions if needed."
        },
        {
            "role": "context",
            "content": 
            {
                "homecontext": 
                $devices_json
            }
        },
        {
            "role": "user",
            "content": $utterance
        },
        {
            "role": "assistant",
            "tool_calls": [
                {
                    "type": "function",
                    "function": $function_json
                }
            ]
        },
        {
            "role": "tool",
            "content":
            {
                "status": "success"
            }
        },
        {
            "role": "assistant",
            "content": "$expected_nlg"
        }
    ],
    "tools": []
}
"""

# Submit button
if st.button("Generate JSON"):
    # Split input parameters into lists
    device_names_list = device_names.split(",")
    device_types_list = device_types.split(",")
    device_statuses_list = device_statuses.split(",")
    location_names_list = location_names.split(",")
    room_names_list = room_names.split(",")

    # Generate JSON objects
    devices_json = []
    for i in range(len(device_names_list)):
        devices_json.append(generate_device_json(
            device_names_list[i].strip(),
            device_types_list[i].strip(),
            device_statuses_list[i].strip(),
            location_names_list[i].strip(),
            room_names_list[i].strip()
        ))

    
    # Split input parameters into lists
    function_names_list = function_names.split(",")
    function_arguments_names_list = [arg.strip().split(",") for arg in function_arguments_names.split(";")]
    function_arguments_values_list = [val.strip().split(",") for val in function_arguments_values.split(";")]
    
    # Generate JSON objects for functions
    function_json = []
    for i in range(len(function_names_list)):
        function_name = function_names_list[i]
        arguments_names = function_arguments_names_list[i]
        arguments_values = function_arguments_values_list[i]
        
        arguments_dict = {}
        for j in range(len(arguments_names)):
            argument_name = arguments_names[j].strip()
            argument_value = arguments_values[j].strip()
            
            # Replace device name with generated device ID
            if argument_name == "device":
                for device in devices_json:
                    if device["deviceName"].lower() == argument_value.lower():
                        arguments_dict[argument_name] = device["deviceId"]
                        break
                    else:
                        arguments_dict[argument_name] = argument_value
            else:
                arguments_dict[argument_name] = argument_value.lower()
        
        function_json.append({
            "name": function_name,
            "arguments": arguments_dict
        })


    FINAL_OUTPUT = FINAL_OUTPUT.replace("$devices_json", json.dumps(devices_json))
    FINAL_OUTPUT = FINAL_OUTPUT.replace("$utterance", json.dumps(utterance))
    FINAL_OUTPUT = FINAL_OUTPUT.replace("$function_json", json.dumps(function_json))
    FINAL_OUTPUT = FINAL_OUTPUT.replace("$expected_nlg", expected_nlg)

    
     # Display final output JSON
    st.write(FINAL_OUTPUT)
