# This section imports various libraries used in the code.
import time # Allows adding delays to script
from bs4 import BeautifulSoup # Allows script to read and identify HTML elements
from selenium import webdriver # Allows script to run Chrome remotely
from selenium.webdriver.common.keys import Keys # Allows script to use keys in remotely ran Chrome
import csv # Allows script to write lists to csv files

checked_loanwords = []
english = 'engels'

with open('similar_words.txt','r') as file:
    loanwords = file.readlines()

#C hromedriver accesses Google Chrome remotely, allowing for automated website searches.
chromedriver_path= "/Users/Maryn/Library/Mobile Documents/com~apple~CloudDocs/iMac/Arts and Sciences BASc/BASC0003/Project/chromedriver"
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
          
with open('loanwordscheckedUVA.csv', 'w') as output: # The loanwords are written to a csv file
     write = csv.writer(output, lineterminator='\n')
     for loanword in checked_loanwords:
        write.writerow([loanword])    

