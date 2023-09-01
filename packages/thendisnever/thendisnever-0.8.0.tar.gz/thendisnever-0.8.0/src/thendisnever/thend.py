"""Main file for the thendisnever package."""
# Import dependencies
import os  # To disable HF parallelism warning message
import subprocess  # To rerun the script

# Disable HF parallelism warning message
os.environ["TOKENIZERS_PARALLELISM"] = "false"


# Main function
def isnever(
    model_name=None,  # Model to generate text with, more info here: https://huggingface.co/docs/transformers/model_doc/auto#transformers.AutoModelForCausalLM
    prompt=None,  # Initial prompt for model, length (in tokens) < the model's max_length
    max_memory_ratio=None,  # % of past tokens to remember, 0 < x < 1
):
    cmd_string = f"python src/thendisnever/utils.py"
    if model_name:
        cmd_string += f" --model_name {model_name}"
    if prompt:
        cmd_string += f" --prompt {prompt}"
    if max_memory_ratio:
        cmd_string += f" --max_memory_ratio {max_memory_ratio}"

    while True:
        try:
            subprocess.run(cmd_string, shell=True)
        except (KeyboardInterrupt, Exception):
            print("\n\nExiting...")
            break
        except TimeoutError:  # Script needs to be rerun
            continue


# Run the function for testing
isnever()