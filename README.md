# extractmemos.py
This script extracts text from .memo files created by the default Memo app on Verizon Samsung Galaxy S phones. No root access required. Share a memo files to a directory on your pc via Bluetooth or USB and run this script against that directory.

## About
I wrote this script to enable storing and reading memos offline on a PC _without_ the need for cloud storage or email transfer. I’ve tested this script for notes created with the default (stock) Samsung Galaxy S6 Memo app that comes preinstalled on Verizon phones. The Memo app I’m referring to is _not_ the "S Memo" app. This script presumably works with other phones that have the same memo app, but I have not tested it.

![alt text](https://github.com/domenicbrosh/extractmemos.py/blob/master/img/memo_icon.png "current icon for the default Memo app")

The image above is the current icon for the default Memo app I am referring to.

These memos, when shared to a PC via Bluetooth or USB, yield an archive with a .memo extension. Changing the file extension to .zip will allow the archive to be decompressed using most zip utilities. However, this can be a chore when multiple files need to be extracted. This script helps automate that process.

## Usage

The only requirement is that you have [Python 2 or 3](https://www.python.org/downloads/) installed on your PC. Run this script and add the path to a directory containing the memo file(s) as an argument:

	python extractMemos.py [source] [target_directory]

Parsing multiple memo files creates one contiguous output with a message appended to the end of each memo listed.

You may change the number of words per line in the extracted file by changing the variable 'word_per_seperator' in extractmemos.py. It is located near the top of the file.
If you would like to leave the memo content unchanged, leave the variable as None.

## Examples

These examples were written to be N00B friendly. Command line ninjas may skip this section.

The following examples assume your memo files are located on your **Desktop** in a folder named **Memos** and that this script is located in your **Documents** folder. Taylor these commands to your environment by replacing the example paths with paths that reflect where your files are located and replace any instance of `username` with your _actual_ username. Your username can be found by typing `whoami` and pressing enter.

##### Change the working directory path to the desktop:

	cd /Users/username/Desktop

##### Example 1 (Given a particular memo):

	python /Users/username/Documents/extractMemos.py ./Memos/filename.memo


##### Example 2 (Given a directory of memos):

	python /Users/username/Documents/extractMemos.py ./Memos


##### Example 3 (Given a directory or memos and a target directory):

	python /Users/username/Documents/extractmemos.py ./Memos ./TargetName


## Caveats and Warnings
This script relies on Python's XML Processing Modules and is therefore _not_ secure against maliciously constructed data. I highly recommend using this script to only parse data that you have created on your own device. For more information see:
  * https://docs.python.org/2/library/xml.html#xml-vulnerabilities
  * https://docs.python.org/3/library/xml.html

## TODO

* Add functionality for extracting images
* Error handling
* Improve Regex
* Cleanup functions
