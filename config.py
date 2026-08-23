def get_region(lat, lon):
    if lat < 19.05:
        return "CENTRAL"
    elif lon < 72.85:
        return "WEST"
    else:
        return "EAST"