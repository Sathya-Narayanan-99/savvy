level_map = [
    '                             ',
    '                             ',
    '                             ',
    ' XX    XX              XX    ',
    ' XX                          ',
    ' XXXX         XX          XX ',
    ' XXXX       XX               ',
    ' XX    X  XXXX    XX  XX     ',
    '       X  XXXX    XX  XXX    ',
    '    XXXX  XXXXXX  XX  XXXX   ',
    'XXXXXXXX  XXXXXX  XX  XXXX   '
]

tile_size = 64
screen_width = 1200

# Setting the height of the screen to be (no. of rows in level * tile size)
screen_height = len(level_map) * tile_size