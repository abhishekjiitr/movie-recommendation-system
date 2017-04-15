import requests
import os

def get_poster(imdburl, counter = 1):
    r = requests.get(imdburl) 
    movieid = r.url.split("/")[-2]
    print(r.url)
    CONFIG_PATTERN = 'http://api.themoviedb.org/3/configuration?api_key={key}'
    KEY = '899fa90e71f003b69927429c6dad961c'

    url = CONFIG_PATTERN.format(key=KEY)
    r = requests.get(url)
    config = r.json()

    base_url = config['images']['base_url']
    sizes = config['images']['poster_sizes']
    """
        'sizes' should be sorted in ascending order, so
            max_size = sizes[-1]
        should get the largest size as well.        
    """
    def size_str_to_int(x):
        return float("inf") if x == 'original' else int(x[1:])
    max_size = sizes[2]
    IMG_PATTERN = 'http://api.themoviedb.org/3/movie/{imdbid}/images?api_key={key}' 
    r = requests.get(IMG_PATTERN.format(key=KEY,imdbid=movieid))
    api_response = r.json()
    print(api_response)
    posters = api_response['posters']
    poster_urls = []
    for poster in posters:
        rel_path = poster['file_path']
        url = "{0}{1}{2}".format(base_url, max_size, rel_path)
        poster_urls.append(url)

    # print poster_urls

    for nr, url in enumerate(poster_urls):
        r = requests.get(url)
        filetype = r.headers['content-type'].split('/')[-1]
        filename = 'poster_{0}.{1}'.format(nr+1,filetype) 
        with open(os.path.join("downloads", str(counter)),'wb') as w:
            w.write(r.content)
        break

