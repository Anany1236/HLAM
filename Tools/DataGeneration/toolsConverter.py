import json
import copy
import os

# # Input JSON string
# input_json = """{
#     "name": "application_search",
#     "description": "This function is used to search something on an application on TV device.",
#     "parameters": [
#         {
#             "name": "location",
#             "type": "string",
#             "description": "The location where the device which needs to be used to launch the application is located.",
#             "optional": true
#         },
#         {
#             "name": "room",
#             "type": "string",
#             "description": "The room where the air conditioner is located. e.g. living room, bedroom, bathroom, etc.",
#             "optional": true
#         },
#         {
#             "name": "device",
#             "type": "string",
#             "description": "The name or type of the device to be used to launch an application.",
#             "optional": true
#         },
#         {
#             "name": "app_name",
#             "type": "string",
#             "description": "The application which the user intends to launch on the device.",
#             "optional": true
#         },
#         {
#             "name": "search_term",
#             "type": "string",
#             "description": "The search query for the application.",
#             "optional": false
#         }
#     ],
#     "depends_upon": [
#         "application_launch",
#         "identify_search_term"
#     ],
#     "output": []
# }"""


def convert_tools_to_required_format(input_json):
    # Parse the input JSON string into a dictionary
    input_dict = input_json

    # Create a new dictionary to store the converted JSON data
    output_dict = {
        "type": "function",
        "function": [
            {
                "name": input_dict["name"],
                "description": input_dict["description"],
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        ]
    }
    # Extract the parameters from the input dictionary and format them accordingly
    for param in input_dict["parameters"]:
        param_info = {
            "type": param["type"],
            "description": param["description"]
        }
        output_dict["function"][0]["parameters"]["properties"][param["name"]] = param_info
        
        if not param["optional"]:
            output_dict["function"][0]["parameters"]["required"].append(param["name"])

    return output_dict

# # Convert the new dictionary back to a JSON string
# output_json = json.dumps(output_dict, indent=4)

# print(output_json)

def read_json_files(directory):
    # Step 3: Get a list of all files in the directory
    files = os.listdir(directory)
    
    # Step 4: Initialize an empty list to store JSON objects
    json_objects = []
    
    # Step 5: Iterate through each file in the list
    for file_name in files:
        # Check if the file ends with .json
        if file_name.endswith('.json'):
            # Open the file and load its contents
            with open(os.path.join(directory, file_name), 'r') as file:
                json_obj = json.load(file)
                try:
                    json_obj = convert_tools_to_required_format(json_obj)
                    if os.path.exists(os.path.join(directory, "mistral_actions")) == False:
                        os.makedirs(os.path.join(directory, "mistral_actions"))
                    save_json_object(json_obj, os.path.join(directory, "mistral_actions"), file_name)
                except Exception as e:
                    print(e)
                    print("[ERROR]: Could not create mistral action for action: ", file_name)

def save_json_object(json_obj, directory, filename):
    # Step 3: Construct the full file path
    file_path = os.path.join(directory, filename)
    
    # Step 4: Write the JSON object to the file
    with open(file_path, 'w') as file:
        print("Saving JSON object to:", file_path)
        json.dump(json_obj, file, indent=4)

# Execute the main function
if __name__ == '__main__':
    INPUT_DIR = "griham_actions"
    directory_path = os.path.join(os.path.dirname(__file__), '..', '..')
    INPUT_DIR = os.path.join(directory_path, INPUT_DIR)
    read_json_files(INPUT_DIR)