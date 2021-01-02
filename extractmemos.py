'''
   This script extracts text from .memo files created by the default
   Memo app on Samsung (and possibly other) phones and puts the content into
   txt files. Make a directory and put memos via Bluetooth to your PC.
   Then run this script against the directory.

   e.g -> memo_extracter.py [source] [target_directory]

   Updated on: 02 Jan 2021 Daniel Irein 
   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
   WARNING: This script relies on Python's XML Processing Modules and
   is therefore not secure against maliciously constructed data. ONLY
   USE THIS SCRIPT TO PARSE MEMOS THAT YOU HAVE CREATED ON YOUR OWN
   DEVICE. For more information see:
   https://docs.python.org/2/library/xml.html#xml-vulnerabilities
   https://docs.python.org/3/library/xml.html
'''


words_per_seperator = None # The number of words per line
                           # in the main content of a memo.
                           # Feel free to change to a number greater than 0.
                           # Change to None if you want the original
                           # main memo content

import re, zipfile, time, xml.etree.ElementTree as eltree

def parseMemo(memo_file):

   zip_ = zipfile.ZipFile(memo_file, 'r')
   xml_file = zip_.open('memo_content.xml')

   tree = eltree.parse(xml_file)
   root = tree.getroot()

   titleElement = root.find('.//meta[@title]')
   memoTitle = titleElement.attrib.get('title')

   timeElement = root.find('.//meta[@createdTime]')
   timeStamp = timeElement.attrib.get('createdTime')
   memoTime = time.strftime('%x %X', time.localtime(float(timeStamp)/1000))

   contentElement = (root[1][0].text)
   parsedList = (re.split('</p>|<p value="memo2" >', contentElement))
   # <p> tags mark new lines. Remove them from the output
   parsedList = [symbol.replace('<p>', '\n') for symbol in parsedList]
   parsedList = [symbol.replace('&nbsp;', '') for symbol in parsedList]

   out = {}
   out['Title'] = memoTitle
   out['Created'] = memoTime
   out['Content'] = ''.join(parsedList)
   return out


def seperateStr(s, words_per_seperator, seperator='\n'):
   if type(words_per_seperator) not in [int, None]:
      raise TypeError('Expected an integer or None, got {}'.format(words_per_seperator))

   if words_per_seperator < 1:
      raise ValueError('words_per_seperator cannot be less than 1')
   out = []
   words = s.split(' ')

   i = 0
   j = 0
   while (i + j) < len(words):
      word = words[i]
      if i >= words_per_seperator:
         out.append( ' '.join(words[j:j+i]) )
         j += i
         i = 0

      i += 1

   out.append( ' '.join(words[j:j+i]) )

   return seperator.join(out)


def extractMemo(memo_file):
   print('extracting {}...'.format(memo_file))
   data = parseMemo(memo_file)

   #if no title for memo
   title_cutoff = 18
   if data['Title'] == '':
      if len(data['Content']) > title_cutoff + 1:
         data['Title'] = data['Content'][:title_cutoff]
      else:
         data['Title'] = data['Content'][:]

      data['Title'] = data['Title'] + '~'

   #rmv special chars
   data['Title'] = re.sub('[^A-Za-z0-9]+', '', data['Title'])

   return data



import sys, os

if len(sys.argv) == 0:
   print('!Run format -> memo_extracter.py [source] [target_directory]')
   quit()
else:
   source = sys.argv[1]


filename_count = {}

if source.endswith(".memo") and not os.path.isdir(source):
      data = extractMemo(source)

      with open('{}.txt'.format(data['Title']), 'w', encoding='utf-8') as txtFile:
         if words_per_seperator != None:
            data['Content'] = seperateStr(data['Content'], words_per_seperator)
         content = 'Title: {}\nCreated: {}\n\n{}'.format(data['Title'], data['Created'], data['Content'])
         txtFile.write(content)

else:
   try:
      target_dir = sys.argv[2]
   except IndexError:
      target_dir = 'extract'

   try:
      os.makedirs(target_dir)
   except FileExistsError:
      pass

   for file in os.listdir(source):
      if file.endswith('.memo') and not os.path.isdir('{}/{}'.format(source, file)):
         data = extractMemo(source + '/' + file)

         filename = data['Title']
         if filename not in filename_count:
            filename_count[filename] = 0
         else:
            filename_count[filename] += 1
            filename = '{} ({})'.format(filename, filename_count[filename])


         with open('{}/{}.txt'.format(target_dir, filename), 'w', encoding='utf-8') as txtFile:
            if words_per_seperator != None:
               data['Content'] = seperateStr(data['Content'], words_per_seperator)
            content = 'Title: {}\nCreated: {}\n\n{}'.format(data['Title'], data['Created'], data['Content'])
            txtFile.write(content)