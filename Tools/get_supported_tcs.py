import os
import glob
import json


data_path = r'D:\\Project\\git\\BHP\\contextual-ml\\bhp-vii-en-US\\Validation\\CoSMIC_CXMDE'
supported_actions_file = r"D:\\Project\\git\\BHP\\contextual-ml\\test\\SupportedActions.txt"
out_dir = r"D:\\Project\\git\\BHP\\contextual-ml\\test\\tcs"

with open(supported_actions_file, 'r') as fin:
    supported_actions = list(map(lambda s: s.strip(), fin.readlines()))
    print(supported_actions)


input_files = glob.glob(os.path.join(
        data_path, '**/*.json'), recursive=True)
for input_file in input_files:
    with open(input_file, 'r') as json_file:
        json_data = json.load(json_file)
        if json_data['voiceIntent'] in supported_actions:
            _, file_name = os.path.split(input_file)
            print(file_name)
            with open(os.path.join(out_dir, file_name), 'w') as fout:
                json.dump(json_data, fout, indent=4, ensure_ascii=False)