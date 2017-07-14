'''
Takes a list of incorrect phrases and produces an output of possible suggestions from Google.
This output could be applied to PATTY data set to fix malformed phrases, 
the script could be extended to apply directly the suggestions to PATTY data set.
'''

from urllib import urlopen
import re

url = "http://google.com/complete/search?output=toolbar&q="

output_file = open("patty_buggy_clean.txt","w") 

# read list of words from file

with open("patty_buggy.txt", "r") as file :
    for phrase in file: 
        
        print "-------"
        
        webpage = urlopen(url + phrase).read()
    
        suggestions = re.findall(r'data="(\w*\s*\w*\s*\w*\s*)"', webpage)

        # take the first suggestion
        
        if suggestions :
            print phrase +" -> "+ suggestions[0]
            output_file.write(suggestions[0]+"\n")
        else :
            print "No suggestions"
            
        print "--------"

output_file.close() 



