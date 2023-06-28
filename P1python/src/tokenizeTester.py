import re

# Below is stopword list
stopword_lst = stopword_lst = ["a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
                "has", "he", "in", "is", "it", "its", "of", "on", "that", "the", "to",
                "was", "were", "with"]

# converting the list into a set for faster lookup time
stopword_lst = set(stopword_lst)

# list to keep track of all the words (tokens) while we are tokenizing
words = []

# list to keep track of all punctuation
punctuation = [".", ",", ")", "(", "'", ]
punctuation = set(punctuation)

# list to keep track of all letters
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
letters = set(letters)

# list to keep track of numerics
numerics = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '.', '-', ',']
numerics = set(numerics)

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

print(fancyTokenize('Token'))
print(fancyTokenize("She's"))
print(fancyTokenize("Mother's-IN-Law"))
print(fancyTokenize('U.mass'))
print(fancyTokenize('go!!!!team'))
print(fancyTokenize('USD$10.30'))
print(fancyTokenize('USD$10,30'))
print(fancyTokenize('USD$10-30'))
print(fancyTokenize('B.C.,'))

# Token → token (lower case rule)
# She’s → shes (apostrophe rule and lower case rule)
# Mother’s-IN-Law → mothers, in, law, mothersinlaw (apostrophe, lowercase, hyphens)
# U.mass → umass (lowercase, abbreviation)
# go!!!!team → go team (non-period punctuation rule)
# USD$10.30 → usd 10.30 (non-period punctuation, case, number)
# USD$10,30 → usd 10 30 (not period punctuation, case)
# USD$10-30 → usd 10 30 usd 1030 (yes, two occurrences of “usd” from the hyphen rule)