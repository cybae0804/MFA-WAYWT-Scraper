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
client_id = input('client_id: ')
client_secret = input('client_secret: ')
username = input('username: ')
password = input('password: ')
reddit = praw.Reddit(client_id=client_id,
	client_secret=client_secret,
	password=password,
	user_agent='WAYWT Stats Scraper',
	username=username)

# praw search
totalList = []
time_filter = input('time filter: ')
for submission in reddit.subreddit('malefashionadvice').search(
	'title:WAYWT NOT title:Top NOT title:Summer NOT title:Fit NOT title:Theme NOT title:Edition NOT title:META NOT title:Monthlong', 
	sort='new', time_filter=time_filter):
	print(submission.title)
	indivList = []
	for top_level_comment in submission.comments:
		brandCount = 0
		repeatSet = set()

		# if the post had been deleted, it won't store the author name. Later, rows w/o author names get dropped.
		if (top_level_comment.author):
			indivList.append(top_level_comment.author.name)

			commentDate = time.strptime(time.ctime(top_level_comment.created_utc))
			indivList.append(commentDate.tm_year)
			indivList.append(commentDate.tm_mon)
			indivList.append(commentDate.tm_mday)
			indivList.append(top_level_comment.score)
			results = kwtree.search_all(top_level_comment.body)

			# For my analysis, an individual wearing more than one item of the same brand is not repeated for that post.
			for result in results:
				if result[0] not in repeatSet:
					repeatSet.add(result[0])
					indivList.append(result[0])
					brandCount += 1

		while brandCount < 7:
			indivList.append('0')
			brandCount += 1

		indivList.append(top_level_comment.permalink)

		if (len(indivList) == 13):
			totalList.append(list(indivList))

		indivList.clear()

df = pd.DataFrame(totalList, columns=['username', 'year', 'month', 'day', 'score', 'BN1', 'BN2', 'BN3', 'BN4', 'BN5', 'BN6', 'BN7', 'permalink'])

# shortened brand names restored to official names
df = df.replace('BR ', 'Banana Republic')
df = df.replace('Birk', 'Birkenstocks')
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
df = df.replace('Brooks', 'Brooks Brothers')
df = df.replace('Martens', 'Doc Martens')
df = df.replace('Gitman', 'Gitman Vintage')
df = df.replace('Hilfiger', 'Tommy Hilfiger')
df = df.replace('CP ', 'Common Projects')

# exports the dataframe to a csv file for analysis
df.to_csv('cleanData.csv')