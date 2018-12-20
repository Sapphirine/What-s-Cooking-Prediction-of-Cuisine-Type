from src.models.recipes.constants import CUISINES_DST, CUISINES_SRC
from bs4 import BeautifulSoup
import requests


class Recipe(object):
    def __init__(self, ingredients, cuisine=None, pic=None, rec_name=None, rec_index=None):
        self.ingredients = ingredients
        self.cuisine = cuisine
        self.pic = pic
        self.rec_name = rec_name
        self.rec_index = rec_index

    def __repr__(self):
        return "<Recipe with ingredients {}>".format(self.ingredients)

    def get_by_cuisine(self):
        rec_name = []
        rec_index = []
        prefix = 'https://www.bbcgoodfood.com'
        headers = {'user-agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1'}

        if CUISINES_SRC[self.cuisine] < 13:
            cus_url = prefix + "/recipes/collection/" + CUISINES_DST[CUISINES_SRC[self.cuisine]]
        else:
            cus_url = prefix + "/search/recipes?query=" + self.cuisine

        response = requests.get(url=cus_url, headers=headers)
        recipe_content = response.content
        soup = BeautifulSoup(recipe_content, "lxml")

        cont = soup.find_all("h3", attrs={'class': 'teaser-item__title'})

        for item in cont:
            name = item.a.string
            rec_name.append(name)
            ind = item.a['href']
            rec_index.append(prefix+ind)

        self.rec_name = rec_name
        self.rec_index = rec_index

        for i in range(len(rec_name)):
            print(rec_name[i])
            print(rec_index[i])
