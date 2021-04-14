# This section imports various libraries used in the code.
import time # Allows adding delays to script
from bs4 import BeautifulSoup # Allows script to read and identify HTML elements
from selenium import webdriver # Allows script to run Chrome remotely
import csv # Allows script to write lists to csv files
import string # Allows generation of a list of uppercase alphabet letters

print('== PROGRAM START == \n')

lemmalist = []
lemmastrip=[]

alphabet = list(string.ascii_uppercase) 

for letter in alphabet:
    print('Currently working on letter:' + ' ' + letter + '\n')
    # Chromedriver accesses Google Chrome remotely and searches for word lists by letter
    chromedriver_path= "/PATH/chromedriver"
    driver = webdriver.Chrome(executable_path=chromedriver_path)
    url = "http://anw.inl.nl/lemmalist/" + letter
    driver.get(url)
    time.sleep(3) # Loading the page properly requires a slight delay
    driver.get(url)
    time.sleep(3) # An error causes page to load improperly on first attempt
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')
    div = soup.find('div', {'class':'col-sm-10'})   # The HTML code of the website is scanned for a <div class='col-sm-10'> element, 
                                                    # which this page uses for the words in the list.
    lemmalist = div.findAll('li')
    for lemma in lemmalist:
        lemmastripped = lemma.text.strip()
        lemmastrip.append(lemmastripped)
        
print('== WORDS IN LIST, NOW WRITING CSV FILE == \n')
    
with open('scrapedwords_nl.csv', 'w') as output: #scraped words are written to a csv file.
    write = csv.writer(output, lineterminator='\n')
    for lemma in lemmastrip:
        write.writerow([lemma])
        
print('==PROGRAM END ==')


