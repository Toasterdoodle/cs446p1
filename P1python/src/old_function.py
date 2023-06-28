# for line in toRead:
#         # print('NEW LINE:')
#         # print(line)

#         # simple tokenize method using spaces
#         if tokenize_type == "spaces":
#             temp = line.split()
#         # print(temp)

#         # advanced tokenize method as described in the assignment
#         else:
#             # first split the line using spaces again
#             temp = line.split()
#             temp2 = []

#             # need to apply special rules for each word in the line
#             for e in temp:
#                 temp2.append(fancyTokenize(e))
            
#             temp = temp2
        
#         # at this point, temp is a list of tokens generated from the line we have just read

#         # sorting through the words after we have split
#         # if stopping is turned on (stopList=”yesStop”), then only certain words should make it into words
#         # otherwise, all words can make it in
#         if stoplist_type == 'yesStop':
#             temp = list(filter(lambda e: e not in stopword_lst, temp))

#         # now we need to begin the stemming process
#         if stemming_type == "porterStem":
#             for i in range(len(temp)):
#                 temp[i] = porterStem(temp[i])
        
#         # now finally, we can append all the words in temp to word
#         for e in temp:
#             words.append(e)

#     print(words)