import numpy as np
import argparse
import re
import os
import copy
import unidecode as ud
import math

# column widths
alb_w = 4 * 21
art_w = 4 * 11
gen_w = 4 * 9
vin_w = 0


class Walkman(object):

	def __init__(self, filename, v_tog):
		self.filename = filename
		self.v_tog = v_tog

		self.filereader()

	def filereader(self):

		self.shelf = {}

		alb = []
		art = []
		gen = []
		vin = []

		with open(self.filename, "r") as file:

			for i, l in enumerate(file):
				if l[0] == "#": continue

				ll = re.split('\t+', l)

				alb.append(ll[0].strip('"\n'))
				art.append(ll[1].strip('"\n'))
				gen.append(ll[2].strip('"\n'))
				vin.append(ll[3].strip('"\n'))

		self.shelf["album"] = np.array(alb)
		self.shelf["artist"] = np.array(art)
		self.shelf["genre"] = np.array(gen)
		self.shelf["vinyl"] = np.array(vin)

		self.shelf["artist_pp"] = np.array(
			[ud.unidecode(x.lower()).replace(" ", "").replace("-", "") for x in self.shelf["artist"]])
		self.shelf["genre_pp"] = np.array(
			[ud.unidecode(x.lower()).replace(" ", "").replace("-", "") for x in self.shelf["genre"]])

		self.shelf["libsize"] = len(self.shelf["album"])

		if self.v_tog:
			self.vinyl_filter()

		self.all_artists = np.unique(self.shelf["artist"])
		self.all_genres = np.unique(self.shelf["genre"])

		if self.v_tog:
			print("-" * 80)
			print(
				f"Read a vinyl library containing {self.shelf['libsize']} albums from {self.all_artists.size} artists across {self.all_genres.size} genres")
			print("-" * 80)

		else:
			print("-" * 80)
			print(
				f"Read library containing {self.shelf['libsize']} albums from {self.all_artists.size} artists across {self.all_genres.size} genres")
			print("-" * 80)

	def rdm_select(self):

		print("Selecting random album from library")
		self.ind = np.random.choice(self.shelf["libsize"])

		self.walkman_display()

	def artist_select(self, artist):

		def find_art_ids(art):
			art_l = ud.unidecode(art.lower()).replace(" ", "").replace("-", "")
			art_ids = np.flatnonzero(np.core.defchararray.find(self.shelf["artist_pp"], art_l) != -1)

			if art_ids.size == 0:
				print(f"No artist found containing '{art}'\n")
				art = input("Enter an artist: ")
				art_ids = find_art_ids(art)

			return art_ids

		artist_ids = find_art_ids(artist)

		# ambiguity check
		amb_arr = np.unique(self.shelf["artist"][artist_ids])
		if amb_arr.size > 1:
			print(f"\nAmbiguous input! Artists containing '{artist}':")
			for i in range(amb_arr.size):
				print(f"\t({i}) {int(math.ceil((4 - len(f'({i})')))) * ' '}{amb_arr[i]}")

			print()
			disamb_artist_id = input(f"Enter number of desired artist: ")
			disamb_artist = amb_arr[int(disamb_artist_id)]

			artist_ids = find_art_ids(disamb_artist)

		self.ind = np.random.choice(artist_ids)

		self.walkman_display()

	def genre_select(self, genre):

		def find_gen_ids(gen):
			gen_l = ud.unidecode(gen.lower()).replace(" ", "").replace("-", "")
			gen_ids = np.flatnonzero(np.core.defchararray.find(self.shelf["genre_pp"], gen_l) != -1)

			if gen_ids.size == 0:
				print(f"No genre found containing '{gen}'\n")
				gen = input("Enter a genre: ")
				gen_ids = find_gen_ids(gen)

			return gen_ids

		genre_ids = find_gen_ids(genre)

		# ambiguity check
		amb_arr = np.unique(self.shelf["genre"][genre_ids])
		if amb_arr.size > 1:
			print(f"Many {genre} sub-genres found:")
			for i in range(amb_arr.size):
				print(f"\t({i}) {int(math.ceil((4 - len(f'({i})')))) * ' '}{amb_arr[i]}")

			print()
			disamb_genre_id = input(f"Enter number of desired sub-genre or nothing for any {genre} album: ")
			if len(disamb_genre_id) == 0:
				pass
			else:
				disamb_genre = amb_arr[int(disamb_genre_id)]
				genre_ids = find_gen_ids(disamb_genre)

		self.ind = np.random.choice(genre_ids)

		self.walkman_display()

	def walkman_display(self):

		print()
		print(f"    /-----------------------------------\ \n"
			  f"  <|           Music selection           |>\n"
			  f"    \-----------------------------------/\n\n"
			  f"{' ' * 7}album: {int(math.ceil((10 - len('album: ')))) * ' '}{self.shelf['album'][self.ind]}\n"
			  f"{' ' * 7}artist: {int(math.ceil((10 - len('artist: ')))) * ' '}{self.shelf['artist'][self.ind]}\n"
			  f"{' ' * 7}genre: {int(math.ceil((10 - len('genre: ')))) * ' '}{self.shelf['genre'][self.ind]}\n")

	def vinyl_filter(self):

		vshelf = {"album": self.shelf["album"][self.shelf["vinyl"] == "yes"],
				  "artist": self.shelf["artist"][self.shelf["vinyl"] == "yes"],
				  "artist_pp": self.shelf["artist_pp"][self.shelf["vinyl"] == "yes"],
				  "genre": self.shelf["genre"][self.shelf["vinyl"] == "yes"],
				  "genre_pp": self.shelf["genre_pp"][self.shelf["vinyl"] == "yes"],
				  "vinyl": self.shelf["vinyl"][self.shelf["vinyl"] == "yes"]}

		vshelf["libsize"] = len(vshelf["album"])

		self.shelf = copy.copy(vshelf)


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Randomly select albums from a library")

	parser.add_argument("-l", type=str, default="charles", help="name of library")
	group = parser.add_mutually_exclusive_group()
	group.add_argument("-r", action="store_true", help="general random selection")
	group.add_argument("-a", action="store_true", help="random selection given artist")
	group.add_argument("-g", action="store_true", help="random selection given genre")

	parser.add_argument("-v", action="store_true", help="select from vinyl collection")

	args = parser.parse_args()

	filename = os.path.join(os.getenv("WALKMAN_PATH"), "library", "lib_charles.txt")
	wm = Walkman(filename, args.v)

	# General random selection
	if args.r:
		wm.rdm_select()

	# Random selection by artist
	elif args.a:
		artist = input("Enter an artist: ")
		wm.artist_select(artist)

	# Random selection by genre
	elif args.g:
		genre = input("Enter a genre: ")
		wm.genre_select(genre)
