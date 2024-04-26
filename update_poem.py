import syllables
import requests
import random
import time
import asyncio
import nltk

async def allowed_types(previous_word):
	if previous_word in ['a','an','the']:
		return ['VB','VBD','VBG','VBN','VBP','VBZ']
		
	pos = nltk.pos_tag([previous_word])[0][1]

	#adjective
	if pos.startswith('JJ'):
		return ['RB','RBR','RBS','VB','VBD','VBG','VBN','VBP','VBZ']
	#noun
	elif pos.startswith('NN'):
		if random.choice([0,1]) == 0:
			if previous_word[0] in ['a','e','i','o','u']:
				if previous_word[-1] == 's':
					return 'the'
				else:
					return random.choice(['an','the'])
			else:
				if previous_word[-1] == 's':
						return 'the'
				else:
					return random.choice(['a','the'])
		else:
			return ['JJ','JJR','JJS']
	#verb
	elif pos.startswith('VB'):
		return ['RB','RBR','RBS','NN','NNS','NNP','NNPS']

	else:
		return 'all'
		
async def update():
	print('making next file')
	#nltk.download('averaged_perceptron_tagger')
	
	total = time.perf_counter()
	
	#make the html file
	
	
	
	#words = requests.get("https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt").text.splitlines()
	
	words = open('templates/words.txt','r')
	words = words.read().splitlines()
	#newwords = []
	#for word in words:
	#	if 'a' in word or 'e' in word or 'i' in word or 'o' in word or 'u' in word or 'y' in word:
	#		newwords.append(word)
	#
	#newwords = '\n'.join(newwords)
	#doc = open('templates/words.txt','w')
	#doc.write(newwords)
	
	
	
	stanza_num = 4
	line_num = random.randrange(4,9)
	
	poem = []
	
	#scheme
	scheme = ['']*line_num
	
	sylltable = {'A': random.randrange(4,9)}
	sylltable['B'] = sylltable['A'] + random.randrange(-3,4)
	sylltable['C'] = sylltable['B'] + random.randrange(-2,3)
	sylltable['D'] = sylltable['C'] + random.randrange(-1,2)
	schemeset = ['A','A','B','B','C','C','D','D']
	"""
 	for i in range(line_num):
		scheme[i] = random.choice(['A','B','C','D'])
 	"""
	if line_num%2 != 0:
		scheme = schemeset.copy()[:line_num-1]
		random.shuffle(scheme)
		
		scheme+=schemeset[line_num-1]
	else:
		scheme = schemeset.copy()[:line_num]
		random.shuffle(scheme)
		
	print(scheme)

	endword = ''

	
	used = []
	stanzas = []
	for stanzacount in range(stanza_num):
		lines = []
		schemed = {}

		if endword != '':
			schemed[schemeset[line_num-1]] = endword
		
		print('Stanza: '+str(stanzacount))
		
		tick = time.perf_counter()
		for endrhymecount in range(line_num):
	
			currentscheme = scheme[endrhymecount]
			limit = sylltable[currentscheme]
			if currentscheme in schemed:
				#find a match
				
				rhyme = schemed[currentscheme]
				print(f'rhyme = {rhyme}')
				#lastoptions = []
				options = []

				#find the longest rhyme
				"""
				for matchlength in range(3,len(rhyme)-1):
					options = []
					match = rhyme[-matchlength:]
					
					for test in words:
						
						if test[-matchlength:] == match:
							if syllables.estimate(test) > limit:
								continue
							if rhyme in test:
								continue
							if test in rhyme:
								continue
							if  test in used:
								continue
							
							options.append(test)
					#print(options)
					if options == []:
						options = lastoptions.copy()
					else:
						lastoptions = options.copy()
				
				
				if options == []:
					options = lastoptions
					if options == []:
						test = 'asedkefjlasskeidjfilaksjidflikajoloolpyailopunyonwlnoe'
						while syllables.estimate(test) > limit:
							test = random.choice(words)
							used.append(test)
				else:		
					test = random.choice(options)
					lines.append(test)
					schemed[currentscheme] = test
					used.append(test)
				"""

				best = 1
				match = rhyme[-1:]
				for test in words:
					if test[-best:] == match:
						if syllables.estimate(test) > limit:
							continue
						if rhyme in test:
							continue
						if test in rhyme:
							continue
						if  test in used:
							continue

						
						if test[-best-1:] == rhyme[-best-1:]:
							best += 1
							if best >= 6:
								break
							match = rhyme[-best:]
							options = [test]
						else:
							options.append(test)

				test = random.choice(options)
				lines.append(test)
				schemed[currentscheme] = test
				used.append(test)
				if line_num % 2 != 0 and stanzacount == 0 and currentscheme == schemeset[line_num]:
					endword = test
				
			else:
				
				while True:
					
					test = random.choice(words)
					if syllables.estimate(test) <= limit and test not in used:
	
						lines.append(test)
						schemed[currentscheme] = test
						used.append(test)
						#print(lines,schemed,sylltable)
						break
	
		print(time.perf_counter() - tick)
		print(lines)
		
		tick = time.perf_counter()
		for linecount in range(line_num):
			line = [lines[linecount]]
			
			while syllables.estimate(' '.join(line)) < sylltable[scheme[linecount]]:
				pos_match = await allowed_types(line[0])
				if pos_match in ['a','an','the']:
					
					if syllables.estimate(' '.join(line)) + 1 <= sylltable[scheme[linecount]]:
						line.insert(0,pos_match)
						continue
					else:
						break
				else:
					test = random.choice(words)

				if pos_match != 'all':
					pos = nltk.pos_tag([test])[0][1]
					if pos not in pos_match:
						continue

				
				if syllables.estimate(test) + syllables.estimate(' '.join(line)) <= sylltable[scheme[linecount]]:
					line.insert(0,test)
					
			line.insert(0,scheme[linecount]+':')
			lines[linecount] = ' '.join(line)
	
		stanzas.append('<br>'.join(lines))
		print(time.perf_counter() - tick)
	stanzas = '<br>\n<br>\n<br>'.join(stanzas)
	content = '<p>'+str(stanzas)+'</p>'
	
	
	pagestart = """
	<!DOCTYPE html>
	<html>
	<head>
	
<meta name="msapplication-TileColor" content="#da532c">
<meta name="theme-color" content="#ffffff">
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width">
	<title>Random Rhyme Genorator</title>
	<h1>Welcome to the Random Rhyme Generator!</h1>
	<h2>The algorithmic bard wrote this poem just for you!</h2>
	<p>(yes these are real words)</p>
	
	</head>
	<body>  
	"""
	content = pagestart+content+"</body></html>"
	with open('templates/index.html', 'w') as f:
		f.write(content)
	
	print(time.perf_counter() - total)

if __name__ == '__main__':
	asyncio.run(update())