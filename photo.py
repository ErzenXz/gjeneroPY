P = 5

photos = {}
for i in range(1, P + 1):
    photo_text = input()
    photo_data = photo_text.split()
    orientation = photo_data[0]
    if orientation == 'H':
        photos[i] = 1
    else:
        photos[i] = 2

print(photos)