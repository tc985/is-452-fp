# BOOKSTATS
Final python programming project for IS 452 at Univerisity of Illinois - Urbana Champaign, Spring 2020.

A program to gather statistics from the text of plaintext novels from Project Gutenberg.

## Prerequisites

You will need to have Python 3 installed on your computer.

## Installing

No crazy installation here. Just download the files and make sure you have bookstats.py and words_alpha.txt in the same directory.

## What this program CAN'T do

Unfortunately this program cannot currently read EVERY book available on Project Gutenberg. Books without traditional chapter headings (think plays, poems, ect.) won't work. Also some oddball formatting choices can also make the file unreadble to our program. The program will let you know immediately if the file won't work and will give you the option to quit or try a differnet file.

Also remember that this is just for plaintext books. UTF-8 will work best.

## How to Use

Run bookstats.py in whatever Python shell is most comfortable for you. The command line (Windows) or terminal (Mac) will work just fine.

It is easiest to move all of the .txt files you want to parse through to the same directory as the bookstats.py file. Then there is no need to type a long directory address. yourfile.txt will work just fine.

When prompted enter the filename do so and continue to enter files as prompted until you wish to export your results. When prompted to enter a name for you csv file pick a unique name and you'll have your data ready.

## Authors

* **Tommy Crawford** - *Initial work* - [tc985](https://github.com/tc985)

## Acknowledgments

* Elizabeth Wickes at UIUC for instrcution, tips, the clean_punc function, and generally being cool
* [dwyl](https://github.com/dwyl) on GitHub for the list of English words used 
* [PurpleBooth](https://gist.github.com/PurpleBooth) on GitHub for the template for this README 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
