'''
    Prototype file for testing screen shot speed.
'''
from mss import mss

from pixel_average import down_scale_resolution

HD = (128, 720)
FHD = (1920, 1080)
QHD = (2560, 1440)
UHD = (3840, 2160)

NUMBER_OF_LEDS = 4
PIXELS_PER_SEGMENT = 0

def get_pixels_per_segment(number_of_pixels, number_of_leds):
    segments = []
    start = 0
    end = 0

    segment_size = number_of_pixels / (number_of_leds + 1)

    # for 
    segments.append( (start,) )
    

if __name__ == '__main__':
    

    with mss() as sct:
        monitor = sct.monitors[0]
        get_pixels_per_segment(monitor['width'], NUMBER_OF_LEDS)
        pixels = sct.grab(monitor).pixels
        down_scaled = down_scale_resolution(screen_matrix=pixels, down_scaled_resolution=5)
        print('done')
