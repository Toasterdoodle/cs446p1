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

print(porterStem('stresses'))
print(porterStem('ties'))
print(porterStem('cries'))
print(porterStem('stress'))
print(porterStem('gaps'))
print(porterStem('gas'))
print(porterStem('feed'))
print(porterStem('agreed'))
print(porterStem('fished'))
print(porterStem('pirating'))
print(porterStem('falling'))
print(porterStem('dripping'))
print(porterStem('hoping'))
print(porterStem('cry'))
print(porterStem('by'))
print(porterStem('say'))
print(porterStem('described'))
print(porterStem('rules'))