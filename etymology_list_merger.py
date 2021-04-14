total_list = []

print('== PROGRAM START == \n')
# Read both files
print('Reading etymologiebank loanwords... \n')
with open('loanwordschecked.csv','r') as file1:
    data1 = file1.readlines()
print('Reading UVA etymologie loanwords... \n')
with open('loanwordscheckedUVA.csv','r') as file2:
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
with open('loanwordschecked_total.txt', 'w') as output: 
    for item in total_list_sorted:
        output.write(item.strip().lower()+'\n')
            
print('== PROGRAM END ==')




