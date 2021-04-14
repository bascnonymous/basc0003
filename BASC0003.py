#
# PART 1: CREATING A DUTCH WORD LIST
#

# This section imports various libraries used in the code.
import time # Allows adding delays to script
from bs4 import BeautifulSoup # Allows script to read and identify HTML elements
from selenium import webdriver # Allows script to run Chrome remotely
from selenium.webdriver.common.keys import Keys # Allows script to use keys in remotely ran Chrome
import csv # Allows script to write lists to csv files
import string # Allows generation of a list of uppercase alphabet letters

print('== PROGRAM START == \n')
print('== CREATING DUTCH WORD LIST == \n')

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

#
# PART 2: COMPARING THE DUTCH AND ENGLISH DICTIONARIES
#

print('== COMPARING DUTCH AND ENGLISH DICTIONARIES == \n')
# The dictionary files are read and added to lists
print('Reading file 1... \n')
with open('scrapedwords_nl.csv','r') as file1:
    data1 = file1.readlines()
print('Reading file 2... \n')
with open('words_uk.txt','r') as file2:
    data2 = file2.readlines()
# A new file is created and written in
print('Writing matching entries to new file... \n')
with open('words_similar.csv', 'w') as output:
    # This loop compares entries between the files
    for file1_data in data1:
        for file2_data in data2:
            # Find matching entries, taking into account capitalisation and spacing differences.
            if file1_data.strip().lower() == file2_data.strip().lower():
                # Write identical entries into a new txt file
                output.write(file2_data.strip()+'\n')

#
# PART 3.1: CHECKING THE ETYMOLOGIES OF THE LOAN WORD LIST WITH ETYMOLOGIEBANK
#

print('== CHECKING ETYMOLOGIES OF LOANWORD LIST WITH ETYMOLOGIEBANK == \n')

divstrip = []
checked_loanwords = []
datastrip = []

# This opens the file created by the previous code.
with open('words_similar.csv','r') as input:
    data = input.readlines()
    
# All data is stripped and lowercase to be consistent throughout the code.
for entry in data:
    datastrip.append(entry.strip().lower())

# Chromedriver accesses Google Chrome remotely, allowing for automated website searches.
chromedriver_path= "/PATH/chromedriver" # Path was replaced with placeholder for security reasons
driver = webdriver.Chrome(executable_path=chromedriver_path)

english = 'engels'

# This loop searches the etymologiebank website to find words that have been loaned from english
for word in datastrip:
    engels_seen = 0 
    print ('Currently finding data for: ' + word.upper())
    url = "http://etymologiebank.ivdnt.org/trefwoord/" + word
    driver.get(url) # Opens link in the remote driver
    time.sleep(2) # Page needs some time to load properly
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')    
    divlist = soup.findAll('div', {'class':'wordContent'})  # The HTML code of the website is scanned for a <div class='wordcontent'> element, 
                                                            # which this site only uses for definitions.
    for entry in divlist:
        entry_stripped = entry.text.strip().lower() # .strip() removes the html tags, leaving just the definition
        if english in entry_stripped:
            engelsseen = engels_seen + 1 
            if engels_seen == 3: # Words are only written to the csv file if they include the word 'English' at least 3 times.
                checked_loanwords.append(word)
                print (word.upper() + ' is indeed an English loanword! \n')
                with open('loanwordschecked.csv', 'w') as output: # Words that pass the check are appended to a csv file
                    write = csv.writer(output, lineterminator='\n')
                    write.writerow([word]) 
                    print(checked_loanwords)

#
# PART 3.2: CHECKING THE ETYMOLOGIES OF THE LOAN WORD LIST WITH THE AMSTERDAM UNIVERSITY PRESS ETYMOLOGY DICTIONARY
#

print('== CHECKING ETYMOLOGIES OF LOANWORD LIST WITH UAP ETYMOLOGY DICTIONARY == \n')

checked_loanwords = []
english = 'engels'

with open('words_similar.csv','r') as file:
    loanwords = file.readlines()

#C hromedriver accesses Google Chrome remotely, allowing for automated website searches.
chromedriver_path= "PATH/chromedriver"
driver = webdriver.Chrome(executable_path=chromedriver_path)

for word in loanwords:
    # Opens homepage of etymology website
    url = "http://www.etymologie.nl"
    driver.get(url)
    time.sleep(2) # Loading the page properly requires a slight delay
    # Code finds the search box in the page 
    driver.switch_to.frame("ewntopFrame") 
    search_box = driver.find_element_by_xpath('//*[@id="q1"]')
    # Word is typed into search bar, and searched
    search_box.send_keys(word)
    time.sleep(1)
    search_box.send_keys(Keys.RETURN)
    # The dictionary entry is on a different frame than the search bar, so the code switches between frames
    driver.switch_to.default_content()
    time.sleep(1)
    driver.switch_to.frame("ewnpage")
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    dictionary_entries = soup.findAll('span',{'class':'resultaat'}) # The HTML code of the website is scanned for a <div class='resultaat'> element, 
                                                                    # which this site only uses for definitions.
    for entry in dictionary_entries:
        entry_stripped = entry.text.strip().lower()
        if english in entry_stripped: # Dictionary entry is checked if it contains 'English'. If true, the loanword is appended to the list.
          checked_loanwords.append(word)
          
with open('loanwordscheckedUAP.csv', 'w') as output: # The loanwords are written to a csv file
     write = csv.writer(output, lineterminator='\n')
     for loanword in checked_loanwords:
        write.writerow([loanword])    

#
# PART 4: COMBINE THE WORD LISTS GENERATED BU THE UAP AND ETYMOLOGYBANK
#

total_list = []

print('== COMBINING ETYMOLOGICAL WORDLISTS == \n')
# Read both files
print('Reading etymologiebank loanwords... \n')
with open('loanwordschecked.csv','r') as file1:
    data1 = file1.readlines()
print('Reading UVA etymologie loanwords... \n')
with open('loanwordscheckedUAP.csv','r') as file2:
    data2 = file2.readlines()
print('Adding entries to new list... \n')
# Add entries in files to new list
for file1_data in data1:
    total_list.append(file1_data.strip().lower())
for file2_data in data2:
    if file2_data not in total_list: # Only adds words that are not already in the file
        total_list.append(file2_data.strip().lower())

total_list_sorted = sorted(total_list)

print('Copying entries to new csv file... \n')
# Write complete list of loanwords to new txt file
with open('loanwordschecked_total.csv', 'w') as output: 
    for item in total_list_sorted:
        output.write(item.strip().lower()+'\n')
            
print('== PROGRAM END ==')


