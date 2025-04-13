import json
import os
import argparse

# Initialize global counters
errors = 0
mandatory_param_error = 0
load_file_error = 0
load_action_file_error = 0
invalid_argument_error = 0

def validate_data(filename):
    global errors, mandatory_param_error, load_file_error, load_action_file_error, invalid_argument_error
    
    # Load the JSON object from INPUT_DIRECTORY
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except Exception as e:
        print(f"[ERROR]:[FILE LOAD] Could not load JSON file: {filename}. Error: {e}")
        load_file_error += 1
        errors += 1
        return

    # Iterate over all messages and find the one with tool_calls
    tool_calls = next((message['tool_calls'] for message in data['messages'] if 'tool_calls' in message), None)
    if not tool_calls:
        print("No tool_calls found in the messages.")
        return

    # Iterate over tool_calls and each function inside it
    for tool_call in tool_calls:
        for function in tool_call['function']:
            functionName = function["name"]
            if functionName.startswith("identify"):
                continue
            
            file_path = os.path.join(DIR_NAME, f"{functionName}.json")
            try:
                with open(file_path, 'r') as file:
                    function_data = json.load(file)
            except Exception as e:
                errors += 1
                print(f"[ERROR]:[ACTION FILE MISSING] Could not find action file for function: {functionName}. Error: {e}")
                load_action_file_error += 1
                continue

            # Create sets for normal_param and mandatory_param
            normal_param = set()
            mandatory_param = set()

            # Iterate over the parameters and add them to the appropriate set
            for param in function_data['parameters']:
                if param['optional']:
                    normal_param.add(param['name'])
                else:
                    mandatory_param.add(param['name'])

            # Iterate over arguments inside each function
            for arg_name, arg_value in function['arguments'].items():
                if arg_name not in normal_param and arg_name not in mandatory_param:
                    print("[ERROR]:[INVALID ARGUMENT] Argument name is not valid for this function.")
                    print(f"Details: [FileName] {filename} - [ArgName] {arg_name} - [function] {functionName}")
                    invalid_argument_error += 1
                    errors += 1
                    break
                if arg_name in mandatory_param:
                    mandatory_param.discard(arg_name)
            
            if mandatory_param:
                print("[ERROR]:[MISSING MANDATORY PARAM] Missing mandatory argument(s).")
                print(f"Details: [FileName] {filename} - [Mandatory_param] {mandatory_param} - [function] {function['name']}")
                mandatory_param_error += 1
                errors += 1

def main():
    global DIR_NAME, INPUT_DIRECTORY

    DIR_NAME = "Griham_Actions"
    INPUT_DIRECTORY = "tools\\Generated_Templates"

    parser = argparse.ArgumentParser(description="Read and save files")
    parser.add_argument("--validate_data", required=False, help="Directory path whose files need to be validated")

    args = parser.parse_args()

    if args.validate_data:
        INPUT_DIRECTORY = args.validate_data

    for filename in os.listdir(INPUT_DIRECTORY):
        if filename.endswith(".json"):
            validate_data(os.path.join(INPUT_DIRECTORY, filename))

    print("Total Errors: " + str(errors))
    print("Invalid Arguments Errors: " + str(invalid_argument_error))
    print("Mandatory param missing Errors: " + str(mandatory_param_error))
    print("Load Test Case File Errors: " + str(load_file_error))
    print("Load Action File Errors: " + str(load_action_file_error))

if __name__ == "__main__":
    main()