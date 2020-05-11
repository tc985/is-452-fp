# bookstats.py
#   this program pulls select data from plaintext books and writes it out to a csv

import sys
import string
import re
import csv

# removes project gutenberg metadata and extra text from the front and end of plaintext book
# returns gutenberg-less lowercase text
def death_to_johannes(text):
    text_parts = text.lower().split('\n\n\n\nchapter') # splits by chapter

    if len(text_parts) > 1:
        cut_point = text_parts[-1].find('end of the project gutenberg')
        if cut_point == -1:
            cut_point = text_parts[-1].find('end of project gutenberg')
        text_parts[-1] = text_parts[-1][:cut_point]
        del text_parts[0]  # kills everything before the first chapter

        # this section removes the line with any leftover chapter heading text from each index in the list by splitting by \n
        count = 0
        for part in text_parts:
            text_parts[count] = '\n'.join(text_parts[count].split('\n')[2:]) # joins while killing the "chapter" lines
            count += 1

        new_text = '\n'.join(text_parts) # so we have something to return

    else:
        new_text = 'ERROR' # in case there are no chapter headings, or formatting incompatible

    return new_text

# replaces smart quotes with dumb quotes and removes all other punctuation
def clean_punc(text):
    text = text.replace('“', '"').replace('”', '"') # converts smart quotes to regular

    cleanline = text
    for punc in string.punctuation:
        if punc != '"':
            cleanline = cleanline.replace(punc, ' ')
    return cleanline

# returns length of dialogue by splitting the text by "
def dialogue_length(text):
    total_length = 0
    dia_lst = text.split('"')
    dia_lst_odd = dia_lst[1::2]

    if len(dia_lst) % 2 != 0: # if we don't have an even number of "
        total_length = 'ERROR'

    else:
        for i in dia_lst_odd:
            dia_words = i.split()
            count = len(dia_words)
            total_length = total_length + count

    return total_length

# gets rid of ALL punctuation
def cleaner_punc(text):
    cleanline = text
    for punc in string.punctuation:
        cleanline = cleanline.replace(punc, " ")
    return cleanline

# find longest word and checks to make sure it's real
# returns longest word and its length
# words_alpha.txt from https://github.com/dwyl/english-words
def longest_word(text):
    with open('words_alpha.txt', 'r', encoding = 'utf-8') as f:
        words = [line.strip() for line in f]

    word_dict = {}
    for w in text.split():
        if w not in word_dict:
            word_dict[w] = len(w)

    word_list = list(word_dict.items())
    
    # this runs every word in the book (collected in dict) against all the
    # "real words" in words_alpha (it's less efficient than I'd like)
    word_order = []
    for tuple in word_list:
        if tuple[0] in words:
            word_order.append(tuple)

    word_order.sort(key = lambda a:a[1], reverse = True)

    word = word_order[0][0]
    length = word_order[0][1]

    return length, word

# returns the most used word and how many times it appears
def most_used(text):
    word_dict = {}
    for i in text.split():
        if i in word_dict:
            word_dict[i] += 1
        else:
            word_dict[i] = 1
    word_list = list(word_dict.items())
    word_list.sort(key = lambda a:a[1], reverse=True)

    top_word = word_list[0][0]
    top_times = word_list[0][1]

    return top_word, top_times

# returns average words per paragraph
def para_size(text):
    para_lst = text.split('\n\n')
    avg_wpp = len(text.split())/len(para_lst)
    return avg_wpp

# returns title and author of book
def t_and_a(text):
    title_re = re.compile('Title: [A-Z][A-Za-z ’,:-]+')
    title = re.findall(title_re, text)

    author_re = re.compile('Author: [A-Z][A-Za-z ’,:-]+')
    author = re.findall(author_re, text)

    final_t = title[0][7:]
    final_a = author[0][8:]

    return final_t, final_a

# returns average word length in characters and the total characters in the book
def avg_word_len(text):
    num_of_words = len(text.split())
    no_spaces = re.sub(r'\s+', '', text)
    full_len = len(no_spaces)
    word_len = full_len / num_of_words

    return word_len, full_len

def main():
    dict_of_power = {}

    print('This program reads one or more plaintext Project Gutenberg books from .txt files and selects')
    print('statistics about the text. It reads out the statistics to a .csv file.')
    print()

    exit_code = 0
    while exit_code != 1:
        try:
            stupid_value = 1 # will be used to intentionally cause a DivideByZeroError later to esc a loop
            file_name = str(input('Enter the filename: '))
            with open(file_name, 'r', encoding = 'utf-8') as f:
                text = f.read()
            # text_test will determine if the file will read or not
            text_test = death_to_johannes(text) # we're now free of gutenberg stuff and all lower case, no chapters
            if text_test == 'ERROR': #if johannes returns 'error', we can't work with the file, loop back to beginning or exit
                print('This file cannot be evaluated with this program, sorry.')
                y_or_n = input(str('Do you want to try a different file? (y/n): '))
                while True:
                    if y_or_n == 'n':
                        q_dis = input("Do you want to quit or continue? \nQuitting will lose what you currently have. Continuing will export it. (q/c): ")
                        if q_dis == 'q':
                            print('Goodbye!')
                            sys.exit()
                        elif q_dis != 'c':
                            print('You did not enter "q" or "c". Please try again.')
                        else:
                            stupid_value = 0 # will cause an error later so we exit the try to an except
                            break
                    elif y_or_n != 'y':
                        print('You did not enter "y" or "n". Try again.')
                    else:
                        break
            # this will run if you don't quit the program above, it will take the file you entered even if it won't work
            # but that will cause an error which will be caught be an except and restart at the first while loop
            try:
                y = 1 / stupid_value # this will force an error to exit the try if 'c' was chosen in the quit/cont if
                text2 = death_to_johannes(text) # we couldn't define this in all the mess above, just filter for it
                text3 = clean_punc(text2) # now we have gutenberg free, punc free text, with non-smart " retained
                text4 = cleaner_punc(text3) # now the " are gone
                
                # this will return an IndexError if the infile can't be read through the johannes properly
                # it will only occur if 'y' to try a new file with a non-working file already in
                word_len, word = longest_word(text4) 
                wpp = para_size(text4)
                dialogue = dialogue_length(text3) # we go back to text 3 so that we can have "s still to split by
                if dialogue != 'ERROR':
                    dialogue_ratio = dialogue / len(text4.split())
                else:
                    print('Note -- We could not obtain a dialogue ratio for you. That value will display blank.')
                    dialogue_ratio = ''

                top_word, top_times = most_used(text4)
                title, author = t_and_a(text) # use text so we still have gutenberg stuff to search
                avg_len, length = avg_word_len(text4) # the length var won't include punctuation characters

                list_of_might = [title, author, top_word, top_times, word, word_len, dialogue_ratio, wpp, avg_len, length,]
                dict_of_power.update({str(title) : list_of_might})

                print("We've finished evaluating and are ready to export your results.")
                while True:
                    decision = input("Do you want to add another book to the evaluation or export what you have? (add/export): ")
                    if decision == 'add':
                        break
                    elif decision == 'export':
                        exit_code = 1

                        the_list_to_end_all_lists = list(dict_of_power.items())

                        outfile_name = str(input('Enter a name for your csv file. (Do not include ".csv".): '))
                        outfile = open(outfile_name + '.csv', 'w', encoding = 'utf-8', newline = '')
                        csvout = csv.writer(outfile)

                        csvout.writerow(['title', 'author', 'most-used word', 'times used', 'longest word', 'lw length', 'dialogue ratio', 'words per para', 'avg word len', 'total characters'])

                        for i in the_list_to_end_all_lists:
                            r1 = i[1][0]
                            r2 = i[1][1]
                            r3 = i[1][2]
                            r4 = i[1][3]
                            r5 = i[1][4]
                            r6 = i[1][5]
                            r7 = i[1][6]
                            r8 = i[1][7]
                            r9 = i[1][8]
                            r10 = i[1][9]

                            row = [r1, r2, r3, r4, r5, r6, r7, r8, r9, r10]
                            csvout.writerow(row)
                        break
                    else:
                        print('You did not enter "add" or "export". Try again.')
            # this will loop back to the beginning of the first while loop to re-enter a new file
            except IndexError:
                print("Then let's take it from the top.")

            #this section will run if you answer 'n' to try another file, but 'c' to quit or continue
            except ZeroDivisionError:
                print("Then let's export your file.")
                exit_code = 1

                # i just copied the code from earlier, which is a silly duplication of effort, but i was having
                # a hard time wrapping my head around making this a function so I wouldn't have to
                the_list_to_end_all_lists = list(dict_of_power.items())

                outfile_name = str(input('Enter a name for your csv file. (Do not include ".csv".): '))
                outfile = open(outfile_name + '.csv', 'w', encoding = 'utf-8', newline = '')
                csvout = csv.writer(outfile)

                csvout.writerow(['title', 'author', 'most-used word', 'times used', 'longest word', 'lw length', 'dialogue ratio', 'words per para', 'avg word len', 'total characters'])

                for i in the_list_to_end_all_lists:
                    r1 = i[1][0]
                    r2 = i[1][1]
                    r3 = i[1][2]
                    r4 = i[1][3]
                    r5 = i[1][4]
                    r6 = i[1][5]
                    r7 = i[1][6]
                    r8 = i[1][7]
                    r9 = i[1][8]
                    r10 = i[1][9]

                    row = [r1, r2, r3, r4, r5, r6, r7, r8, r9, r10]
                    csvout.writerow(row)
        # if you didn't enter a workable filename
        except FileNotFoundError:
            print('We could not find a file with that name. Check the exact address and try again.')

main()
