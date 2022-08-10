# Formula Globals
# ROW_DEPTH -> The number of rows to include in the averaging.
ROW_DEPTH = 3
# OFFSET -> How far down to start taking pixels. This was needed
# due to the menu bar on top.
OFFSET = 90

def section_average(row_section: list) -> tuple:
    RED_PIXEL = 0
    GREEN_PIXEL = 1
    BLUE_PIXEL = 2
    
    red_total = 0
    green_total = 0
    blue_total = 0

    section_length = len(row_section)

    for pixel in row_section:
        red_total += pixel[RED_PIXEL]
        green_total += pixel[GREEN_PIXEL]
        blue_total += pixel[BLUE_PIXEL]

    result_pixel = (
        red_total / section_length,
        green_total / section_length,
        blue_total / section_length
    )
    return result_pixel

def average_row(row_list, down_scaled_resolution) -> list:
    section_size = int(len(row_list) / down_scaled_resolution)
    start_index = 0
    down_scaled_matrix = []

    while start_index < len(row_list):
        stop_index = start_index + section_size
        if start_index == 0:
            down_scaled_matrix.append(section_average(row_list[start_index:stop_index+30]))
        elif stop_index == len(row_list):
            down_scaled_matrix.append(section_average(row_list[start_index-30:stop_index]))
        else:
            down_scaled_matrix.append(section_average(row_list[start_index-30:stop_index+30]))
        start_index += section_size
    return down_scaled_matrix

def average_column(screen_matrix, pixel_column) -> list:
    RED_PIXEL = 0
    GREEN_PIXEL = 1
    BLUE_PIXEL = 2
    
    red_total = 0
    green_total = 0
    blue_total = 0

    section_length = len(screen_matrix)

    for row in range(section_length):
        red_total += screen_matrix[row][pixel_column][RED_PIXEL]
        green_total += screen_matrix[row][pixel_column][GREEN_PIXEL]
        blue_total += screen_matrix[row][pixel_column][BLUE_PIXEL]

    result_pixel = (
        red_total / section_length,
        green_total / section_length,
        blue_total / section_length
    )
    return result_pixel

def horizontal_pixel_average(screen_matrix, down_scaled_resolution=1):
    screen_matrix_average = []
    for pixel_row in range(OFFSET, OFFSET + ROW_DEPTH):
        screen_matrix_average.append(average_row(screen_matrix[pixel_row], down_scaled_resolution))
    return screen_matrix_average

def vertical_pixel_average(screen_matrix, down_scaled_resolution=ROW_DEPTH):
    screen_matrix_average = []
    for pixel_column in range(0, down_scaled_resolution):
        screen_matrix_average.append(average_column(screen_matrix, pixel_column))
    return screen_matrix_average

def down_scale_resolution(screen_matrix, down_scaled_resolution) -> list:
    ''' Takes a screen matrix tuple and downscales the screen's 
    top x-axis to the downscaled resolution value passed to the 
    function.

    Parameters:     
            screen_matrix:              
                type:   tuple
                description: Tuple matrx representing each RGB value for every pixel on the screen
            down_scaled_resolution:
                type:   int
                description: The number of LEDs that represent the new resolution of the ambient lights.
    
    Result:
        screen_matrix_average:  
            type: list
            description: A downscaled list of pixel colour averages.
    '''
    screen_matrix_average = horizontal_pixel_average(screen_matrix, down_scaled_resolution)
    screen_matrix_average = vertical_pixel_average(screen_matrix_average, down_scaled_resolution)

    return screen_matrix_average
