def pick_largest_face(faces):
    if not faces:
        return None
    return max(faces, key=lambda f: (f.bbox[2]-f.bbox[0]) * (f.bbox[3]-f.bbox[1]))
