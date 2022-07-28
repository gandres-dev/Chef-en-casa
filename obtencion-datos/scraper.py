from cmath import e
from urllib.request import urlopen
from bs4 import BeautifulSoup
from pymongo import MongoClient
from tqdm import tqdm 
import logging
import time
import sys
import argparse

LOG_FORMAT = "%(levelname)s %(asctime)s: %(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
logger = logging.getLogger()

def get_recipes_urls(url):
  """Obtiene las direcciones url del sitio web de las recetas
  
  Parametros
  ----------
  url: str
    URL direcction recipes

  Return
  ------
  url_recipes: str
    URL's recipes 
  """
  html = urlopen(url)
  bs = BeautifulSoup(html, 'html.parser')
  articles = bs.find_all('article', {'class': {'article-loop', 'asap-columns-3'}})
  url_recipes = []
  for article in articles:  
    url_recipes.append(article.a.get('href'))  
  return url_recipes


def get_info_recipe(url_recipe):
  """Get information of the url recipe

  Parameters
  ---------
  url_recipe: str
    URL where we find recipe
  
  Return
  -------
  recipe: dict
    One recipe with format json
  """
  html = urlopen(url_recipe)
  bs = BeautifulSoup(html, 'html.parser')
  recipe = {}
  title = bs.h1.get_text()
  recipe['title'] = title
  recipe['ingredients'] = []
  # Obtencion de los ingredientes
  try:
    tags_ingredientes = bs.findAll('ul', class_=None)[0].findAll('li')      
    for ingrediente in tags_ingredientes:
      recipe['ingredients'].append(ingrediente.getText())    
    paragraphs = bs.find('div', class_='the-content').findAll('p', class_=None)[1:-1]
    description = ""
    for i, paragraph in enumerate(paragraphs):
      description += paragraph.getText()
    url_video = bs.find('iframe').get('src')
    url_image = bs.find('div', class_='post-thumbnail').find('img').get('src')    
    recipe['procedimiento'] = description
    recipe['url_video'] = url_video
    recipe['url_image'] = url_image
  except:
    return None
  return recipe



def retrieve_recipes(pages=1):
  """Retrive recipes in the page https://recetas-mexicanas.com.mx
  
  Parameters
  ----------
  page: int
    Number page of the siteweb
  
  Return
  ------
  recipe: list
    List recipes of the page
  """
  recipes = []  
  # Get 10 recipes by page
  url_recipes = get_recipes_urls(f'https://recetas-mexicanas.com.mx/page/{pages}') 
  #print(url_recipes)   
  for url_recipe in url_recipes:    
    # try:
    #print(f'url-recipe {url_recipe}')
    recipe = get_info_recipe(url_recipe)   
    if recipe == None:
      continue 
    # except:
      # logger.warning('Error al desestructurar')           
    recipes.append(recipe)
    logger.info(f'Agregando {recipe["title"]}...')
    time.sleep(2) 
  return recipes       


def schedule(step=1, begin_page=1, end_page=10):
  """Retrive the data every step time
  
  step: int
    Time lapse for every called in retrive recipes
  """
  recipes = []
  for page in tqdm(range(begin_page, end_page+1), ascii=True):
    recipes.extend(retrieve_recipes(page))
    time.sleep(step)    
  recipes_collection.insert_many(recipes)
      


if __name__ == "__main__":
  logger.info('Request data to https://recetas-mexicanas.com.mx/')  
  parser = argparse.ArgumentParser(description='Scraper mexican recipes')
  parser.add_argument('-b', '--begin_page', type=int, help='Begin page',
                      default=1)
  parser.add_argument('-e', '--end_page', type=int, help='End page',
                      default=2)
  args = parser.parse_args()

  # Conect DB
  client = MongoClient('localhost', 27017)
  db = client['chef-casa']
  recipes_collection = db['recipes']  
  
  
  # Retrive recipes of the page every step
  schedule(step=1, begin_page=args.begin_page, end_page=args.end_page)
  logger.info('Listo! Guardado en MongoDB.')


