import uuid
import json

def create_json_object(deviceName, deviceType, deviceStatus, locationName, roomName):
    # Generate unique identifiers
    deviceId = str(uuid.uuid4())
    locationId = str(uuid.uuid4())
    roomId = str(uuid.uuid4())

    # Create the dictionary representing the JSON object
    json_dict = {
        "deviceId": deviceId,
        "deviceName": deviceName,
        "deviceType": deviceType,
        "deviceStatus": deviceStatus,
        "location": {
            "locationName": locationName,
            "locationId": locationId,
            "roomName": roomName,
            "roomId": roomId
        }
    }

    # Convert the dictionary to a JSON string
    json_string = json.dumps(json_dict, indent=4)

    return json_string

# Example usage
deviceName = "Speaker 1"
deviceType = "speaker"
deviceStatus = "on"
locationName = "house"
roomName = "Living room"

json_object = create_json_object(deviceName, deviceType, deviceStatus, locationName, roomName)
print(json_object)