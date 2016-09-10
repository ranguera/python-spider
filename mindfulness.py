# Python practice - mindfulness quotes spider for engage
# run this on console 'chcp 65001' to change encoding

import urllib.request
import codecs

authors = []
quotes = []


def GetGoodReads(page):
	chunks = []
	content = urllib.request.urlopen("http://www.goodreads.com/quotes/tag/mindfulness?page=" + str(page)).read()
	content = str(content.decode('utf-8', errors='ignore'))
	start = 0
	end = 0
	
	while( start != -1):
		start = content.find('<div class="quoteText">', end)
		if( start != -1 ):
			end = content.find('</a>', start)
			chunks.append(content[start:end])
	
	#print("Chunks found: " + str(len(chunks)))
	for i in range(len(chunks)):
		#print('\n')
		index = ProcessQuote(chunks[i])
		ProcessAuthor(chunks[i], index)
		#print('\n')
		
	
def ProcessQuote(chunk):
	left = '&ldquo;'
	right = '&rdquo;';
	start = chunk.find(left,0)
	end = chunk.find(right,0)
	quote = chunk[start+len(left):end]
	quote = quote.replace('<br>','. ')
	quote = quote.replace('<em>','')
	quote = quote.replace('</em>','')
	if(len(quote) < 240 ):
		quotes.append(quote)
		#print("Quote: " + quote)
		return end
	else:
		return -10
	
	
def ProcessAuthor(chunk, index):
	if( index != -10):
		left = '">'
		right = '</a>';
		start = chunk.find(left,index)
		end = chunk.find(right,start)
		authors.append(chunk[start+len(left):len(chunk)])
		#print("Author: " + chunk[start+len(left):len(chunk)])


def WriteFile():
	file = codecs.open('output.csv', 'w', 'utf-8')
	for i in range(len(authors)):
		file.write(authors[i]+"|"+quotes[i]+"\n")
	file.close


def Main():
	for i in range(30):
		print("Checking page: " + str(i+1))
		GetGoodReads(i)
	
	print("Found: " + str(len(quotes)) + " quotes")
	WriteFile()

	
Main()