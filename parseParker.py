'''
APP: Parse Parker
AUTHORS:
Thomas Van Duyne - Wrote the software
Allison Tetreault - Authored the research report

DESCRIPTION:
This application prompts the user for three things:
(i) The smallest interval set
(ii) The Largest interval set
(iii) the input folder 
    - this will default to "CSVs"
It will then intake 10 charlie parker tunes from the input folder
(using glob so that it is not dependent on quanitity of input files)
and run a variety of functions on them to create meaningful data for the user.
It then prints this data out in the 'outputs', 'ngrams', and 'results' 
folders as TXT files.

INPUT:
This application takes in whatever CSV files are present in the given input folder (defaults to 'CSVs')
and scrapes them for meaningful data to manipulate and print out.

OUTPUTS:
    FOLDERS:
    (i)'outputs'
        -In this folder, the user will find the outputted files comparing the relative frequency 
        of each ngram in the users chosen range.  If the user choose 3 as their smallest
        interval set and 7 as their largest, a file called "results3_7.txt" will be created
        here that displays the frequencies of all 3-grams, 4-grams, 5-grams, 6-grams, and 7-grams
        in a table organized by frequency (higher frequency at the top)
    (ii)'ngrams'
        -In this folder, the user will find the outputted files of each song for each ngram. Each one
        of these files contains a string of ngrams separated by a space so if the user so chooses, they
        could use this file to create a meaning representation for the intervals in this song via a ngram
        displayer or something else.
    (iii)'results'
        -In this folder, the user will find a single folder that contains all the ngrams from all the songs
        in a single file.  It gets updated each time the user runs the program and reflects the chosen 
        interval sets.

Date last modified: 4/29/2014
'''
import glob
import os
def main():
    #global variable declaration
    output_folder = "outputs"
    collective_output = "results"
    ngram_folder = "ngrams"
    input_folder = "CSVs"
    fileNames = glob.glob(input_folder+"/*")
    start_spot = 1 #default value
    end_spot = 1 #default value

    #Prompt user for some specifications
    start_spot = ''
    end_spot = ''
    input_folder = ''
    
    #get start_spot
    while type(start_spot) is not int:
        try:
            start_spot = input("Smallest interval set?:\t")
            if not start_spot:
                raise ValueError('empty string')
            elif not is_int(start_spot):
                print ("Please input an integer...")
            elif int(start_spot) <= 0:
                print ("Smallest interval must be greater than 0")
            else:
                start_spot = int(start_spot)
        except ValueError as e:
            print (e)

    #get end_spot
    while type(end_spot) is not int:
        try:
            end_spot = input("Largest interval set?:\t")
            if not end_spot:
                raise ValueError('empty string')
            if not is_int(end_spot):
                print ("Please input an integer...")
            elif start_spot > int(end_spot):
                print ("Please input an integer great than previous input")
            else:
                end_spot = int(end_spot)
        except ValueError as e:
            print (e)
    
    #get input folder
    while not os.path.isdir(input_folder):
        try:
            input_folder = input("Input Folder (defaults to 'CSVs')?:\t")
            if input_folder == "":
                input_folder = "CSVs"
            elif not os.path.isdir(input_folder):
                print ("Folder does not exist")
        except ValueError as e:
            print (e)
    
    #Dictionary used later for all the interval sets {}
    wordDictionary = {}
    #etc...
    ngramList = []
    #CALL FUNCTIONS
    for fileName in fileNames:
        fileName.replace("CSVs","")
        print ("Checking: "+fileName)
        noteList = []
        intervalList = []

        #get notes from csv files
        getNotes(noteList,fileName,input_folder)

        #create list of intervals
        getIntervals(noteList,intervalList)

        #get fileWrite ready to write
        fileWrite = ngram_folder+"/"+fileName.replace(".csv","_ngram")
        fileWrite = fileWrite.replace("CSVs/","")
        print ("Writing to: "+fileWrite+".txt")

        #create ngram data
        n_gram_creator(intervalList,ngramList,output_folder,fileWrite,start_spot, end_spot)
    
    #Grabs ngramList to make a dictionary    
    crunchTheNumbers(wordDictionary,ngramList)

    #prints the dictionary into new file
    printDictionary(wordDictionary,output_folder,start_spot,end_spot)

    printNgramList(ngramList,collective_output)
#end of main()

#-----------------------------------------------------#
# printNgramList() - prints the ngrams out            # 
# for the user in a file called results.txt.  This    #
# file can hopefully be used by the user to create    #
# interesting representations of the data.  It        #
# contains all the ngrams in all the csv files of the #
# lengths specified by the user                       #
#-----------------------------------------------------#
def printNgramList(ngramList,collective_output):
    OUTPUT = open(collective_output+"/"+"results.txt",'w')
    for gram in ngramList:
        OUTPUT.write(gram+"\n")
    print("writing to "+collective_output+"/"+"results.txt")
    OUTPUT.close()
#end of printNgramList

#---------------------------------------------------------------------#
# printDictionary() - compares the frequency  of the ngrams           #
# between the lengths given by the user  and then                     #
# prints them out for the user in one file dynamically named          #
# based on the length of the ngrams being compared. For example,      #
# if the user was to enter 3 for the smallest interval set            #
# and 7 for the largest interval set, the file created would compare  #
# all interval sets from 3-7 and created a file called                #
# results3_7.txt in the folder 'outputs' to print the results         #
#---------------------------------------------------------------------#
def printDictionary(wordDictionary,output_folder,start_spot,end_spot):
    OUTPUT = open(output_folder+'/'+'results'+str(start_spot)+'_'+str(end_spot)+'.txt', 'w')
    for word in sorted(wordDictionary, key=wordDictionary.get, reverse=True):
        OUTPUT.write(str(wordDictionary[word])+"\t"+ word+"\n")
    print("writing to "+output_folder+'/'+'results'+str(start_spot)+'_'+str(end_spot)+'.txt')
    OUTPUT.close()
    
#end of printDictionary()

#------------------------------------------------------------#
# crunchTheNumbers() - This function accepts a dictionary    #  
# and a list as inputs.  The list is a list of ngrams.       #
# These ngrams are then counted, and stored into the passed  #
# dictionary: The ngram itself is the key, and its frequency #
# is the value.                                              #
#------------------------------------------------------------#
def crunchTheNumbers(wordDictionary,ngramList):
    for gram in ngramList:
        if gram in wordDictionary:
            wordDictionary[gram]+=1
        else:
            wordDictionary[gram] = 1
    #end for loop
#end of crunchTheNumbers()

#-----------------------------------------------------------------------------#
# n_gram_creator() - This function takes in a list of intervals               #
# and, based on a users smallest and largest interval sets, creates ngrams of #
# length start_spot to length end_spot and prints them out                    #
# into documents in the ngrams folder. It also adds the ngrams to             #
# a list that can be used in later functions to determine most                #
# common ngrams                                                               #
#-----------------------------------------------------------------------------#
def n_gram_creator(intervalList,ngramList,output_folder,fileWrite,start_spot, end_spot):
    notesSharp = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
    notesFlat = ["C","Db","D","Eb","E","F","Gb","G","Ab","A","Bb","B"]
    for n in range(start_spot,end_spot+1):
        OUTPUT = open(fileWrite+str(n)+".txt", 'w')
        i = 0
    	#write into file with numbers
        while (i < len(intervalList)-(n-1)-1):
            ngram_stringINTERVALS = ""
            for number in range(n):
                ngram_stringINTERVALS += str(intervalList[i+number])+','     
            start = 0
            ngram_stringNOTES = "C ";
            for number in range(n):
                #ngram_string = ngram_string+str(intervalList[i+number])+','     
                interval = intervalList[i+number]
                operator = interval[0]
                trueInterval = interval[1:] 
                if operator == '+': 
                    start = start + int(trueInterval)
                elif operator == '-': 
                    start = start - int(trueInterval) 
                else: # is 0
                    operator = ''
                    start = start
                newLetter = notesSharp[start%12]  
                ngram_stringNOTES += (operator + newLetter + ' ')
            #print(ngram_stringINTERVALS + " ")
            #print(ngram_stringNOTES + "\n")
            OUTPUT.write(ngram_stringNOTES+" ")
            ngramList.append(ngram_stringNOTES)
            i+=1
        OUTPUT.close()
    #end of for loops
#end of n_gram_creator()

#------------------------------------------------------------------------#
# getNotes() - This function dives into the csv files in                 #
# the input folder (which will default to 'CSVs') and grabs the notes    #
# (which are currently midi values from 1-127).  It then stores these    #
# values in a list called noteList                                       # 
#------------------------------------------------------------------------#
def getNotes(noteList,fileName,input_folder):
    INPUT = open(fileName, 'r')
    #remove meaningless file lines
    for i in range(15):
        INPUT.readline()
    count = 0
    #Begin Meaningful Loop    
    for line in INPUT:
        #Make sure we dont doublre up on notes from note_on and note_off in file
        if count%2 == 0:
            count+=1
            continue
        #create list of values from CSV file
        daList = line.split()
        #make sure that daList is not at the eof
        if len(daList)>=5:
            #Write to file
            noteList.append(daList[4].replace(',',''))
        else:
            break
        count+=1
    #for note in noteList:
     #   print(note)
    INPUT.close()
#end of getNotes()

#---------------------------------------------------------#
# getIntervals() - This function continues on from what   #
# getNotes() does, in that it takes the list of notes     #
# (noteList) and creates a list of intervals. The list of #
# intervals is key-independent, creating useful data for  #
# analysis                                                #
#---------------------------------------------------------#
def getIntervals(noteList,intervalList):
    previousNote = "stand-in string"
    for note in noteList:
        if previousNote == "stand-in string":
            previousNote = note
            continue
        interval = int(note)-int(previousNote)
        #Use M to denote upward interval and m to denote downward interval.
        if interval > 0:
            interval = "+"+str(interval)
        else:
            interval = str(interval).replace("-","-")
        intervalList.append(interval)
        previousNote = note
#end of getIntervals()

def is_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    main()
