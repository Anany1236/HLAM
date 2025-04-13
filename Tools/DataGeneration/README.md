# Griham AI Data Generation Script

This repository contains the Python script `grihamAIDataGeneration.py` used for generating data for Griham AI. This script is designed to process Bixby 3.0 LLM fine-tuning data and create necessary data templates based on the specified Griham actions.

## Prerequisites

Before running the script, ensure you have the following:

* Bixby3-Data Repo cloned into your system. [Bixby3-Data Repo](https://github.ecodesamsung.com/bixby-platform/bixby3-data)

## Directory Structure

- **Input Directory (`--read_from`)**: Directory containing the Bixby 3.0 LLM fine-tuning data.
  - Example: `D:\Bixby3-Platform\bixby3-data\llm-finetuning-data\en-US\test\SRIB\smartthings`
- **Output Directory (`--save_to`)**: Directory where the generated data will be saved.
  - Example: `D:\GRIHAM_AI\GrihamAI_DataGen\Test_Templates`
- **Griham Actions Directory (`--griham_actions`)**: Directory containing the Griham actions to be read from.
  - Example: `D:\GRIHAM_AI\GrihamAI_Core\Griham_Actions`

## Usage

To run the script, use the following command:

```sh
python.\grihamAIDataGeneration.py --read_from D:\Bixby3-Platform\bixby3-data\llm-finetuning-data\en-US\test\SRIB\smartthings --save_to D:\GRIHAM_AI\GrihamAI_DataGen\Test_Templates --griham_actions D:\GRIHAM_AI\GrihamAI_Core\Griham_Actions
```

## Parameters Used To run the script
* --read_from: Specifies the input directory path for Bixby 3.0 LLM fine-tuning data.
* --save_to: Specifies the directory path for saving the created data.
* --griham_actions: Specifies the directory path to Griham actions to be read from.
* --deleteSaveToDirectory: Optional Parameter if you want to delete the save_to directory before running the code.
* --dontIncludeDependsUpon: Optional Parameter if you don't want to include depends upon in the data generation.

## Steps to Run the Script
**To create the data for the required actions, use the action name as per the naming convention followed in Griham Actions, with an underscore (_) in between.**
* Update the action name inside the referenceFunctionList.txt file.
* Update the action name in **referenceFunctionList.txt**.
* Run the script using the provided command.
* The generated data will be available in the specified --save_to directory.

### Things to Note

* The save_to gets created on its own. Just mention the path.
