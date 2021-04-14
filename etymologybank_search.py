# This section imports various libraries used in the code.
import time # Allows adding delays to script
from bs4 import BeautifulSoup # Allows script to read and identify HTML elements
from selenium import webdriver # Allows script to run Chrome remotely
import csv # Allows script to write lists to csv files

divstrip = []
checked_loanwords = []
datastrip = []

# This opens the file created by the previous code (see figure 1).
with open('similar_words.txt','r') as input:
    data = input.readlines()
    
# All data is stripped and lowercase to be consistent throughout the code.
for entry in data:
    datastrip.append(entry.strip().lower())

print('== PROGRAM START == \n')

# Chromedriver accesses Google Chrome remotely, allowing for automated website searches.
chromedriver_path= "/PATH/chromedriver"
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

    
print ('== PROGRAM END ==')



