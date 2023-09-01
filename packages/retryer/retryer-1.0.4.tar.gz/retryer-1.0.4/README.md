# Retryr
[![PyPI version](https://badge.fury.io/py/retryer.svg)](https://badge.fury.io/py/retryer)

A Python decorator that allows you to retry a function, and customise the action if it runs into error.

## Installation
You can install this package using pip:

```bash
pip install retryer

# Usage

from retryr import retryer

# Define your custom_action function
def custom_action(exception):

    print(f"Custom error handling: {exception}")
    # You can perform any action you want here

@retryer(max_retries=5, retry_delay=2, on_error=custom_action)
def your_function():
    # Your code here
    # If this function raises an error, it will retry up to 5 times with a 2-second delay.

if __name__ == "__main__":
    your_function()
```
## Parameters
* max_retries: The maximum number of times the function should be retried on error.
* retry_delay: The delay in seconds between retry attempts.
* on_error: A custom error handling function that will be executed when an error occurs.

## License
This project is licensed under the MIT License - see the LICENSE file for details.