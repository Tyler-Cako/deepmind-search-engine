from urllib.parse import urlparse
import re

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

def getHostName(url: str) -> str:
    """
        Given url, return the hostname

        Args:
            url(str): Input URL
        Returns:
            hostname(str)
    """
    # parsed_url = urlparse(url)

    # hostname = parsed_url.hostname
    # scheme = parsed_url.scheme

    # if not scheme:
    #     scheme = "http"
    
    # rooturl = scheme + "://" + hostname

    # return rooturl.rstrip()
    return urlparse(url).hostname

def isValid(url: str, hostname: str) -> bool:
    """
        Checks if a URL is valid. a valid URL meets the following parameters:
            1. Starts with http(s)://
            2. Contains hostname in URL
            3. Contains a paper
        
        Args:
            url(str): input URL
            hostname(str): expected hostname
        
        Returns:
            isValid boolean  
    """

    if url[0:4] != "http":
        print("http not found in URL")
        return False
    
    if not url.find(hostname):
        print("hostname not found in URL")
        return False
    
    return True

def isPaper(url: str) -> bool:
    """
        Checks URL: to see if it is a paper or not
    """
    if re.search("(paper[/])|(publications[/])", url):
        return True

    return False