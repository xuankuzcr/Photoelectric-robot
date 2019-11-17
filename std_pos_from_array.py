std_pos = {
    "1": [177, 35],
    "2": [167, 59],
    "3": [167, 39],
    "4": [177, 49]
}
std_pos_put = {
    "red0":     [155, 127], ##
    "green0":   [151, 71],  ##
    "blue0":    [205, 145], ##
    "white0":   [187, 81],  
    "black0":   [175, 63],  #
    "red1":     [171, 63],  #
    "green1":   [175, 101], #
    "blue1":    [171, 59],  #
    "white1":   [193, 63]   #
}

print "Reading standard position from array"
for key, [x, y] in std_pos.items():
    print "std_pos[%s] x_origin: %d, y_origin: %d" % (key, x, y)
for key, [x, y] in std_pos_put.items():
    print "std_pos_put[%s]\t x_origin: %d, y_origin: %d" % (key, x, y)
