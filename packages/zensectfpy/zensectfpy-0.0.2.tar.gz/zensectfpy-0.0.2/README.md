# simple-vuln-py-lib
Python library that contains a snarky storage secret.

## Installation
`pip install --upgrade zensectfpy`

## Public-facing functionality
```py
from zensectfpy.rickroll import print_rickroll # Importing the `print_rickroll` function

num_iterations:int = 10 # Number of times the Rickroll lyrics are to be printed

print_rickroll(num_iterations) # Calling the function
```

## Zense CTF Challenge
There is some private functionality hidden in this repo. Access it, and you shall find the flag!