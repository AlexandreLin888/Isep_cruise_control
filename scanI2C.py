from smbus import SMBus
import sys

def scan(bus_num, start=0x03, end=0x78):
    try:
        bus = SMBus(bus_num)
    except PermissionError:
        print("Permission error!")
        sys.exit()

    print("I2C bus       : " + str(bus_num))
    print("Start address : " + hex(start))
    print("End address   : " + hex(end) + "\n")

    for i in range(start, end):
        val = 1
        try:
            bus.read_byte(i)
        except OSError as e:
            val = e.args[0]
        finally:
            if val != 5:    # No device
                if val == 1:
                    res = "Available"
                elif val == 16:
                    res = "Busy"
                elif val == 110:
                    res = "Timeout"
                else:
                    res = "Error code: " + str(val)
                print(hex(i) + " -> " + res)

if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        print("Specify desired I2C bus!")
        print("Usage : i2c-scanner.py <bus>")
        sys.exit()
    scan(int(args[1]))