print('== PROGRAM START == \n')
# The dictionary files are read and added to lists
print('Reading file 1... \n')
with open('scrapedwords_nl.txt','r') as file1:
    data1 = file1.readlines()
print('Reading file 2... \n')
with open('words_uk.txt','r') as file2:
    data2 = file2.readlines()
# A new file is created and written in
print('Writing matching entries to new file... \n')
with open('words_similar.txt', 'w') as output:
    # This loop compares entries between the files
    for file1_data in data1:
        for file2_data in data2:
            # Find matching entries, taking into account capitalisation and spacing differences.
            if file1_data.strip().lower() == file2_data.strip().lower():
                # Write identical entries into a new txt file
                output.write(file2_data.strip()+'\n')
print('== PROGRAM END ==')


