# boundary.py
def define_boundary(frame):
    height, width, _ = frame.shape
    # Define boundary as a central region (30% width, 50% height)
    x1 = int(width * 0.35)   
    x2 = int(width * 0.65)   
    y1 = int(height * 0.4)   
    y2 = int(height * 0.9)   

    return (x1, y1, x2, y2)

# def is_in_boundary(bbox, boundary):
#     x1, y1, x2, y2 = boundary
#     obj_x1, obj_y1, obj_x2, obj_y2 = bbox
#     return obj_x1 >= x1 and obj_x2 <= x2 and obj_y1 >= y1 and obj_y2 <= y2

def is_in_boundary(bbox, boundary):
    x1, y1, x2, y2 = boundary
    obj_x1, obj_y1, obj_x2, obj_y2 = bbox
    
    # Check if any part of the object's bounding box intersects with the boundary
    return not (obj_x2 < x1 or obj_x1 > x2 or obj_y2 < y1 or obj_y1 > y2)
