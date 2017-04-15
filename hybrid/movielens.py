import re

class User:
    def __init__(self, id, age, sex, occupation, zip):
        self.id = int(id)
        self.age = int(age)
        self.sex = sex
        self.occupation = occupation
        self.zip = zip
        self.avg_r = 0.0

class Item:
    def __init__(self, id, title, release_date, video_release_date, imdb_url, \
    unknown, action, adventure, animation, childrens, comedy, crime, documentary, \
    drama, fantasy, film_noir, horror, musical, mystery, romance, sci_fi, thriller, war, western, actor, country, director, genre, lang, rating, year, production):
        self.id = int(id)
        self.title = title
        self.release_date = release_date
        self.video_release_date = video_release_date
        self.imdb_url = imdb_url
        self.unknown = int(unknown)
        self.action = int(action)
        self.adventure = int(adventure)
        self.animation = int(animation)
        self.childrens = int(childrens)
        self.comedy = int(comedy)
        self.crime = int(crime)
        self.documentary = int(documentary)
        self.drama = int(drama)
        self.fantasy = int(fantasy)
        self.film_noir = int(film_noir)
        self.horror = int(horror)
        self.musical = int(musical)
        self.mystery = int(mystery)
        self.romance = int(romance)
        self.sci_fi = int(sci_fi)
        self.thriller = int(thriller)
        self.war = int(war)
        self.western = int(western)
        self.actor = actor
        self.country = country
        self.director = director
        self.genre = genre
        self.lang = lang
        try:
            self.rating = float(rating[0])
        except:
            self.rating = 0
        try:
            self.year = int(year)
        except:
            self.year = 1900
        self.production = production
class Rating:
    def __init__(self, user_id, item_id, rating, time):
        self.user_id = int(user_id)
        self.item_id = int(item_id)
        self.rating = int(rating)
        self.time = time

class Dataset:
    def load_users(self, file, u):
        f = open(file, "r")
        text = f.read()
        entries = re.split("\n+", text)
        for entry in entries:
            e = entry.split('|', 5)
            if len(e) == 5:
                u.append(User(e[0], e[1], e[2], e[3], e[4]))
        f.close()

    def load_items(self, file, i):
        total_movies = 0
        f = open(file, "r")
        text = f.read()
        with open('scraped_data.txt', 'r') as scraped_data:
            data = scraped_data.readlines()
        data = [el.strip() for el in data]
        # print(data)
        info = {}
        for mov in data:
            myid, mydata = int(mov.split('|')[0]), mov.split('|')[1:]
            # print(myid)
            # print(mydata)
            mydata = [data.split(',') for data in mydata]
            # print(mydata)
            mydata = [ [el.strip() for el in data] for data in mydata]
            # print(mydata)
            info[myid] = mydata
            # break
        entries = re.split("\n+", text)
        for entry in entries:
            e = entry.split('|', 24)
            if len(e) == 24:
                total_movies += 1
                id = int(e[0])
                if id in info:
                    # print("YO")
                    data = info[id]
                    i.append(Item(e[0], e[1], e[2], e[3], e[4], e[5], e[6], e[7], e[8], e[9], e[10], e[11], e[12], e[13], e[14], \
                e[15], e[16], e[17], e[18], e[19], e[20], e[21], e[22], e[23], data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]))
                # else:
                #     i.append(Item(e[0], e[1], e[2], e[3], e[4], e[5], e[6], e[7], e[8], e[9], e[10], e[11], e[12], e[13], e[14], \
                # e[15], e[16], e[17], e[18], e[19], e[20], e[21], e[22], e[23], "", "", "", "", "", [-1], "", ""))
                # break
        f.close()
        self.total_movies = total_movies
        
    def load_ratings(self, file, r):
        f = open(file, "r")
        text = f.read()
        entries = re.split("\n+", text)
        for entry in entries:
            e = entry.split('\t', 4)
            if len(e) == 4:
                r.append(Rating(e[0], e[1], e[2], e[3]))
        f.close()
