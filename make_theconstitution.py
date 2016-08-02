import requests
from bs4 import BeautifulSoup
import os
from datetime import date, datetime
from time import strftime, mktime

html = requests.get('https://www.constituteproject.org/constitution/' +
                    'United_States_of_America_1992?lang=en').text

articles = BeautifulSoup(html, 'html.parser').find_all(class_='level2')

if os.path.exists('theconstitution'):
    os.system('rm -rf theconstitution')
os.makedirs('theconstitution')

os.chdir('theconstitution')
os.system('git init')

amendment_dates = ['06/21/1788']*8 + ['12/15/1791']*10 + \
                  ['02/7/1795', '06/15/1804', '12/06/1865',
                   '07/9/1868', '02/03/1870', '02/03/1913', '04/08/1913',
                   '01/16/1919', '08/18/1920', '01/23/1933', '12/5/1933',
                   '02/27/1951', '03/29/1961', '01/23/1964', '02/10/1967',
                   '07/01/1971', '05/7/1992']

print(len(amendment_dates))


def commit(markdown, header, commit_date):
    f = open('constitution.md', 'w')
    f.write(markdown)
    f.close()
    os.system('git add constitution.md')
    cmd = "git commit -m '{0}: {1}'".format(commit_date, header)
    os.system(cmd.format(commit_date, header))

markdown = ''
for i, article in enumerate(articles):
    article_name = article.find('h3').get_text()
    markdown += '# %s\n\n' % article_name
    sections = article.find_all(class_='level3')

    for section in sections:
        if(section.find('h3')):
            header = section.find('h3').get_text()
            markdown += '## %s\n\n' % header
        paragraphs = [p.get_text() for p in section.find_all('p')]
        for paragraph in paragraphs:
            markdown += '%s\n\n' % paragraph

    if i == 7:
        commit(markdown, 'Articles of the Constitution', amendment_dates[i])
    if i == 17:
        commit(markdown, 'Bill of Rights', amendment_dates[i])
    if i > 17:
        commit(markdown, article_name, amendment_dates[i])

os.system('cp ../theconstitution_readme.md README.md')
os.system('git add README.md')
os.system("git commit -m 'adding readme (note: not in actual constitution)'")
os.system('git remote add origin ' +
          'git@github.com:anthonygarvan/theconstitution.git')
