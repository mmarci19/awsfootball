# writing to file
file1 = open('TeamNames.csv', 'r')

Lines = file1.readlines()
  
count = 0
# Strips the newline character
file2 = open('out2.txt', 'w')
for line in Lines:
    vv = line.split(",")[1]
    strng = "<option>" +  vv +"</option>"
      
    file2.write(strng)
