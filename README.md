# Using in other projects

## Requirements
Python >= 3.10

## Add dependency
Add following entry in your project requirements.txt:
`mappingpylib @ git+https://github.com/hamster007Github/mappingpylib.git`

## Import library in project files
Examples:
-`import mappingpylib` or
-`import mappingpylib.scanner` or
-`from mappingpylib.scanner import DragoniteScanner`

# Used in following projects
- [hamster007Github/tg_raidbot](https://github.com/hamster007Github/tg_raidbot)
- ...

# Development

## Prepare environment
Create venv: `python3 -m venv ./`  
Note: Python >= 3.10 needed. If you have multiple python version installed, use python version specific call e.g. `python3.10 -m venv ./.venv`

## Install dependencies
`pip install .[dev]` or run script `./build_dev.sh`  
Note: script expect venv in folder '.venv'.

## Run lint, unittests and generate coverage report
`./run_tests.sh`
Note: script expect venv. For single steps please checkout script content.

# Credits
[WatWowMap/pogo-translations](https://github.com/WatWowMap/pogo-translations), where the pogo translation data are fetched from.
