# Retrieve talks by speaker on speeches.byu.edu using BeautifulSoup

from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import re

'''Get list of urls for each of the topics For my reference, number of talks by speaker:  Nelson - 22, Maxwell - 30, 
Holland - 27, Hinckley - 41, Monson - 14, Oaks - 35, Eyring - 25 (Total - 194)'''
url = "https://speeches.byu.edu/speakers/"

url_list = [
    'russell-m-nelson/', 'neal-a-maxwell/', 'jeffrey-r-holland/', 'gordon-b-hinckley/', 'thomas-s-monson/',
    'dallin-h-oaks', 'henry-b-eyring'
]

links = []
new_links = []

''' some of the links are repeated with '?M=V' and '?M=A' and those will be removed so we can have a unique set of 
links to pull talk information from.'''

for u in url_list:
    response = requests.get(url + u)
    html = response.content
    video = '?M=V'
    soup = bs(html, 'lxml')
    for link in soup.findAll("a", attrs={'href': re.compile("^https://speeches.byu.edu/talks/[\D+]")}):
        links.append(link.get('href').replace(video, ''))

    audio = '?M=A'
    for link in links:
        new_link = link.replace(audio, '')
        new_links.append(new_link)
    new_links = list(set(new_links))

print(len(new_links))

'''Retrieves talk text from each of the urls using beautiful soup.  Information such as the talk/sermon text, title, 
topic, date, and speaker will be retrieved and put into a dataframe.  A csv file will also be saved due to the time 
it takes to run or in case we need to work offline. '''

talk_text = []
speakers = []

for link in new_links:
    url = link
    response = requests.get(url)
    html = response.content
    soup = bs(html, 'lxml')
    temp_list = []

    link_splitter = link.split('/')
    speakers.append(link_splitter[4].replace('-', ' '))

    for div in soup.find_all('div', class_='single-speech__content'):
        talk_text.append(div.get_text(strip=True))

dict_speeches_byu = {'speaker': speakers, 'talks': talk_text}
df = pd.DataFrame(dict_speeches_byu)

print(df.sample(15))

# Now to pull information from the church general conference website.

# Get list of urls for each of the topics
gc_url = "https://www.churchofjesuschrist.org/study/general-conference/speakers/"

gc_url_list = [
    'russell-m-nelson/', 'neal-a-maxwell/', 'jeffrey-r-holland/', 'gordon-b-hinckley/', 'thomas-s-monson/',
    'dallin-h-oaks', 'henry-b-eyring'
]

links = []

for u in gc_url_list:
    response = requests.get(gc_url + u)
    html = response.content
    soup = bs(html, 'lxml')
    for link in soup.findAll("a", attrs={'href': re.compile("^/study/general-conference/\w+/(?:\w+/)(?:\w+)")}):
        links.append(link.get('href'))

talk_text = []
speakers = []

for link in links:
    url = 'https://www.churchofjesuschrist.org'+link
    response = requests.get(url)
    html = response.content
    soup = bs(html, 'lxml')

    sermon_name = soup.find_all('div', class_='byline')
    '''This is basically a switch statement that will allow for the speaker column to have the same format as the 
    dataframe speeches.byu.edu dataframe created above.'''
    for x in sermon_name:
        if 'nelson' in x.find('p').text.lower():
            speakers.append('russell m nelson')
        elif 'maxwell' in x.find('p').text.lower():
            speakers.append('neal a maxwell')
        elif 'holland' in x.find('p').text.lower():
            speakers.append('jeffrey r holland')
        elif 'hinckley' in x.find('p').text.lower():
            speakers.append('gordon b hinckley')
        elif 'monson' in x.find('p').text.lower():
            speakers.append('thomas s monson')
        elif 'oaks' in x.find('p').text.lower():
            speakers.append('dallin h oaks')
        else:
            speakers.append('henry b eyring')

    for div in soup.find_all('div', class_='body-block'):
        talk_text.append(div.get_text(separator= ' ', strip=True))

dict_gc = {'speaker': speakers,'talks': talk_text}
df_gc = pd.DataFrame(dict_gc)

print(df_gc.sample(15))

df = df.append(df_gc)
df.to_csv('talk_corpus.csv')
print(df.sample(50))