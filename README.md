# GrihamAI_Core
Griham AI Core Engine work repository

## List of Contents
- [Model](#model)
- [Dataset](#dataset)
- [Preprocessing](#preprocessing)
- [Training](#training)
- [Evaluation](#evaluation)
- [Tools](#tools)

## Model
This section contains the base models for Mistral, LLaMA, and Phi, along with our fine-tuned models created.

## Dataset
This section includes the training and test data used for fine-tuning the training and testing of the large language models (LLMs).

## Preprocessing
This section includes Jupyter notebooks or Python scripts used for preprocessing the training data to the required base model format.

## Training
This section includes Jupyter notebooks or Python scripts used for fine-tuning our LLM.

## Evaluation
This section includes Jupyter notebooks or Python scripts used for evaluating the performance of our fine-tuned models.

## Tools
This section includes additional scripts used for the project usage.

## Data Validator

### Overview

`datavalidator.py`  script designed to validate generated action parameters against actual action names and their respective mandatory parameters. It checks for any missing mandatory parameters and prints the errors along with the associated file name.

### Usage

To use `datavalidator the following command:

```bash
python datavalidator.py --validate_data <path_to_input_directory>
```

#### Example
```sh
python .\dataValidator.py --validate_data .\Corrected_Data\
```

### Error Output
```
[ERROR]:[FILE LOAD] Could not load JSON file: some_file.json. Error: [error details]
[ERROR]:[ACTION FILE MISSING] Could not find action file for function: some_function. Error: [error details]
[ERROR]:[INVALID ARGUMENT] Argument name is not valid for this function.
Details: [FileName] some_file.json - [ArgName] some_arg - [function] some_function
[ERROR]:[MISSING MANDATORY PARAM] Missing mandatory argument(s).
Details: [FileName] some_file.json - [Mandatory_param] {'param1', 'param2'} - [function] some_function
Total Errors: [number]
Invalid Arguments Errors: [number]
Mandatory param missing Errors: [number]
Load Test Case File Errors: [number]
Load Action File Errors: [number]
```

### Output

This is the example showing the output of the script.

```
[ERROR]: Argument name is not valid for this function.
Details: [FileName] .\Corrected_Data\dishWashing_cancel_0.json  - [ArgName]  predefinedCompartment  - [function]  dishWashing_cancel

[ERROR]: Missing mandatory argument(s).
Details: [FileName] .\Corrected_Data\colorControl_setValue_0.json  - [Mandatory_param]  {'color'}  - [function]  colorControl_setValue

Total Errors: 2
Invalid Arguments Errors: 0
Mandatory param missing Errors: 0
Load Test Case File Errors: 0
Load Action File Errors: 0
```
