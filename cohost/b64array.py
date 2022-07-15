# this file is a bit of a mess
# i tried porting the b64 stuff from @mog's JS library
# but it's a bit of a mess in trying to find equivalent python things
# i instead wanted to focus on getting endpoints working *once* logged in, as i think this is only needed for that
# if you care about login, feel free to fix lol
# but be warned this
HOURS_WASTED = 2
# anyway

chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

# Use a lookup table to find the index.
lookup = []
for char in chars:
    lookup.append(ord(char))


def decode(base64):
    """straight port (i think) of Mog's code here. It's a bit hacky, but, hey, means I don't have to reverse engineer this myself.

    Args:
        base64 (_type_): b64 buffer thingy

    Returns:
        _type_: _description_
    """
    bufferLength = len(base64) * 0.75
    p = 0
    if (base64[len(base64) - 1] == "="):
        bufferLength -= 1
    if (base64[len(base64) - 2] == "="):
        bufferLength -= 1
    
    b = []

    for i in range(0, len(base64), 4):
        print(base64)
        print(lookup)
        encoded1 = lookup[ord(base64[i])];
        encoded2 = lookup[ord(base64[i+1])];
        encoded3 = lookup[ord(base64[i+2])];
        encoded4 = lookup[ord(base64[i+3])];
        p += 1
        b[p] = (encoded1 << 2) | (encoded2 >> 4);
        p += 1
        b[p] = ((encoded2 & 15) << 4) | (encoded3 >> 2);
        p += 1
        b[p] = ((encoded3 & 3) << 6) | (encoded4 & 63);
    

    return b;
