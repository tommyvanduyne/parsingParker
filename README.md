# Parsing Parker
###Authors: 
Thomas Van Duyne and Allison Tetreault
###Description:
This application prompts the user for three things:

1. The smallest interval set
2. The Largest interval set
3. the input folder 
    - this will default to "CSVs"
It will then intake 10 charlie parker tunes from the input folder
(using glob so that it is not dependent on quanitity of input files)
and run a variety of functions on them to create meaningful data for the user.
It then prints this data out in the 'outputs', 'ngrams', and 'ngramCollective' 
folders as TXT files.

###INPUT:

This application takes in whatever CSV files are present in the given input folder (defaults to 'CSVs')
and scrapes them for meaningful data to manipulate and print out.

###OUTPUTS:

####FOLDERS:

1. outputs
    - In this folder, the user will find the outputted files comparing the relative frequency 
    of each ngram in the users chosen range.  If the user choose 3 as their smallest
    interval set and 7 as their largest, a file called "results3_7.txt" will be created
    here that displays the frequencies of all 3-grams, 4-grams, 5-grams, 6-grams, and 7-grams
    in a table organized by frequency (higher frequency at the top)
2. ngrams
    - In this folder, the user will find the outputted files of each song for each ngram. Each one
    of these files contains a string of ngrams separated by a space so if the user so chooses, they
    could use this file to create a meaning representation for the intervals in this song via a ngram
    displayer or something else.
3. ngramCollective
    - In this folder, the user will find a single folder that contains all the ngrams from all the songs
    in a single file.  It gets updated each time the user runs the program and reflects the chosen 
    interval sets.

Date last modified: 3/21/2015


