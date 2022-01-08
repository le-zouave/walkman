"""
This script allows for manipulation of the album_list_OG file.
Code compatible for \t width of 4

note: lib_charles.txt is NEVER to be opened in write mode (generally) !

TODO: add every vinyl in collection to spotify library and to lib_charles.txt
"""
import numpy as np
import math
import re

# column widths
alb_w = 4*21
art_w = 4*11
gen_w = 4*9
vin_w = 0


with open("libraries/lib_charles.txt", "r") as library:
    # unpack lines
    album = []
    artist = []
    genre = []
    vinyl = []

    for i,l in enumerate(library):
        if l[0] == "#": continue

        ll = re.split('\t+', l)

        alb = ll[0].strip('"\n')
        art = ll[1].strip('"\n')
        gen = ll[2].strip('"\n')
        vin = ll[3].strip('"\n')

        print(f"{alb}" + int(math.ceil((alb_w - len(alb)) / 4)) * '\t'
              + f"{art}" + int(math.ceil((art_w - len(art)) / 4)) * '\t'
              + f"{gen}" + int(math.ceil((gen_w - len(gen)) // 4)) * '\t')

        album.append(alb)
        artist.append(art)
        genre.append(gen)
        vinyl.append(vin)


# vinyl = ['no']*len(album)

with open("libraries/album_list_cobaye.txt", "w") as library:
    library.write("# Spotify albums in alphabetical order (by title)\n")
    library.write("# album" + int(math.ceil((alb_w - len('# album')) / 4)) * '\t'
                  + "artist" + int(math.ceil((art_w - len('artist')) / 4)) * '\t'
                  + "genre" + int(math.ceil((gen_w - len('genre')) / 4)) * '\t'
                  + "vinyl" + int(math.ceil((vin_w - len('vinyl')) / 4)) * '\t'+'\n')

    for i in range(len(album)):
        alb = album[i]
        art = artist[i]
        gen = genre[i]
        vin = vinyl[i]

        library.write(f"{alb}" + int(math.ceil((alb_w - len(alb)) / 4)) * '\t'
                      + f"{art}" + int(math.ceil((art_w - len(art)) / 4)) * '\t'
                      + f"{gen}" + int(math.ceil((gen_w - len(gen)) / 4)) * '\t'
                      + f"{vin}" + int(math.ceil((vin_w - len(vin)) / 4)) * '\t'+'\n')

# # produce csv album_list
# data = {"album": album,
#         "artist": artist,
#         "genre": genre,
#         "vinyl": vinyl}

# df = pd.DataFrame(data, dtype=str)

# for name in df.columns:
#     df.rename(columns={name: f"{name:60}"}, inplace=True)

# df.style.set_properties(**{'text-align': 'left'}).set_table_styles([ dict(selector='th', props=[('text-align', 'left')] ) ])

# print(df.to_string(justify="left"))
#
# df.to_csv(path_or_buf="./libraries/album_list.csv", sep='\t')

# print("halte")