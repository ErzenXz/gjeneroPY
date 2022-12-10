# Data
M = 4  # Number of photos
photos = [
    {"type": "H", "tags": ["cat", "beach", "sun"]},  # Photo 1
    {"type": "V", "tags": ["selfie", "smile"]},  # Photo 2
    {"type": "V", "tags": ["garden", "selfie"]},  # Photo 3
    {"type": "H", "tags": ["garden", "cat"]},  # Photo 4
]

# Preprocessing
possible_slides = []
same_photos = []
multidict = {}

# Generate possible_slides
for i in range(M):
    if photos[i]["type"] == "H":
        # Horizontal photos can be used as a single slide
        possible_slides.append([i])
    else:
        # Vertical photos must be paired with another vertical photo
        # to create a slide
        possible_slides.append([i, j] for j in range(i + 1, M) if photos[j]["type"] == "V")

# Generate same_photos
for i in range(M):
    for j in range(i + 1, M):
        # If the two photos have any tags in common, they are considered "same photos"
        common_tags = set(photos[i]["tags"]) & set(photos[j]["tags"])
        if common_tags:
            same_photos.append((i, j))

# Generate multidict
for i in range(M):
    for j in range(i + 1, M):
        # Compute the number of common tags between photos i and j
        common_tags = len(set(photos[i]["tags"]) & set(photos[j]["tags"]))
        # Compute the number of unique tags in photo i
        unique_i = len(set(photos[i]["tags"]) - set(photos[j]["tags"]))
        # Compute the number of unique tags in photo j
        unique_j = len(set(photos[j]["tags"]) - set(photos[i]["tags"]))
        # The "value" for the multidict entry for photos i and j is the minimum
        # of the number of common tags, the number of unique tags in photo i,
        # and the number of unique tags in photo j.
        multidict[(i, j)] = min(common_tags, unique_i, unique_j)

print(possible_slides)
print(multidict)
print(same_photos)