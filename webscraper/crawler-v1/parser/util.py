def appendUrl(root: str, url: str) -> str:
    """Makes relative path absolute"""
    return (root + url).rstrip()