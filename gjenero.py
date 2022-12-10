from gurobipy import *
from collections import defaultdict

# Data
P = 50
H = 25
V = 25
NH = 25
NV = V * (V - 1) / 2  # NV=3
N = int(NH + NV)  # N=5

with open("P10.txt", 'r') as f:
    photo_types = []
    for line in f:
        if line[0] == "H":
            photo_types.append(1)
        elif line[0] == "V":
            photo_types.append(2)

photos = {}
for i in range(len(photo_types)):
    photos[i+1] = photo_types[i]


# Preprocessing
possible_slides = {}

for photo_num, photo_type in photos.items():
    if photo_type == 1:
        # Horizontal photo, add slide containing only that photo
        possible_slides[photo_num] = [photo_num]
    elif photo_type == 2:
        # Vertical photo, add pairs with all other vertical photos
        possible_pairs = []
        for other_photo_num, other_photo_type in photos.items():
            if other_photo_type == 2 and other_photo_num != photo_num:
                possible_pairs.append((photo_num, other_photo_num))
            possible_slides[photo_num] = possible_pairs


with open("P10.txt", "r") as f:
    P = int(f.readline())
    tags = {}
    for i in range(P):
        photo_text = f.readline()
        photo_data = photo_text.split()
        if photo_data[0] == "H":
            photo_types = 1
        elif photo_data[0] == "V":
            photo_types = 2
        tags[i+1] = photo_data[2:]



same_photos = []
for i in range(1, len(tags)):
    for j in range(i+1, len(tags) + 1):
        if len(set(tags[i]) & set(tags[j])) > 0:
            same_photos.append((i, j))

multidict = defaultdict(int)

for pair in same_photos:
    if pair[0] in tags and pair[1] in tags:
        score = len(set(tags[pair[0]]) & set(tags[pair[1]]))
        multidict[pair] = score

T = multidict.values()
TI = multidict.keys()


# Convert the dict_keys objects to a list

T = list(T)
TI = list(TI)


# Data from file


class PhotoSlideShowData:
    def __init__(self, M: int, photos: dict):
        self.M = M
        self.photos = photos


file_name = 'P10.txt'


def read_instance_from_file(file_name: str):
    try:
        with open(file_name, 'r') as f:
            P = int(f.readline())
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


slide_show_data = read_instance_from_file(file_name)
# print(slide_show_data.M)
# print(slide_show_data.photos)

m = Model('photo slide show')

z = {}
for pair, score in multidict.items():
    z[pair] = m.addVar(vtype=GRB.BINARY, name="z%d" % i)

z = {}
for i in range(1, N + 1):
    for j in range(1, N + 1):
        if i != j:
            z[(i, j)] = m.addVar(vtype=GRB.BINARY, name='z' + str(i) + str(j))

# Constraints
for sp in same_photos:
    i = sp[0]
    j = sp[1]
    m.addConstr(quicksum(
        quicksum(z[(a, b)] for b in range(1, N + 1) if b != a and (a == i or a == j or b == i or b == j)) for a in
        range(1, N + 1)) <= 1, name='same photos')

for i in range(1, N + 1):
    m.addConstr(quicksum(z[(i, j)] for j in range(1, N + 1) if j != i) <= 1,
                name='one slide is placed after slide i')

for j in range(1, N + 1):
    m.addConstr(quicksum(z[(i, j)] for i in range(1, N + 1) if j != i) <= 1,
                name='one slide is placed after slide j ')

for i in range(1, N + 1):
    for j in range(1, N + 1):
        if i != j:
            m.addConstr(z[(i, j)] + z[(j, i)] <= 1,
                        name='each slide is used at most once')

m.update()
m.setObjective(quicksum(quicksum(z[str((i, j))] * TI[(i, j)] if (i, j) in TI and str((i, j)) in z else 0 for j in range(2, N + 1) if j != i)
    for i in range(1, N)), sense=GRB.MAXIMIZE)
m.optimize()
m.printAttr('X')