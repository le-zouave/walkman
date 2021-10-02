"""
This script allows for manipulation of the album_list file
"""

import numpy as np
import re

library = open("./album_list.txt", "r")

# unpack lines

album = []
artist = []
genre = []

for i,l in enumerate(library):
    if l[0] == "#": continue


    ll = re.split('\t+', l)

    album.append(ll[0].strip('"\n'))
    artist.append(ll[1].strip('"\n'))
    genre.append((ll[2]).strip('"\n'))

print("halte")