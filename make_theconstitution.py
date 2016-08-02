import requests
from bs4 import BeautifulSoup
from os.path import exists
from os import makedirs

html = requests.get('https://www.constituteproject.org/constitution/' +
                    'United_States_of_America_1992?lang=en').text

articles = BeautifulSoup(html, 'html.parser').find_all(class_='level2')

markdown = ''
for article in articles:
    header = article.find('h3').get_text()
    markdown += '# %s\n\n' % header
    sections = article.find_all(class_='level3')

    for section in sections:
        if(section.find('h3')):
            header = section.find('h3').get_text()
            markdown += '## %s\n\n' % header
        paragraphs = [p.get_text() for p in section.find_all('p')]
        for paragraph in paragraphs:
            markdown += '%s\n\n' % paragraph

if not exists('theconstitution'):
    makedirs('theconstitution')

f = open('theconstitution/constitution.md', 'w')
f.write(markdown)
f.close()
