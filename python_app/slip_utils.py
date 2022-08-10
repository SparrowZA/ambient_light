SLIP_END = ord('D')
SLIP_ESC = ord('E')
SLIP_ESC_END = ord('F')
SLIP_ESC_ESC = ord('G')

def encodeToSlip(AByteArray: bytearray()) -> bytearray:
    ''' Takes a byte array and escapes END and ESC byte
    characters in the packet body and ensure the END byte 
    is appended to the end of the byte array.
    '''
    tempSLIPBuffer = bytearray()
    for i in AByteArray:
        if i == SLIP_END:
            tempSLIPBuffer.append(SLIP_ESC)
            tempSLIPBuffer.append(SLIP_ESC_END)
        elif i == SLIP_ESC:
            tempSLIPBuffer.append(SLIP_ESC)
            tempSLIPBuffer.append(SLIP_ESC_ESC)
        else:
            tempSLIPBuffer.append(i)
    tempSLIPBuffer.append(SLIP_END)
    return tempSLIPBuffer
