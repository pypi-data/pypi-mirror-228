"""Utility functions for the thendisnever package."""
# Import the necessary classes
import argparse  # To parse command line arguments
import os  # To disable HF parallelism warning message
import sys  # To parse command line arguments
from transformers import (
    AutoTokenizer,  # Converts text to tokens and vice versa for the model to understand
    AutoModelForCausalLM,  # Model that generates text from a prompt
    TextStreamer,  # Print what the model generates as it generates it
)
import torch  # PyTorch is used to run the model on the GPU


# Define the default arguments
DEFAULT_MODEL_NAME = "togethercomputer/RedPajama-INCITE-Base-3B-v1"  # https://huggingface.co/togethercomputer/RedPajama-INCITE-Base-3B-v1
DEFAULT_PROMPT = "THE END IS NEVER THE END IS NEVER "  # https://thestanleyparable.fandom.com/wiki/The_End_Is_Never...
DEFAULT_MAX_MEMORY_RATIO = 0.5  # Randomly chosen
DEVICE = (
    "cuda:0" if torch.cuda.is_available() else "cpu"
)  # Use GPU if available, otherwise use CPU


# Define helper functions
def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model_name",
        type=str,
        default=DEFAULT_MODEL_NAME,
        help="Model to generate text with, more info here: https://huggingface.co/docs/transformers/model_doc/auto#transformers.AutoModelForCausalLM",
    )
    parser.add_argument(
        "--prompt",
        type=str,
        default=DEFAULT_PROMPT,
        help="Initial prompt for model, length (in tokens) < the model's max_length",
    )
    parser.add_argument(
        "--max_memory_ratio",
        type=float,
        default=DEFAULT_MAX_MEMORY_RATIO,
        help="% of past tokens to remember, 0 < x < 1",
    )
    return parser.parse_args(args)


def clear_terminal():
    if os.name == "nt":  # For Windows
        _ = os.system("cls")
    else:  # For macOS and Linux
        _ = os.system("clear")


def download_model(model_name):
    print("Downloading model...")
    model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    streamer = TextStreamer(
        tokenizer,
        skip_prompt=True,  # To skip the prompt when streaming since it's already printed
    )
    print("Model downloaded")
    return model, tokenizer, streamer


# Define the main function
def run(model_name=None, prompt=None, max_memory_ratio=None):
    # Check if the arguments are valid
    if not model_name:  # If no model is provided
        print("Using default model")
        model_name = DEFAULT_MODEL_NAME  # Use the default model
    if type(model_name) != str:  # If model_name is not a string
        print("Model name must be a string, using default model")
        model_name = DEFAULT_MODEL_NAME  # Use the default model
    if not prompt:
        print("Using default prompt")
        prompt = DEFAULT_PROMPT
    if type(prompt) != str:
        print("Prompt must be a string, using default prompt")
        prompt = DEFAULT_PROMPT
    if not max_memory_ratio:
        print("Using default max memory ratio")
        max_memory_ratio = DEFAULT_MAX_MEMORY_RATIO
    if (
        (type(max_memory_ratio) != float and type(max_memory_ratio) != int)
        or max_memory_ratio <= 0
        or max_memory_ratio >= 1
    ):  # If max_memory_ratio is not a valid value
        print(
            "Max memory ratio must be a float or integer between 0 and 1, using default max memory ratio"
        )
        max_memory_ratio = DEFAULT_MAX_MEMORY_RATIO

    # Download model and tokenizer
    try:
        model, tokenizer, streamer = download_model(model_name)
    except Exception as e:
        if "valid" in str(e):  # To catch invalid model names
            print("Invalid model name, using default model\n\n")
            model_name = DEFAULT_MODEL_NAME  # To use the default model
            model, tokenizer, streamer = download_model(model_name)
        elif "timed out" in str(e):  # To catch connection errors
            raise TimeoutError(
                "Connection error, retrying...\n\n"
            ) from None  # from None suppresses multiple tracebacks
        else:  # To catch other errors
            raise Exception(e) from None

    # Generate text
    try:  # In case anything goes wrong
        # Define model.generate() arguments
        max_length = (
            model.config.max_length
        )  # Context window size of the model (in tokens)
        max_memory = (
            int(max_length * max_memory_ratio) + 1
        )  # Add 1 to avoid empty prompt

        # Check if prompt is too long
        inputs = tokenizer(
            [prompt],  # Wrap prompt as a list since inputs are usually a batch
            return_tensors="pt",  # Return PyTorch tensors
        )["input_ids"][
            0
        ]  # Text to tokens, index 0 because only one prompt
        if len(inputs) >= max_length:  # If the prompt is too long
            inputs = inputs[
                : max_length - 1
            ]  # Only keep the first max_length - 1 tokens (- 1 to give model space to generate)
            prompt = tokenizer.decode(
                inputs,
                skip_special_tokens=True,  # To remove special tokens like <eos>
            )  # Tokens to text
        clear_terminal()
        print(prompt)  # Print the initial prompt since it's not streamed

        # Set up the conversation loop, where the response is used as the next prompt
        while True:
            inputs = tokenizer(
                [prompt],  # Wrap prompt as a list since inputs are usually a batch
                return_tensors="pt",
            )
            inputs, model = inputs.to(DEVICE), model.to(
                DEVICE
            )  # Move to GPU if available
            response = model.generate(
                **inputs,  # Unpack dictionary into keyword arguments
                streamer=streamer,
                max_length=max_length,
                num_return_sequences=1,  # To return only one response
                pad_token_id=tokenizer.eos_token_id,  # To remove warning message in console
                do_sample=True,
                num_beams=1,
            )  # Arguments from here: https://huggingface.co/docs/transformers/generation_strategies#multinomial-sampling
            prompt = tokenizer.decode(
                response[0][-max_memory:],  # index 0 since inputs are usually a batch
                skip_special_tokens=True,
            )
    except Exception as e:
        raise Exception(e) from None


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    run(**vars(args))
