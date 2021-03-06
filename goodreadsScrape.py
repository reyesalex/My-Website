from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

def simple_get(url): 
    try: 
        with closing(get(url, stream=True)) as resp: 
            if is_good_response(resp): 
                return resp.content
            else: 
                return None

    except RequestException as e: 
        log_error("Error using requests to {0} : {1}".format(url, str(e)))

def is_good_response(resp): 
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)

def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

def get_books():
    url = 'https://www.goodreads.com/user_challenges/16171692'
    response = simple_get(url)

    returnArr = []
    
    soup = BeautifulSoup(response, 'html.parser')

    if response is not None: 
        
        for li in soup.find_all('li', attrs={'class': 'bookCoverContainer'}):
            title = li.find('img', alt=True)
            link = li.find('a', attrs={'class': 'bookCoverTarget'})
            
            if title['alt'] is not "":
                newDict = {}
                title = title['alt']
                link = "https://www.goodreads.com" + link['href']

                newDict[title] = link

                returnArr.append(newDict)
    
    return returnArr
    