with open('ground_truth.txt', 'r') as file:
  filedata = file.read()

# Replace the target string
filedata = filedata.replace('.txt', '.json')

# Write the file out again
with open('file2.txt', 'w') as file:
  file.write(filedata)