# Withwait

A simple utility to ensure that a sleep operation always completes, even if an
exception happens in code within the with statement.

## Usage

```py
from withwait import wait

# Start a 2 second wait timer
with wait(2):
    # These operations happen while the timer is run
    print("Started timer")
    # Even if an error is raised, the timer will always be allowed to complete
    # before the withwait block is closed
    raise Exception("Yikes")

# The exception isn't actually caught so this code won't run
print("This never prints")
```
