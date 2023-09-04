import math

def euclidean_distance(point1, point2):
    """Calculate the Euclidean distance between two 2D points."""
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def haversine_distance(coord1, coord2, radius=6371.0):
    """
    Calculate the great-circle distance between two points on the Earth.
    
    :param coord1: Tuple (latitude, longitude) of the first point.
    :param coord2: Tuple (latitude, longitude) of the second point.
    :param radius: Radius of the Earth (default is in kilometers). 
                   Use radius=3958.8 for miles.
    :return:       Great-circle distance between the two points.
    """
    
    # lat/lon degrees -> radians
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = (math.sin(dlat / 2)**2 +
         math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = radius * c

    return distance


def is_point_in_polygon(p, polygon):
    """
    Determine if the point p is inside the polygon.
    
    :param p:       Tuple (x, y), the point to test
    :param polygon: List of tuples [(x1, y1), (x2, y2), ...], representing 
                    the vertices of the polygon.
    :return:        True if point p is inside the polygon, False otherwise.
    """
    
    x, y = p
    odd_nodes = False
    j = len(polygon) - 1  # Last vertex in the polygon

    for i in range(len(polygon)):
        xi, yi = polygon[i]
        xj, yj = polygon[j]
        
        if yi < y and yj >= y or yj < y and yi >= y:
            if xi + (y - yi) / (yj - yi) * (xj - xi) < x:
                odd_nodes = not odd_nodes
        j = i
    return odd_nodes
