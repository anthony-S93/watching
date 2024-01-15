# watching
A simple command-line tool that retains the main feature of the linux `watch` command and supports scrollable output. 

## Features
`watching` adds the following features to make the `watch` command more user-friendly for certain use cases:
### Scrollable output

  Useful for situations where the output of the command cannot fit into the entire terminal window.
  The default behavior of `watch` in such cases is to keep only the characters that will fit into the screen
  while discarding the rest, which isn't ideal for all cases. `watching` circumvents that by retaining all 
  characters of the output of the command and allowing you to scroll through them. 
  
  https://github.com/anthony-S93/watching/assets/69449791/62bc2144-3174-46ae-abf4-0f2bcdd19df9

  Vim-style scrolling is supported: to scroll down, press `j`; to scroll up, press `k`  


**IMPORTANT:**

Please note that `watching` is **_not_** meant to replace the linux `watch` command. 
As such, not all features and flags of the `watch` command is implemented. For example, 
`watching` does not support the ability to take screenshots. For those use cases, it makes 
more sense to use the `watch` command. `watching` is useful for a specific use case only: 
when you need to scroll through the command output you're watching.

## Installation
Clone this repository and run the setup script. 

## Requirements
Python 3.60+

## Usage
### Command-line syntax
```text
watching [{-n | --interval} <time_seconds>] [{-h | --help}] [{-w | --no-wrap}] [{-t | --no-title}] <cmd> [args]
```
### Options
- `-n`, `--interval`

  The watch interval. Takes precedence over the `WATCH_INTERVAL` environment variable.
- `-w`, `--no-wrap`

  Turn off line wrapping. Long lines will be truncated instead of wrapped to the next line.

- `-t`, `--no-title`

  Turn off the heading normally shown at the top of the screen.

   
### Key Controls
- `j` to scroll down
- `k` to scroll up
- `q` to quit

### Environment
The behavior of `watching` is affected by the following environment variables:
- `WATCH_INTERVAL`

  Update interval, follows the same rules as the `--interval` command line option


## Examples
### Monitor the changes in a file

https://github.com/anthony-S93/watching/assets/69449791/40e28fdb-8cec-4f01-83e8-0e812b7d6ffc

### Monitor the changes in command ouput

https://github.com/anthony-S93/watching/assets/69449791/c66a7fda-6c81-43bf-afb2-79f9e9ff92da







