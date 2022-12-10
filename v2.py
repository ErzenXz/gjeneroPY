from gurobipy import *

# Data
P = 0  # Total number of photos
H = 0  # Number of horizontal photos
V = 0  # Number of vertical photos
NH = 0  # Number of horizontal-vertical pairs
NV = 0  # Number of vertical-vertical pairs
N = 0  # Total number of slides
photos = {}  # Maps photo ID to orientation
possible_slides = {}  # Maps photo ID to list of other photos that can be paired with it
same_photos = tuplelist([])  # Pairs of photos with the same tag

# Data from file
class PhotoSlideShowData:
    def __init__(self, M: int, photos: dict):
        self.M = M
        self.photos = photos


def read_instance_from_file(file_name: str):
    try:
        with open('PhotoSlideShow\\' + file_name, 'r') as f:
            # Read number of photos
            P = int(f.readline())
            # Read photo data
            photos = {}
            for i in range(P):
                photo_text = f.readline()
                photo_data = photo_text.split()
                photos[i] = photo_data
            result = PhotoSlideShowData(P, photos)
    except FileNotFoundError as e:
        print(e.strerror)
    except Exception as e:
        print(e.values)
    else:
        pass

    return result


# Read data from input file
file_name = 'a_example.txt'
slide_show_data = read_instance_from_file(file_name)

# Process data
for i in range(slide_show_data.M):
    photo = slide_show_data.photos[i]
    orientation = photo[0]
    if orientation == 'H':
        H += 1
    else:
        V += 1
    same_photos.append((i, photo[2:]))

NH = H
NV = V * (V - 1) / 2
N = NH + NV

# Preprocessing
for i in range(slide_show_data.M):
    photo = slide_show_data.photos[i]
    orientation = photo[0]
    possible_slides[i] = []
    for j in range(slide_show_data.M):
        if i != j:
            other_photo = slide_show_data.photos[j]
            other_orientation = other_photo[0]
            if orientation == 'H' and other_orientation == 'V':
                possible_slides[i].append(j)
            elif orientation == 'V' and other_orientation == 'V':
                possible_slides[i].append(j)

T, TI = multidict({(i, j): 0 for i in range(N) for j in range(N)})
a = 0
for i in range(N):
    for j in range(N):
        if i != j:
            T[(i, j)] = 0
            for tag in same_photos[i]:
                if tag in same_photos[j]:
                    a = 1

# Print generated data
print('Total number of photos:', P)
print('Number of horizontal photos:', H)
print('Number of vertical photos:', V)
print('Number of horizontal-vertical pairs:', NH)
print('Number of vertical-vertical pairs:', NV)
print('Total number of slides:', N)
print('Photos:', photos)
print('Possible slides:', possible_slides)
print('Photos with same tag:', same_photos)
print('Interest factors:', T)
