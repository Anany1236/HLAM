import os
import json

def read_json(file_path):
    # """Read and parse a JSON file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def process_json(data):
    # """Process the JSON data according to the given instructions."""
    messages = data['messages']
    # Find the identify_device function call
    for message in messages:
        if 'tool_calls' in message:
            functions = message['tool_calls'][0]['function']
            for i, tool_call in enumerate(functions):
                if tool_call['name'] == 'identify_device':
                    identify_device_arguments = tool_call['arguments']
                    # Copy the arguments to the next function call
                    if i + 1 < len(functions):
                        next_function = functions[i + 1]
                        if next_function['name'] == 'identify_device':
                            print("[ISSUE] PLEASE RESOLVE TEST CASE")
                        next_function_args = next_function['arguments']
                        next_function['arguments'] = merge_arguments(identify_device_arguments, next_function_args)
            
            for i, tool_call in enumerate(functions):
                if tool_call['name'] == 'identify_device':
                    del functions[i]
    return data

def merge_arguments(data1, data2):

    # Create a copy of data1 to avoid modifying the original
    merged_data = data1.copy()

    # Update merged_data with the values from data2
    for key, value in data2.items():
        if isinstance(value, str) and value.startswith('#'):
            continue
        merged_data[key] = value

    return merged_data

def process_directory(directory_path):
    # """Process all JSON files in the specified directory."""
    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            file_path = os.path.join(directory_path, filename)
            data = read_json(file_path)
            # try:
            processed_data = process_json(data)
            # except:
            #     print(f"[ERROR] Could not process {filename}. Skipping...")
            with open(file_path, 'w') as file:
                json.dump(processed_data, file, indent=4)
            print(f"Processed and saved changes to {file_path}")

# Specify the directory containing the JSON files
directory_path = 'D:\\SamsungSept2024\\Test_Templates_1'
process_directory(directory_path)