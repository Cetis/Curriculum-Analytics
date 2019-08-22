#not a good way to do this. It is getting every single instance of a module from the site so we can do some early text analysis

import psycopg2
from bs4 import BeautifulSoup 
import urllib3
import requests
import re

def create_table():
    print("in creating table method")
    con = psycopg2.connect(database="postgres", user="postgres", password="gladdylight", host="127.0.0.1", port="5432")
    cur = con.cursor()
    cur.execute('''CREATE TABLE module
        (ID SERIAL PRIMARY KEY     NOT NULL,
        TITLE           VARCHAR    NULL,
        CODE            VARCHAR    NULL,
        TUTOR           VARCHAR    NULL,
        SCHOOL           VARCHAR    NULL,
        CAT           VARCHAR    NULL,
        LEVEL           VARCHAR    NULL,
        DESCRIPTION           VARCHAR    NULL,
        SYLLABUS            VARCHAR      NULL,
        OUTCOMES           VARCHAR    NULL,
        ACTIVITIES           VARCHAR    NULL,
        ASSESSMENT           VARCHAR    NULL,
        SPECIAL           VARCHAR    NULL,
        RESOURCES        VARCHAR    NULL)''')

    con.commit()
    con.close()


def get_maps(maps_url):
    #fake headers..
    print("we are now going through every page and getting a lit of every single coure map")
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    page = requests.get(maps_url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')

    links = soup.find_all("a", href=re.compile("/courses/undergraduate"))
    
    links_array = []
    
    for link in links:
        link_text = "https://www.glos.ac.uk/" + link.get('href')
        links_array.append(link_text)

    links_array = list(dict.fromkeys(links_array))

    map_links_array = []
    for single_link in links_array:
        print("we ae looking for course maps on page..")
        print(single_link)
        page = requests.get(single_link, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')
        map_links = soup.find_all("a", href=re.compile("/courses/undergraduate"))
        for map_link in map_links:
            if "maps/pages" in map_link.get('href'):
                link_text = "https://www.glos.ac.uk/" + map_link.get('href')
                map_links_array.append(link_text)

        
    map_links_array = list(dict.fromkeys(map_links_array)) 
    print("every single course_map page:")
    print(map_links_array)
    return(map_links_array)


def get_links(url):
    #fake headers..
    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')

    tables = soup.findAll('table') 
    links_array = []
    for table in tables:
        links = table.findAll('a')

        for link in links:
            links_array.append(link.get('href'))

    return(links_array)

def get_details(url):
    #fake headers..
    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')

    table = soup.find("table",{"class":"descriptor-table"})
    rows = table.find_all("tr")
    fields_array = []

    for tr in rows:
        td = tr.find("td")
        th = tr.find("th")
        if not td.getText().strip():
            fields_array.append("Null")
        else:
            text = td.getText()
            #text = text.encode('utf-8')
            fields_array.append(text)

    return(fields_array)

def insert(fields):

   con = psycopg2.connect(database="postgres", user="postgres", password="gladdylight", host="127.0.0.1", port="5432")
   cursor = con.cursor()

   postgres_insert_query = """ INSERT INTO module (TITLE, CODE, TUTOR, SCHOOL, CAT, LEVEL, DESCRIPTION, SYLLABUS, OUTCOMES, ACTIVITIES, ASSESSMENT, SPECIAL, RESOURCES) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
   try:
        cursor.execute(postgres_insert_query,fields)
        print("inserted")
   except:
        print("string problem")
   

   con.commit()
   count = cursor.rowcount
   cursor.close()
   con.close()


if __name__ =="__main__":

    #create db
    try:
        create_table()
    except:
        print("Did not create")

    maps_links = get_maps("https://www.glos.ac.uk/study/pages/course-finder.aspx?studyLevel=undergraduate&subjectArea=null&schoolCode=null#courseFinder")
    #return links from url
    for map_link in maps_links:
        print("looking at a page with course map info on it:")
        print(map_link)
        links = get_links(map_link)  
    
        for link in links:
            link = "https://www.glos.ac.uk/" + link
            print(link)
            fields = get_details(link)
            #print(fields)
            insert(fields)