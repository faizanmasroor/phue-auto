"""If you have never connected to your Philips Hue Bridge via Python file, you will need to press the bridge's link
button and run this script within 30 seconds to successfully make a connection."""

from dotenv import load_dotenv
import phue
import os
import subprocess

load_dotenv()

# ping responses that indicate a failure when pinging the IP address of the user's device
ping_fails = ['Request timed out.\n', 'Destination host unreachable.\n']

# retrieves the Philips Hue Bridge and user device IP addresses from .env
BRIDGE_ADDR = os.getenv('BRIDGE_ADDR')
DEVICE_ADDR = os.getenv('DEVICE_ADDR')


def main():
    """Connection is established with Philips Hue Bridge and a list containing all phue.Light objects is created.
    Continuous ping beings and the bridge and lights are passed as arguments."""

    use_all_lights = input("Will all lights be controlled? [y/n] ") == "y"
    b = phue.Bridge(BRIDGE_ADDR)
    target_lights = b.get_light_objects(mode='id') if use_all_lights else "Game Room Lamp"
    ping(b, target_lights)


def ping(bridge, lights):
    """Creates a command terminal subprocess that continuously pings the user device with a time out of 500
    milliseconds. Most recent response is read and the lights turn off the ping status matches with an element from
    ping_fails. Conversely, the lights turn on if the response is 'Reply from [DEVICE_ADDR]'."""

    process = subprocess.Popen(f'ping -t -w 500 {DEVICE_ADDR}', stdout=subprocess.PIPE, text=True)
    while True:
        echo = process.stdout.readline()
        is_fail = echo in ping_fails
        is_success = f'Reply from {DEVICE_ADDR}' in echo
        if is_success:
            bridge.set_light(lights, 'on', True)
        if is_fail:
            bridge.set_light(lights, 'on', False)


if __name__ == '__main__':
    main()
