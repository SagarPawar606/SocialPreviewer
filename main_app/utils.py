import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def validate_url(url_str):
    regex = r'[(http(s)?):\/\/(www\.)?a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)'
    compiler = re.compile(regex)
    if(re.search(compiler, url_str)):
        return True
    print('[INVALID URL]')
    return False

def get_meta_data(req_url):
    req_url = str(req_url)
    if not validate_url(req_url):
        '''Check if its valid url pattern or not'''
        return False

    try:
        '''Will raise excepption if no such url found'''
        req = requests.get(req_url)
    except Exception as e:
        print('[NO SUCH URL FOUND]', e)
        return False

    soup = BeautifulSoup(req.content, 'html.parser')

    # SITE DATA
    site_title = soup.find("title")
    site_description = soup.find("meta", {"name":"description"})
    site_domain = urlparse(req_url).netloc
    
    # OG:DATA
    og_title = soup.find("meta",  property="og:title")
    og_description = soup.find("meta",  property="og:description")
    og_image = soup.find("meta", property="og:image")
    og_url = soup.find("meta", property="og:url")
    og_site = soup.find("meta", property="og:site_name")
    og_embeded_url = soup.find("meta", property="og:video:url")
    og_favicon = soup.find("link", rel="shortcut icon")
    if not og_favicon:
        og_favicon = soup.find("link", rel="icon")
    og_dict = {
                "title" : site_title.string if site_title else None,
                "description" : site_description['content'] if site_description else None,
                "site_domain" : site_domain,
                "og_title" : og_title['content'] if og_title else None,
                "og_description" : og_description['content'] if og_description else None,
                "og_image" : og_image['content'] if og_image else None,
                "og_url" : og_url['content'] if og_url else None,
                "og_site" : og_site['content'] if og_site else None,
                "og_embeded_url" : og_embeded_url['content'] if og_embeded_url else None,
                "og_favicon" : og_favicon['href'] if og_favicon else None,
                
                }

    # # TIWTTER:DATA
    twtr_title = soup.find("meta",  {"name":"twitter:title"})
    twtr_description = soup.find("meta",  {"name":"twitter:description"})
    twtr_card = soup.find("meta",  {"name":"twitter:card"})
    twtr_image = soup.find("meta", {"name":"twitter:image"})
    twtr_url = soup.find("meta", {"name":"twitter:url"})
    twtr_site = soup.find("meta", {"name":"twitter:site"})
    twtr_embeded_url = soup.find("meta", {"name":"twitter:player"})

    '''If twtr_card found every other field will 
        get override by every other og field respectively, 
        else twitter preview will be none
    '''
    twtr_dict = {
                "twtr_card" : twtr_card['content'] if twtr_card else None,
                "twtr_title" : twtr_title['content'] if twtr_title else og_dict['og_title'],
                "twtr_description" : twtr_description['content'] if twtr_description else og_dict['og_description'],
                "twtr_image" : twtr_image['content'] if twtr_image else og_dict['og_image'],
                "twtr_url" : twtr_url['content'] if twtr_url else og_dict['og_url'],
                "twtr_site" : twtr_site['content'] if twtr_site else og_dict['og_site'],
                "twtr_embeded_url" : twtr_embeded_url['content'] if twtr_embeded_url else og_dict['og_embeded_url'],
                }
    
    og_dict.update(twtr_dict)
    return og_dict