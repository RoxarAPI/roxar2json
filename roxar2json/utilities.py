import hashlib

def generate_color(text):
    hash_object = hashlib.sha256()
    hash_object.update(text.encode('ascii', errors='replace'))
    digest = hash_object.digest()
    segment_size = int(hash_object.digest_size / 3)
    red = int.from_bytes(digest[:segment_size], 'big') % 255
    green = int.from_bytes(digest[segment_size:-segment_size], 'big') % 255
    blue = int.from_bytes(digest[-segment_size:], 'big') % 255

    max_intensity = max(red, green, blue)

    frac = 255 / max_intensity

    red *= frac
    green *= frac
    blue *= frac

    red = int(red)
    green = int(green)
    blue = int(blue)

    return [red, green, blue, 255]
