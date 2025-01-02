from urllib.parse import urlparse

def appendUrl(root: str, url: str) -> str:
    """Makes relative path absolute"""
    return (root + url).rstrip()

def cleanUrl(url: str) -> str:
    """
        Check that URL starts with https and remove #tags from url. Also removes trailing characters from URL.

        Args:
            url (str): Input URl

        Returns:
            Cleaned URL
    """

    #Check if http
    if url[0:4] != "http":
        url = "http://" + url

    #Slice away page jumps (designeated with # in URL)
    i = url.find('#')
    if i != -1:
        url = url[:i]

    if url[-1] == "/":
        url = url[:-1]

    return url.rstrip()

def getRootUrl(url: str) -> str:
    """
        Given url, return the hostname

        Args:
            url(str): Input URL
        Returns:
            hostname(str)
    """
    parsed_url = urlparse(url)

    print(parsed_url)

    hostname = parsed_url.hostname
    scheme = parsed_url.scheme

    if not scheme:
        scheme = "http"
    
    rooturl = scheme + "://" + hostname

    return rooturl.rstrip()