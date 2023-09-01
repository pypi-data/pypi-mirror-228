
---

# OpenUr Dashboard Commands

OpenUr is a powerful tool for controlling your UR robot. Currently, in this version, only Dashboard commands can be used for both testing and production programs. Stay tuned for upcoming updates where more features will be enabled!

## Getting Started

To use the dashboard commands from OpenUr, you can simply import the required module and proceed with your robot operations.

### Prerequisites

- Ensure you have `openur` installed.
- Know the IP address of your UR robot.

### Example Usage

Here's a quick example demonstrating the use of the Dashboard commands:

```python
from openur import Dashboard  # Enables you to use all the dashboard commands of the robot.
import time

# Example of using the Dashboard class
with Dashboard('192.168.1.11', 29999) as dc:  # replace with the IP of your robot
    dc.popup('Hello World!')
    time.sleep(2)
    dc.close_popup()
```

In the above example, we're displaying a 'Hello World!' popup on the robot's dashboard and then closing it after 2 seconds.

## Future Implementations

In the upcoming versions, we plan to enable functionalities like `RobotModel` which can be used to connect to RTDE and get robot data. Here's a sneak peek:

```python
# Initialize the connection to RTDE
with RobotModel(host="192.178.1.11") as ur:
    # Start the main logic
    print(ur.output_bit_registers())
```

This functionality is currently not available in this version but will be enabled soon!

## Updates & Support

Keep an eye on our GitHub repository for future updates and enhancements. Feel free to raise issues or contribute.

---

Remember to tailor this to fit the context and specifics of your project as needed. Adjustments may be required based on actual functionalities, project details, and nuances that might not be captured in the provided details.