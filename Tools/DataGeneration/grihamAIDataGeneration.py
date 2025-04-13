import os, json
import copy
import argparse
import re

# Reading the function-intentMap json file for 
# New SmartThings Bixby3.0 Intent mapping to older intent's
with open('function-intentMap.json', 'r') as file:
    json_data = file.read()

# Loading the json file to a dict
newIntentToOldIntent = json.loads(json_data)

oldIntentToNewIntent = {}
for key, value in newIntentToOldIntent.items():
    oldIntentToNewIntent[value] = key

for key, value in newIntentToOldIntent.items():
    print(key, ":", value)
    break

tool={
    "type": "function",
    "function": []
}

def read_json_files_recursively(directory, referenceFunctionList, saveToDirectory):
    functionList = copy.deepcopy(referenceFunctionList)
    for root, _, files in os.walk(directory):
        for file in files:
            # print("fileName:", file)
            file_name = file.replace(".json", "")
            if file.endswith('.json') and file_name.endswith('Root'):
                
                main_function = file.split('_')[3]
                try:
                    main_function = newIntentToOldIntent[main_function]
                except:
                    continue
                if main_function in referenceFunctionList:
                    if(main_function in functionList):
                        functionList.remove(main_function) # In order to check the test cases which don't have created data
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        json_data = json.load(f)
                        try:
                            json_data = iterate_over_turns_and_functions(json_data)
                            # pretty_json = json.dumps(json_data, indent=4)
                            # print(pretty_json)
                            save_json_to_directory(saveToDirectory, main_function, json_data)
                        except Exception as e:
                            print("[ERROR]: Could not create test case for "+main_function+".")
                            print(e)

    print("Remaining Intents which were not able to generate : {referenceFunctionList: " + str(functionList) + "}")

def iterate_over_turns_and_functions(json_object):
        tool_calls = []
        for turn_idx, turn in enumerate(json_object['turns']):
            utterance = turn['utterance']
            expected_nlg = turn['expected_nlg']
            tool_calls.append(copy.deepcopy(tool))
            for func_idx, function in enumerate(turn['functions']):
                if(function['capsule_id']=='planner'): continue
                functionName = function['function_name']
                function_replaced = {}
                arguments = {}
                call_depends_upon = False
                if(functionName=='searchDevicesSmartThings'):
                    for parameter, parameter_value in function['function_parameters'].items():
                        if(parameter.endswith("Name")): parameter = parameter[:-4]
                        arguments[parameter] = parameter_value
                else:
                    # call the depends_upon functionality here
                    call_depends_upon=True
                    for parameter, parameter_value in function['function_parameters'].items():
                        if(parameter != 'smartThingsDeviceList'):
                            arguments[parameter] = parameter_value
                        else:
                            arguments['device'] = '#E1'
                functionName = newIntentToOldIntent[functionName] # enter function name
                
                # recursively calling the depends_upon function and adding them to the tool_calls list
                globalFunctionList = []
                if(call_depends_upon and not args.dontIncludeDependsUpon):
                    call_depends_upon = False
                    depends_upon_function_updation(grihamActions, functionName, "", globalFunctionList)
                    # print(globalFunctionList)
                    for item in globalFunctionList:
                        if item not in tool_calls[turn_idx]['function']:
                            tool_calls[turn_idx]['function'].append(item)

                function_replaced['name'] = functionName
                function_replaced['arguments'] = arguments
                tool_calls[turn_idx]['function'].append(function_replaced)
                    
        
        return updateTemplateFile(baseTemplateJsonPath, utterance, tool_calls, expected_nlg)

# would return list of functions to which this action can depend upon
def depends_upon_function_updation(action_dir, action_name, last_action_name, globalFunctionList):
    # print("action_dir: "+action_dir)
    # print("action_name: "+action_name)
    if(action_name == last_action_name):
        print("[ERROR]: File is dependent upon itself: "+action_name)
        return

    with open(f'{action_dir}/{action_name}.json', 'r') as file:
        data = json.load(file)

    # Read the depends_upon parameter from the loaded JSON
    depends_upon = data['depends_upon']

    if(len(depends_upon) == 0):
        if(action_name == "identify_device"): return
        function = {
            "name": action_name,
            "arguments": {
                "device": "#E1"
            }
        }
        globalFunctionList.append(function)

    for item in depends_upon:
        # call recursively to until we get to a mandatory action
        depends_upon_function_updation(action_dir, item, action_name, globalFunctionList)
            
                

def updateTemplateFile(input_file_name, utterance, tool_calls, expected_nlg):
    # Read the JSON content from the input file
    with open(input_file_name, 'r') as file:
        data = json.load(file)
    
    # Update the relevant parameters in the JSON content
    data['messages'][1]['content'] = trim_spaces(utterance)
    data['messages'][2]['tool_calls'] = tool_calls
    data['messages'][4]['content'] = trim_spaces(expected_nlg)

    return data

def save_json_to_directory(baseDirectory, main_function, data):
    # Check if the directory exists, if not create it
    if not os.path.exists(baseDirectory):
        os.makedirs(baseDirectory)
    
    # Create a base file name
    base_file_name = main_function
    
    # Initialize the counter
    counter = 0
    
    # Check if a file with the same name already exists
    while True:
        file_path = os.path.join(baseDirectory, f"{base_file_name}{'_0' if counter == 0 else f'_{counter}'}.json")
        if not os.path.exists(file_path):
            break
        counter += 1
    
    # Write the JSON data to the file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
        print(f"File saved at: {file_path}")

def deleteDirectory(directory_path):
    if os.path.exists(directory_path):
        # Delete all files and folders inside the directory
        for root, dirs, files in os.walk(directory_path, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                shutil.rmtree(os.path.join(root, dir))

        # Remove the directory itself
        os.rmdir(directory_path)
    else:
        print("Directory does not exist.")

def fetchReferenceFunctionList(fileName):
    with open(fileName, 'r') as file:
        function_list = []
        for line in file:
            line = line.strip()
            function_list.append(line)

    return function_list

def trim_spaces(input_string):
    # Remove leading and trailing spaces
    trimmed_string = input_string.strip()

    # Replace multiple consecutive spaces with a single space
    trimmed_string = re.sub(' +', ' ', trimmed_string)

    return trimmed_string

if __name__ == '__main__':

    # referenceFunctionList = [
    #     "device_turnOn",
    #     "device_turnOff"
    # ]

    referenceFunctionList = fetchReferenceFunctionList('referenceFunctionList.txt')

    # referenceFunctionList = [
    #     "airConditioningMode_getValue",
    #     "airConditioningMode_setValue",
    #     "application_exit",
    #     "camera_show",
    #     "channel_setByName",
    #     "channel_setByNumber",
    #     "channel_setPrevious",
    #     "cleaning_getProgress",
    #     "cleaning_pause",
    #     "cleaning_start",
    #     "cleaning_stop",
    #     "colorControl_setValue",
    #     "colorTemperature_setValue",
    #     "colorTemperature_getValue",
    #     "cooking_start",
    #     "cooking_startCourse",
    #     "device_getList",
    #     "deviceTemperatureSetting_setValue",
    #     "deviceTemperatureSetting_getValue",
    #     "deviceTemperatureSetting_increase",
    #     "deviceTemperatureSetting_decrease",
    #     "dishWashing_cancel",
    #     "dishWashing_start",
    #     "door_open",
    #     "door_close",
    #     "dressing_start",
    #     "dressing_cancel",
    #     "drying_cancel",
    #     "drying_start",
    #     "media_play",
    #     "media_pause",
    #     "media_stop",
    #     "microwave_start",
    #     "mode_setValue",
    #     "mode_getValue",
    #     "mute_turnOn",
    #     "mute_turnOff",
    #     "powerSwitch_turnOn",
    #     "powerSwitch_turnOff",
    #     "washing_cancel",
    #     "washing_start",
    #     "washing_getRemainingTime",
    #     "washing_getProgress"
    # ]

    parser = argparse.ArgumentParser(description="Read and save files")
    parser.add_argument("--read_from", required=True, help="Input Directory path for Bixby 3.0 llm finetuning data")
    parser.add_argument("--save_to", required=True, help="Directory path for saving the created data")
    parser.add_argument("--griham_actions", required=True, help="Directory Path to Griham Actions to be read from")
    parser.add_argument("--deleteSaveToDirectory", action="store_true" , default = False,  help="If needed to delete the save_to directory")
    parser.add_argument("--dontIncludeDependsUpon", action="store_true" , default = False,  help="If needed to dont include depends_upon functons in generated data")

    baseTemplateJsonPath = 'BaseTemplate.json'

    args = parser.parse_args()

    args = parser.parse_args()
    if args.read_from is None:
        print("Enter Input Directory path eg: --read_from 'D:\\directory_path'")
        exit()
    
    if args.save_to is None:
        print("Enter Output Directory path eg: --save_to 'D:\\directory_path'")
        exit()
    
    if args.griham_actions is None:
        print("Enter Input Directory path for Griham Actions eg: --griham_actions 'D:\\directory_path'")
        exit()

    grihamActions = args.griham_actions
    if(args.deleteSaveToDirectory):
        deleteDirectory(args.save_to)
    globalFunctionList = []

    read_json_files_recursively(args.read_from, referenceFunctionList, args.save_to)

