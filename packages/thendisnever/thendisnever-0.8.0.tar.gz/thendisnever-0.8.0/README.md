# The End is Never

A package to make an LLM talk with itself forever.

```python
from thendisnever.thend import isnever
isnever()
```

## `is_never()` parameters

- `model_name`: The model to generate text with.
  - [This](https://huggingface.co/togethercomputer/RedPajama-INCITE-Base-3B-v1) is the default model.
  - This must be a model compatible with [AutoModelForCausalLM](https://huggingface.co/docs/transformers/model_doc/auto#transformers.AutoModelForCausalLM).
- `prompt`: The initial prompt for the model.
  - [This](https://thestanleyparable.fandom.com/wiki/The_End_Is_Never...) is the inspiration for the default prompt.
  - The length in tokens of the prompt must be less than the model's `max_length` (see [here](https://huggingface.co/docs/transformers/pad_truncation#padding-and-truncation) for more info).
- `max_memory_ratio`: The % of past tokens to remember.
  - This must be a real number between 0 and 1, since empty prompts are not allowed (0) and the prompt must be smaller than the model's context window for generation to work (1).

## Notes

- When running `isnever()` for the first time, it will download the model and tokenizer from HuggingFace. This will take a while, but it only needs to be done once.
- If you want to use the CPU (not recommended because it's slow, but it works), make sure you have [PyTorch for CPU](https://pytorch.org/get-started/locally/) installed before installing this package.

## Contributing

1. Install [poetry](https://python-poetry.org/docs/#installation) if necessary.
1. Create and setup the poetry environment:

    ```bash
    git clone https://github.com/andrewhinh/thendisnever.git
    cd thendisnever
    poetry shell
    poetry install
    ```

1. Make your changes, remembering to update in `pyproject.toml` the `version` in the `tool.poetry` section and the `tool.poetry.dependencies` section as necessary.

1. Build the package:

    ```bash
    poetry build
    ```

1. Test the package in a fresh environment:

    ```bash
    pip install dist/thendisnever-<version>.tar.gz
    ```

1. Once confirmed to work, make a PR from a feature branch to main on GitHub.
1. Once PR is merged, [email me](mailto:ajhinh@gmail.com) to be added as a collaborator on PyPI.
1. Once added as a collaborator, publish the package to `PyPI`:
  
      ```bash
      poetry config pypi-token.pypi <your-token> # Get your token from https://pypi.org/manage/account/token/
      poetry publish
      ```
