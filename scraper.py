import praw
import time
import numpy as np
import pandas as pd
import csv
from ahocorapy.keywordtree import KeywordTree

# Initializing Brand Names
brandNamesFile = open('brandNames.csv', 'r')
reader = csv.reader(brandNamesFile)
allRows = [row for row in reader]
brandNames = []

for item in allRows:
	brandNames.append(item[0])

# Initializing ahocorasick search
kwtree = KeywordTree(case_insensitive=True)

for brand in brandNames:
	kwtree.add(brand)

kwtree.finalize()

# Initializing praw reddit client
reddit = praw.Reddit(client_id=input('client_id: '),
	client_secret=input('client_secret: '),
	password=input('password: '),
	user_agent='WAYWT Stats Scraper',
	username=input('username: '))

# praw search return
totalList = []
for submission in reddit.subreddit('malefashionadvice').search(
	'title:WAYWT AND NOT Top AND NOT Summer AND NOT Theme AND NOT ANNOUNCEMENT AND NOT META AND NOT Monthlong', 
	sort='new', time_filter='month'):
	print(submission.title)
	indivList = []
	for top_level_comment in submission.comments:
		if (top_level_comment.author):
			indivList.append(top_level_comment.author.name)
			print(top_level_comment.author.name)
			print(top_level_comment.body)

		commentDate = time.strptime(time.ctime(top_level_comment.created_utc))
		indivList.append(commentDate.tm_year)
		indivList.append(commentDate.tm_mon)
		indivList.append(commentDate.tm_mday)
		indivList.append(top_level_comment.score)
		results = kwtree.search_all(top_level_comment.body)
		brandCount = 0

		repeatSet = set()
		for result in results:
			if result[0] in repeatSet:
				print('REPEAT FOUND')
			else:
				repeatSet.add(result[0])
				indivList.append(result[0])
				brandCount += 1
				print(result)
			#print("Current set: ", repeatSet)
			#print("Current input: ", result[0])
		while brandCount < 7:
			indivList.append('0')
			brandCount += 1
		#print(indivList)
		indivList.append(top_level_comment.permalink)
		if (len(indivList) == 13):
			totalList.append(indivList.copy())
			#print('ok')
		indivList.clear()
df = pd.DataFrame(totalList, columns=['username', 'year', 'month', 'day', 'score', 'BN1', 'BN2', 'BN3', 'BN4', 'BN5', 'BN6', 'BN7', 'permalink'])

df = df.replace('BR ', 'Banana Republic')
df = df.replace('Birk ', 'Birkenstocks')
df = df.replace('OL ', 'Our Legacy')
df = df.replace('Yohji', 'Yohji Yamamoto')
df = df.replace(['J.Crew', 'J. Crew', 'J crew', 'jcrew'], 'J. Crew')
df = df.replace(['Margiela', 'MMM'], 'Maison Margiela')
df = df.replace('Howell', 'MHL')
df = df.replace('Wings', 'Wings + Horns')
df = df.replace('Rag', 'Rag & Bone')
df = df.replace('NB', 'New Balance')
df = df.replace('UQ', 'Uniqlo')
df = df.replace('SLP', 'Saint Laurent Paris')
df = df.replace('Rick', 'Rick Owens')
df = df.replace(['A.P.C.', 'APC'], 'A.P.C.')
df = df.replace('Acne', 'Acne Studios')
df = df.replace(['arc\'teryx', 'arcteryx'], 'Arc\'teryx')
df = df.replace('Anonymousism', 'Anonymous Ism')
df = df.replace('UC ', 'Undercover')
df = df.replace('Y3', 'Y-3')
df = df.replace('Raf', 'Raf Simons')
df = df.replace('Naked', 'Naked & Famous')
df = df.replace('EG ', 'Engineered Garments')
df = df.replace('AE', 'American Eagle')
df = df.replace('Helmut', 'Helmut Lang')
df = df.replace('Onitsuka', 'Onitsuka Tiger')
df = df.replace('Levi ', 'Levis')
df = df.replace('Comme des', 'Comme des Garcons')
df = df.replace('SEF', 'Story Et Fall')
df = df.replace('Martens ', 'Doc Martens')
df = df.replace('Gitman', 'Gitman Vintage')
df = df.replace('Hilfiger', 'Tommy Hilfiger')
df = df.replace('CP ', 'Common Projects')





df.to_csv('cleanData.csv')