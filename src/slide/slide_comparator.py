def compare(slide1, slide2):
    return min([
        len(slide1.tags.intersection(slide2.tags)),
        len(slide1.tags - slide2.tags),
        len(slide2.tags - slide1.tags)
    ])