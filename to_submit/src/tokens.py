import gzip
import re
import sys

# TODO:
# determine whether stopwords are case sensitive or not
# if it is, we need to modify our algorithm to only append if the case sensitive matches the stopword

# Your function start here

if __name__ == '__main__':
    # Read arguments from command line; or use sane defaults for IDE.
    argv_len = len(sys.argv)
    inputFile = sys.argv[1] if argv_len >= 2 else "P1-train.gz"
    outputFilePrefix = sys.argv[2] if argv_len >= 3 else "outPrefix"
    tokenize_type = sys.argv[3] if argv_len >= 4 else "spaces"
    stoplist_type = sys.argv[4] if argv_len >= 5 else "yesStop"
    stemming_type = sys.argv[5] if argv_len >= 6 else "porterStem"

    # Below is stopword list
    stopword_lst = stopword_lst = ["a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
                    "has", "he", "in", "is", "it", "its", "of", "on", "that", "the", "to",
                    "was", "were", "with"]
    
    # converting the list into a set for faster lookup time
    stopword_lst = set(stopword_lst)
    
    # open file using python tools
    toRead = gzip.open(inputFile, 'rt')

    #----------------- BEGINNING OF FANCY TOKENIZER IMPLEMENTATION --------------------

    # function takes in a word, and runs the fancy tokenize on it
    # should return a list of strings
    def fancyTokenize(word: str) -> str:
        # print('Tokenizing Word:', word)
        toReturn = []

        # list to keep track of all punctuation
        punctuation = {".", ",", ")", "(", "'"}

        # list to keep track of all letters
        letters = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'}

        # list to keep track of numerics
        numerics = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '.', '-', ','}

        # if the word is a URL:
        if len(word) >= 7 and word[:7] == "http://":
            # print('Word is URL')
            # we need to remove all punctuation from after it
            # while the last letter is some sort of punctuation
            while(word[len(word)-1] in punctuation):
                # removing the last letter
                word = word[:len(word)-1]
            toReturn.append(word)
            return toReturn
                
        # another form of URL:
        elif len(word) >= 8 and word[:8] == "https://":
            # print('Word is URL')
            while(word[len(word)-1] in punctuation):
                word = word[:len(word)-1]
            toReturn.append(word)
            return toReturn

        # if the word is not a URL
        else:
            # print('Word is not URL')
            # need to convert the word to lowercase
            word = word.lower()

            # check to see if the word is a numeric word
            isNumeric = True
            for e in word:
                if e not in numerics:
                    isNumeric = False
            
            # if the word is a numeric, we want to return it without doing anything further
            if isNumeric:
                # print('Word is Numeric')
                toReturn.append(word)
                return toReturn
            
            # if this word contains letters (is a word of some sort), we will need to do further processing
            else:
                # print('Word is not Numeric')

                # squeezing out apostrophes:
                # print('Squeezing Apostrophes...')
                j = 0
                while j < len(word):
                    if word[j] == "'":
                        # skipping j since j is an '
                        word = word[:j] + word[j+1:]
                    else:
                        j = j + 1

                # print('Checking for abbreviations...')
                # for abbreviations (words containing only periods and letters) after all apostrophes have been removed:
                abbreviation = True
                for j in range(len(word)):
                    if word[j] not in letters and word[j] != '.':
                        # print('Word is not an abbreviation')
                        abbreviation = False
                        

                # if this word is an abbreviation
                if abbreviation:
                    # print('Word is an abbreviation')
                    # we want to get rid of all the periods
                    j = 0
                    while j < len(word):
                        if word[j] == ".":
                            word = word[:j] + word[j+1:]
                        else:
                            j = j + 1

                # print('Checking for hyphenated words...')
                # checking if the word is a hyphenated word:
                tempWords = word.split('-')

                # if tempWords has more than one item
                # that means that this is a hyphenated word
                if len(tempWords) > 1:

                    # print('Hyphenated words detected.')

                    # adding the concatenation of all previous item to tempWords
                    tempWords.append(''.join(tempWords))

                    for e in tempWords:
                        # we want to re-run our algorithm on the newly generated words
                        # and then append that onto our toReturn
                        # print('Running recursive function...')
                        tempList = fancyTokenize(e)
                        for e in tempList:
                            toReturn.append(e)
                    
                    return toReturn
                
                # if tempWords is only one item long, then we don't need to worry

                # splitting for punctuation
                # print('Splitting punctuation...')
                tempWords = re.split('[;:\/,^<>?"=_+!@#$%&*()-]', word)

                # checking for length
                if len(tempWords) > 1:
                    # getting rid of empty strings
                    # print('Removing empty strings...')
                    tempWords = [x for x in tempWords if x != '']
                    # print('new words detected.')
                    # if it is greater than one, we want to recursively run the function on each newly generated word
                    # print('running recursively...')
                    for e in tempWords:
                        tempList = fancyTokenize(e)
                        for e in tempList:
                            toReturn.append(e)
                    return toReturn
                
                # if the length of tempwords is 1 or 0
                return tempWords
            
    #----------------- END OF FANCY TOKENIZER IMPLEMENTATION --------------------

    #--------------- BEGINNING OF PORTER STEMMER IMPLEMENTATION ----------------------

    # takes in a word, and then returns the stemmed version of that word
    def porterStem(word: str) -> str:
        vowels = {'a', 'e', 'i', 'o', 'u', 'y'}
        # Step 1a:
        # Replace sses by ss (e.g., stresses→stress).
        # Replace ied or ies by i if preceded by more than one letter, otherwise by ie (e.g., ties→tie, cries→cri).
        # If the stem ends in us or ss do nothing (e.g., stress→stress).
        # Delete s if the preceding stem part contains a vowel not immediately before the s (e.g., gaps→gap but gas→gas).
        
        # implementing part 1 here:
        # Replace sses by ss (e.g., stresses→stress).
        alreadyStemmed = False
        if len(word) > 4:
            if word[-4:] == 'sses':
                # replacing with ss
                word = word[:-4] + 'ss'
                alreadyStemmed = True
        
        # implementing part 2 here:
        # already stemmed makes sure that we dont run this step if we already ran the previous step
        # Replace ied or ies by i if preceded by more than one letter, otherwise by ie (e.g., ties→tie, cries→cri).
        if not alreadyStemmed:
            if len(word) > 3:
                suffix = word[-3:]
                if suffix == 'ied' or suffix == 'ies':
                    prefix = word[:-3]
                    # if the prefix is only one letter
                    if len(prefix) < 2:
                        word = prefix + 'ie'
                    else:
                        word = prefix + 'i'
                    alreadyStemmed = True
        
        # implementing part 3:
        # If the stem ends in us or ss do nothing (e.g., stress→stress).
        if not alreadyStemmed:
            if len(word) > 2:
                suffix = word[-2:]
                if suffix == 'ss' or suffix == 'us':
                    alreadyStemmed = True

        # implementing part 4
        # Delete s if the preceding stem part contains a vowel not immediately before the s (e.g., gaps→gap but gas→gas).
        if not alreadyStemmed:
            if len(word) > 1:
                # if the last letter is an s
                if word[-1] == 's':
                    # check for a vowel not immediately preceeding the s
                    preceedingVowel = False
                    for i in range(len(word)-2):
                        if word[i] in vowels:
                            preceedingVowel = True
                    if preceedingVowel:
                        # remove the s
                        word = word[:-1]
                        alreadyStemmed = True
        
        # Step 1b:
        # If the stem ends in eed or eedly then if it is in the part of the stem after the first non-vowel following a vowel, replace it by ee (e.g., agreed→agree, feed→feed).
        # If the stem ends in ed, edly, ing, or ingly then if the preceding stem part contains a vowel delete the ending and then also:
        # if the stem now ends in at, bl, or iz add e (e.g., fished → fish, pirating → pirate)
        # or if the stem now ends with a double letter that is one of bb, dd, ff, gg, mm, nn, pp, rr, or tt, remove the last letter (e.g., falling → fall, dripping → drip)
        # or if the stem is now short, add e (e.g., hoping → hope). A stem is short if and only if:
        # it is only a vowel followed by a single consonant (e.g., at or ow (or “or”!) but not be), or
        # It is one or more consonants in a row followed by a single vowel and then followed by only one other consonant other than w and x (e.g., shed, shred, rap, trap, hop, or bid but not box, bow, or beds).

        # changing alreadyStemmed back to false since we are on the second part
        alreadyStemmed = False

        # implementing part 1 of step 1b
        # If the stem ends in eed or eedly:
            # then if it is in the part of the stem after the first non-vowel following a vowel, replace it by ee (e.g., agreed→agree, feed→feed).
        # checking if the word ends in eed here:

        # takes in a word, and checks to see if a non-vowel following a vowel exists
        def helper1b1(s: str) -> str:
            vowelFound = False
            needChange = False
            for i in range(len(s)):
                if s[i] in vowels:
                    vowelFound = True
                else:
                    if vowelFound:
                        needChange = True
            return needChange

        # checking for eed
        if len(word) > 3:
            if word[-3:] == 'eed':
                # print('eed detected')
                # checking to see if we have found the first non-vowel following a vowel
                if helper1b1(word[:-3]):
                    # print('change is needed')
                    word = word[:-3] + 'ee'
                alreadyStemmed = True
        
        # checking for eedly
        if not alreadyStemmed:
            if len(word) > 5:
                if word[-5:] == 'eedly':
                    if helper1b1(word[:-5]):
                        word = word[:-5] + 'ee'
                    alreadyStemmed = True

        # nested helper function
        # takes in a word, and a stemlength, and returns whether or not the word needs to be stemmed
        def helper1(stemLength: int, word: str) -> str:
            for i in range(len(word)-stemLength):
                if word[i] in vowels:
                    return True
            return False
        
        # If the stem ends in ed, edly, ing, or ingly then if the preceding stem part contains a vowel delete the ending and then also:
        if not alreadyStemmed:
            # checking for ed
            edited = False
            if len(word) > 5 and word[-5:] == 'ingly':
                if helper1(5, word):
                    edited = True
                    word = word[:-5]
            elif len(word) > 4 and word[-4:] == 'edly':
                if helper1(4, word):
                    edited = True
                    word = word[:-4]
            elif len(word) > 3 and word[-3:] == 'ing':
                if helper1(3, word):
                    edited = True
                    word = word[:-3]
            elif len(word) > 2 and word[-2:] == 'ed':
                # print('ed detected')
                if helper1(2, word):
                    edited = True
                    word = word[:-2]

            doublesToRemove = {'bb', 'dd', 'ff', 'gg', 'mm', 'nn', 'pp', 'rr', 'tt'}

            if edited:
                alreadyModified = False
                if len(word) > 2:
                    stem = word[-2:]
                    # if the stem now ends in at, bl, or iz add e (e.g., fished → fish, pirating → pirate)
                    if stem == 'at' or stem == 'bl' or stem == 'iz':
                        word = word + 'e'
                        alreadyModified = True
                    # or if the stem now ends with a double letter that is one of bb, dd, ff, gg, mm, nn, pp, rr, or tt, remove the last letter (e.g., falling → fall, dripping → drip)
                    elif stem in doublesToRemove:
                        word = word[:-1]
                        alreadyModified = True

                if not alreadyModified:
                    short = False
                    # checking if the vowel is short
                    # it is only a vowel followed by a single consonant (e.g., at or ow (or “or”!) but not be)
                    if len(word) == 2:
                        if word[0] in vowels and word[1] not in vowels:
                            short = True
                    # It is one or more consonants in a row followed by a single vowel and then followed by only one other consonant other than w and x (e.g., shed, shred, rap, trap, hop, or bid but not box, bow, or beds).
                    # find the first non-consonant
                    if not short:
                        index = 0
                        while index < len(word):
                            if word[index] not in vowels:
                                index = index + 1
                            else:
                                break
                        # now, word[index] should be the first non vowel in word
                        # check to see if the vowel is followed by only one other consonant other than w and x
                        # word has only one letter after word[index]
                        if len(word) == index + 2:
                            if word[index + 1] not in vowels and word[index + 1] != 'w' and word[index + 1] != 'x':
                                short = True
                    # OR if the stem is now short, add e (e.g., hoping→hope)
                    if short:
                        word = word + 'e'
        
        # step 1c: If the stem ends in y and the character before the y is neither a vowel nor the first letter of the word
        if len(word) > 2:
            if word[-1] == 'y':
                if word[-2] not in vowels:
                    # replace the y with an i (e.g., cry→cri, by→by, say→say)
                    word = word[:-1] + 'i'
        
        return word

    #----------------- END OF PORTER STEMMER IMPLEMENTATION --------------------

    #----------------- BEGINNING READING OF GZIP FILE -----------------------

    # tokenlist: a list of lists containing each and every token
    # where the first element of the list is the original token
    # and the second and so on is the tokens generated by fancy tokenize, and then stemmed
    tokenlist = []

    # reading the file line by line
    for line in toRead:
        # print('NEW LINE:')
        # print(line)

        # separate words by spaces
        line = line.split()

        for e in line:
            # initialize an empty list to store our future tokens
            tokenlist.append([e])
            if tokenize_type == "spaces":
                if stoplist_type == "yesStop":
                    if e not in stopword_lst:
                        if stemming_type == "porterStem":
                            # since append always appends on to the end, we can just use len(tokenlist)-1
                            tokenlist[len(tokenlist)-1].append(porterStem(e))
                        else:
                            tokenlist[len(tokenlist)-1].append(e)
                else:
                    if stemming_type == "porterStem":
                        # since append always appends on to the end, we can just use len(tokenlist)-1
                        tokenlist[len(tokenlist)-1].append(porterStem(e))
                    else:
                        tokenlist[len(tokenlist)-1].append(e)
            else:
                e = fancyTokenize(e)
                # now we should have a list of words
                # we want to remove any stop words from this
                if stoplist_type == "yesStop":
                    e = list(filter(lambda x: x not in stopword_lst, e))
                # now we want to porterStem whatever is left
                if stemming_type == "porterStem":
                    for i in range(len(e)):
                        e[i] = porterStem(e[i])
                # now we can append whatever is left in e to our dict
                for f in e:
                    tokenlist[len(tokenlist)-1].append(f)
    
    #----------------- FILE GENERATION -----------------------
    # keeping track of unique tokens
    uniqueTokens = set()
    numUniqueTokens = 0
    # every time we reach count % 10 == 0, we need to generate a line for our heapstext
    count = 0

    file1 = outputFilePrefix + '-tokens.txt'
    tokentext = open(file1, 'w')
    file2 = outputFilePrefix + '-heaps.txt'
    heapstext = open(file2, 'w')
    file3 = outputFilePrefix + '-stats.txt'
    statstext = open(file3, 'w')

    # this chunk of code should take care of tokentext and heapstext at the same time
    # for every element in our dictionary
    # print(tokenlist)
    for e in tokenlist:
        # toWrite symbolizes what to write for tokentext
        toWrite = ''
        toWrite = toWrite + e[0] + ' '
        if len(e) > 1:
            for word in e[1:]:
                # little section to help with our heap section
                count = count + 1
                # counting number of unique tokens
                if word not in uniqueTokens:
                    uniqueTokens.add(word)
                    numUniqueTokens = numUniqueTokens + 1
                # if the count is 10, we need to print to our heapstext
                if count % 10 == 0 and count != 0:
                    heapstext.write(str(count) + ' ' + str(numUniqueTokens) + '\n')
                toWrite = toWrite + word + ' '
        # getting rid of the space at the end
        toWrite = toWrite[:-1]
        # adding a newline to the file
        toWrite = toWrite + '\n'
        tokentext.write(toWrite)
    
    # taking care of the final bit for heapstext
    heapstext.write(str(count) + ' ' + str(numUniqueTokens) + '\n')

    # print(tokenlist)
    # print('####################################')
    
    # now to take care of statstext
    # first we need to count how many of each token there are
    counter = dict()
    for e in tokenlist:
        if len(e) > 1:
            for i in range(1, len(e)):
                if e[i] in counter:
                    counter[e[i]] = counter[e[i]] + 1
                else:
                    counter[e[i]] = 1

    # now we need to convert this counter into a list to be sorted
    countlist = []
    # print(counter)
    for e in counter:
        countlist.append([counter[e], e])
    # sort sorts based off the first element so we have a list sorted from smallest to largest
    countlist = sorted(countlist, key=lambda x: x[1], reverse=True)
    # print(countlist)
    countlist = sorted(countlist, key=lambda x: x[0])
    # print(countlist)
    # print(countlist)
    # now on to the printing
    statstext.write(str(count))
    statstext.write('\n')
    statstext.write(str(numUniqueTokens))
    statstext.write('\n')
    # now we want to print the 100 most common tokens
    reversecount = 0
    index = len(countlist)-1
    # whichever happens first, we either run out of items or we reach 100
    while index >= 0 and reversecount <= 100:
        statstext.write(countlist[index][1] + ' ' + str(countlist[index][0]) + '\n')
        index = index - 1
        reversecount = reversecount + 1