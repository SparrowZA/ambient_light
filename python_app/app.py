from serial import Serial
from mss import mss

# A modified version of mss that brings down screenshot time from 0.6-0.7s
# to 0.07s.
# from mss_custom import mss
from time import perf_counter

from slip_utils import encodeToSlip
from pixel_average import down_scale_resolution

# Hardcoded COMM port
PORT = '/dev/tty.usbmodem14201'
BAUD_RATE = 115200

# The number of LEDs to use.
# For an optimal effect, make sure the number of LEDs 
# equals the length of the monitor
NUMBER_OF_LEDS = 19


def rgb_pixel_tuple_to_byte_array(pixel_arr):
    ''' Takes the 2D pixel tuple from the mss library
    eg ((...),(...),(...),...)
    and converts it into a serialised list of byte values.
    '''
    byte_arr = []
    for pixel in pixel_arr:
        for value in pixel:
            byte_arr.append(int(value).to_bytes(2, 'big')[-1])
    return byte_arr

def send_pixel(serial_obj, pixel_byte):
    ''' Writes the serialised byte array to the 
    serial object.
    '''
    # print('pixel: ' + str(pixel_byte))
    serial_obj.write(bytes(pixel_byte))

if __name__ == '__main__':
    with mss() as sct:        
        with Serial(PORT, BAUD_RATE, timeout=1) as ser:
            while True:
                pixel_byte = None
                # Hardcoded which monitor to use
                monitor = sct.monitors[0]

                start_time = perf_counter()
                # The screen shot function. grab() returns an object
                # of which pixels is an attribute. It comes back as
                # 2D tuple matrix with each individual RGB byte value
                # its own tuple.
                pixels = sct.grab(monitor).pixels
                finish_time = perf_counter()
                print('pixels calc time:' + str(finish_time - start_time))
                
                # My own code for downscaling the pixel matrix.
                down_scaled = down_scale_resolution(screen_matrix=pixels, down_scaled_resolution=NUMBER_OF_LEDS)

                # Serialise the tuple matrix into a byte array
                pixel_byte = rgb_pixel_tuple_to_byte_array(down_scaled)

                # Endcode the byte array using the Serial
                # Line Interface Protocol (SLIP) to ensure
                # the END byte is escaped in the packet data. 
                pixel_byte = encodeToSlip(pixel_byte)
                
                send_pixel(serial_obj=ser, pixel_byte=pixel_byte)
                ser.flush()
                

    # with mss() as sct:
    #     for count in range(10):
    #         start_time = perf_counter()

    #         monitor = sct.monitors[0]
    #         pixels = sct.grab(monitor).pixels
    #         down_scaled = down_scale_resolution(screen_matrix=pixels, down_scaled_resolution=5)
            
    #         finish_time = perf_counter()
    #         print('time: ' + str(finish_time - start_time))
