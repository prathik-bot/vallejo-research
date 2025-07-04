# app/utils/helpers.py
from math import radians, sin, cos, sqrt, atan2


def calculate_bounding_box(lat, lng, radius_km):
    """Calculate NW and SE coordinates for a bounding box"""
    radius_deg = radius_km / 111.32  # Approx km per degree

    nw_lat = lat + radius_deg
    nw_lng = lng - radius_deg / cos(radians(lat))

    se_lat = lat - radius_deg
    se_lng = lng + radius_deg / cos(radians(lat))

    return {
        'nw': {'lat': nw_lat, 'lng': nw_lng},
        'se': {'lat': se_lat, 'lng': se_lng}
    }