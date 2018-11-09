import praw
from time import sleep
import time
import pendulum
from pendulum import datetime
import imgurpython
from collections import Counter
import savefig
import os
import matplotlib.pyplot as plt
import numpy as np
from imgurpython import ImgurClient
from scipy.stats import kde
'''
Data to gather: 
'''
USERAGENT = 'web:PeskyStatsBot:v1.0 (by ',u',ThePeskyWabbit)'
IMGUR_ID = '60a5ba1e95afc6a'
IMGUR_SECRET = '6975c23826a7f4f54885b1c352aa9610573f9655'

DEFAULT_SUBS = ['announcements','Art','AskReddit','askscience','aww','blog','books','creepy','dataisbeautiful','DIY',
'Documentaries','EarthPorn','explainlikeimfive','food','funny','Futurology','gadgets','gaming','GetMotivated','gifs',
'history','IAmA','InternetIsBeautiful','Jokes','LifeProTips','listentothis','mildlyinteresting','movies','Music','news',
'nosleep','nottheonion','OldSchoolCool','personalfinance','philosophy','photoshopbattles','pics','science','Showerthoughts',
'space','sports','television','tifu','todayilearned','UpliftingNews','videos',
'worldnews', 'WTF', 'politics']


WORDS = ['a', 'able', 'about', 'above', 'abst', 'accordance', 'according', 'accordingly', 'across', 'act', 'actually',
             'added', 'adj', 'affected', 'affecting', 'affects', 'after', 'afterwards', 'again', 'against', 'ah', 'all',
             'almost', 'alone', 'along', 'already', 'also', 'although', 'always', 'am', 'among', 'amongst', 'an', 'and',
             'announce', 'another', 'any', 'anybody', 'anyhow', 'anymore', 'anyone', 'anything', 'anyway', 'anyways',
             'anywhere', 'apparently', 'approximately', 'are', 'aren', 'arent', 'arise', 'around', 'as', 'aside',
             'ask', 'asking', 'at', 'auth', 'available', 'away', 'awfully', 'b', 'back', 'be', 'became', 'because',
             'become', 'becomes', 'becoming', 'been', 'before', 'beforehand', 'begin', 'beginning', 'beginnings',
             'begins', 'behind', 'being', 'believe', 'below', 'beside', 'besides', 'between', 'beyond', 'biol',
             'both', 'brief', 'briefly', 'but', 'by', 'c', 'ca', 'came', 'can', 'cannot', "can’t", "can't", 'cause', 'causes',
             'certain', 'certainly', 'co', 'com', 'come', 'comes', 'contain', 'containing', 'contains', 'could', 'couldnt',
             'd', 'date', 'did', "didn’t", "didn't", 'different', 'do', 'does', "doesn’t", "doesn't", 'doing', 'done', "don’t", 'don’t', "don't", 'down',
             'downwards', 'due', 'during', 'e', 'each', 'ed', 'edu', 'effect', 'eg', 'eight', 'eighty', 'either', 'else',
             'elsewhere', 'end', 'ending', 'enough', 'especially', 'et', 'et-al', 'etc', 'even', 'ever', 'every', 'everybody',
             'everyone', 'everything', 'everywhere', 'ex', 'except', 'f', 'far', 'few', 'ff', 'fifth', 'first', 'five', 'fix',
             'followed', 'following', 'follows', 'for', 'former', 'formerly', 'forth', 'found', 'four', 'from', 'further',
             'furthermore', 'g', 'gave', 'get', 'gets', 'getting', 'give', 'given', 'gives', 'giving', 'go', 'goes', 'gone',
             'got', 'gotten', 'h', 'had', 'happens', 'hardly', 'has', "hasn’t", "hasn't", 'have', "haven’t", "haven't", 'having', 'he', 'hed',
             'hence', 'her', 'here', 'hereafter', 'hereby', 'herein', 'heres', 'hereupon', 'hers', 'herself', 'hes', 'hi',
             'hid', 'him', 'himself', 'his', 'hither', 'home', 'how', 'howbeit', 'however', 'hundred', 'i', 'id', 'ie', 'if',
             "i’ll", "i'll", 'im', "i’m", "i'm", 'i’m', 'immediate', 'immediately', 'importance', 'important', 'in', 'inc', 'indeed', 'index',
             'information', 'instead', 'into', 'invention', 'inward', 'is', "isn’t", "isn't", 'it', 'it.', 'itd', "it’ll", "it'll", "it’s", 'its',
             'itself', "i’ve", "i've", 'j', 'just', 'k', 'keep 	keeps', 'kept', 'kg', 'km', 'know', 'known', 'knows', 'l',
             'largely', 'last', 'lately', 'later', 'latter', 'latterly', 'least', 'less', 'lest', 'let', 'lets', 'like',
             'liked', 'likely', 'line', 'little', 'look', 'looking', 'looks', 'ltd', 'm', 'made', 'mainly', 'make',
             'makes', 'many', 'may', 'maybe', 'me', 'mean', 'means', 'meantime', 'meanwhile', 'merely', 'mg', 'might',
             'million', 'miss', 'ml', 'more', 'moreover', 'most', 'mostly', 'mr', 'mrs', 'much', 'mug', 'must', 'my',
             'myself', 'n', 'na', 'name', 'namely', 'nay', 'nd', 'near', 'nearly', 'necessarily', 'necessary', 'need',
             'needs', 'neither', 'never', 'nevertheless', 'new', 'next', 'nine', 'ninety', 'no', 'nobody', 'non', 'none',
             'nonetheless', 'noone', 'nor', 'normally', 'nos', 'not', 'noted', 'nothing', 'now', 'nowhere', 'o', 'obtain',
             'obtained', 'obviously', 'of', 'off', 'often', 'oh', 'ok', 'okay', 'old', 'omitted', 'on', 'once', 'one',
             'ones', 'only', 'onto', 'or', 'ord', 'other', 'others', 'otherwise', 'ought', 'our', 'ours', 'ourselves',
             'out', 'outside', 'over', 'overall', 'owing', 'own', 'p', 'page', 'pages', 'part', 'particular', 'particularly',
             'past', 'per', 'people', 'perhaps', 'placed', 'please', 'plus', 'poorly', 'possible', 'possibly', 'potentially', 'pp',
             'predominantly', 'present', 'previously', 'primarily', 'probably', 'promptly', 'proud', 'provides', 'put', 'q',
             'que', 'quickly', 'quite', 'qv', 'r', 'ran', 'rather', 'rd', 're', 'readily', 'really', 'recent', 'recently',
             'ref', 'refs', 'regarding', 'regardless', 'regards', 'related', 'relatively', 'research', 'respectively',
             'resulted', 'resulting', 'results', 'right', 'run', 's', 'said', 'same', 'saw', 'say', 'saying', 'says', 'sec',
             'section', 'see', 'seeing', 'seem', 'seemed', 'seeming', 'seems', 'seen', 'self', 'selves', 'sent', 'seven',
             'several', 'shall', 'she', 'shed', "she’ll", "she'll", 'shes', 'should', "shouldn’t", "shouldn't", 'show', 'showed', 'shown',
             'showns', 'shows', 'significant', 'significantly', 'similar', 'similarly', 'since', 'six', 'slightly', 'so',
             'some', 'somebody', 'somehow', 'someone', 'somethan', 'something', 'sometime', 'sometimes', 'somewhat',
             'somewhere', 'soon', 'sorry', 'specifically', 'specified', 'specify', 'specifying', 'still', 'stop', 'strongly',
             'sub', 'substantially', 'successfully', 'such', 'sufficiently', 'suggest', 'sup', 'sure', 'take', 'taken',
             'taking', 'tell', 'tends', 'th', 'than', 'thank', 'thanks', 'thanx', 'that', "that’ll", "that'll", 'thats', "that’s", "that's", "that’ve", "that've",
             'the', 'their', 'theirs', 'them', 'themselves', 'then', 'thence', 'there', 'thereafter', 'thereby', 'thered',
             'therefore', 'therein', "there’ll", "there'll", 'thereof', 'therere', 'theres', 'thereto', 'thereupon', "there’ve",
             'these', 'they', 'theyd', "they’ll", "they'll", 'theyre', "they’ve", "they've", 'think', 'this', 'those', 'thou', 'though',
             'thoughh', 'thousand', 'throug', 'through', 'throughout', 'thru', 'thus', 'til', 'tip', 'to', 'together',
             'too', 'took', 'toward', 'towards', 'tried', 'tries', 'truly', 'try', 'trying', 'ts', 'twice', 'two', 'u',
             'un', 'under', 'unfortunately', 'unless', 'unlike', 'unlikely', 'until', 'unto', 'up', 'upon', 'ups', 'us',
             'use', 'used', 'useful', 'usefully', 'usefulness', 'uses', 'using', 'usually', 'v', 'value', 'various', "’ve",
             'very', 'via', 'viz', 'vol', 'vols', 'vs', 'w', 'want', 'wants', 'was', 'wasnt', 'way', 'we', 'wed', 'welcome',
             "we’ll", "we'll", 'went', 'were', 'werent', "we’ve", "we've", 'what', 'whatever', "what’ll", "what'll", 'whats', 'when', 'whence',
             'whenever', 'where', 'whereafter', 'whereas', 'whereby', 'wherein', 'wheres', 'whereupon', 'wherever', 'whether',
             'which', 'while', 'whim', 'whither', 'who', 'whod', 'whoever', 'whole', "who’ll", "who'll", 'whom', 'whomever', 'whos',
             'whose', 'why', 'widely', 'willing', 'wish', 'with', 'within', 'without', 'wont', 'words', 'world', 'would',
             'wouldnt', 'www', 'x', 'y', 'yes', 'yet', 'you', 'youd', "you’ll", "you'll", 'your', 'youre', "you’re", "you're", 'yours', 'yourself',
             'yourselves', "you’ve", "you've", 'z', 'zero', '', '|', "i’m", "i'm", 'going', 'will', "it's", "don't", "i'm", "doesn't",
              "didn't", "you're", "that's", 'good', 'post', 'gif', 'pic', 'lol', 'lmao', 'rofl', "doesn't", "didn't", 'well',
             "isn't", "he's", "he’s", 'reddit', '-', 'man', 'guy', 'thing', "can't", "they're", "i've", "there's", 'pretty', 'bad', 'good'
             'things', 'feel', 'lot', 'time', 'better', 'feel', '>', '<', '=', '@', "i'd", 'yeah', 'don’t', 'that’s', 'it’s', 'it\'s']

'''
Next up:

'''

def populateSubList():
    subList = []
    with open("subs.txt", 'r') as f:
        for line in f.readlines():
            subList.append(line[0:len(line)-1])
    f.close()
    return subList

def authenticate():
    print('Authenticating...')
    reddit = praw.Reddit('bot1', user_agent=USERAGENT)
    print('Authenticated as {}\n'.format(reddit.user.me()))
    return reddit

auth = True
while (auth):
    try:
        client = ImgurClient(IMGUR_ID, IMGUR_SECRET)
        reddit = authenticate()
        auth = False
    except:
        print('Authentication Failed, retying in 30 seconds.')
        time.sleep(30)

def getUsersFromSubreddit(subreddit, howMany):
    # initialize function variables

    userList = []
    # save the last (sample size) comment authors, excluding repeat author entries
    for comment in reddit.subreddit(subreddit).comments(limit=1000):
        if comment.author not in userList:
            # Add user to list
            userList.append(comment.author)
        if len(userList) == howMany:
            break
    print('user list of sample size ' + str(howMany) + ' has been created.')
    return [userList, subreddit]

def getMostActiveSubsFromUserList(userList, subreddit):
    i = 0
    activityList = []
    # iterate through the users in the list gathered from the target sub
    for redditor in userList:
        userSubList = []
        print('On user #' + str(i))
        i+=1
        # if the list entry is a valid entry (had some come back as none-type for some reason??
        if(redditor):
            for comment in redditor.comments.new(limit=500):
                if(str(comment.subreddit.display_name) not in DEFAULT_SUBS and str(comment.subreddit.display_name).lower() not in str(subreddit)):
                    userSubList.append(str(comment.subreddit.display_name))
            data = Counter(userSubList)

            # find this users top 5 most active subreddits
            for sub in [x[0] for x in data.most_common(5)]:
                # check each and if it is a new sub, append it to the target sub's activity list
                print('adding ' + str(sub))
                activityList.append(sub)

    data = Counter(activityList)
    string = "The last " + str(len(userList)) + " commenters in r/" + subreddit + " are most active in the following subreddits"
    generateBarGraph(data, subreddit, string, "activeSubs")

def generatePlot(x, y, sub, string, folder):
    nbins = 500
    x = np.array(x).astype(np.float)
    y = np.array(y).astype(np.float)
    k = kde.gaussian_kde([x, y])
    xi, yi = np.mgrid[x.min():x.max():nbins * 1j, y.min():y.max():nbins * 1j]
    zi = k(np.vstack([xi.flatten(), yi.flatten()]))

    fig, ax = plt.subplots()


    im = ax.pcolormesh(xi, yi, zi.reshape(xi.shape), cmap='gist_rainbow')
    cbar = fig.colorbar(im, ax=ax, ticks=[min(zi[:]), max(zi[:])])
    cbar.set_ticklabels(['Min', 'Max'])
    cbar.set_label('Density of Datapoints', rotation=-90)
    ax.set_title(string[0])
    plt.ylim(top=(max(y)+min(y))/2)
    plt.xlabel(string[2])
    plt.ylabel(string[1])
    plt.xticks([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24])
    plt.savefig(os.getcwd() + '/images/' + folder + '/' + sub + '.jpeg', bbox_inches='tight', dpi=100)
    plt.close('all')
    print(sub + ' saved.')
    return os.getcwd() + '/images/' + folder + '/' + sub + '.jpeg'


def generateBarGraph(countList, sub, title, folder):
    objects = []
    performance = []
    for item in countList.most_common(15):
        objects.append(item[0])
        performance.append(item[1])

    y_pos = np.arange(len(objects))

    plt.figure(figsize=(10,4))
    plt.grid(zorder=0)
    plt.bar(y_pos, performance, align='center', zorder=3)
    plt.xticks(y_pos, objects)
    plt.title(title)
    plt.xticks(rotation=45)
    plt.ylabel("Occurrences in sample")
    plt.xlabel("")
    plt.tight_layout()
    plt.savefig(os.getcwd() + '/images/' + folder + '/' + str(sub) + '.jpeg', bbox_inches='tight', dpi=100)
    plt.close('all')
    return os.getcwd() + '/images/' + folder + '/' + str(sub) + '.jpeg'

def postToSub(body, subreddit):
    title = "Statistics of r/" + subreddit + " -- " + pendulum.today('America/Chicago').format('MM-DD-YYYY')
    title2 = "Here are statistics of r/" + subreddit + " based on activity of the past week! (" + pendulum.today('America/Chicago').format('MM-DD-YYYY') + ")"
    reddit.subreddit("peskystatsbot").submit(title, body)
    reddit.subreddit(subreddit).submit(title2, body)


def mostCommonWords(sub, sample, time):

    commentIDs = []
    wordList = []
    i = 0
    print("processing " + sub + " with sample: " + str(sample))
    while(i < 1):
        for post in reddit.subreddit(sub).top(time, limit=sample):
            for comment in post.comments.list():
                if 'MoreComments' not in str(type(comment)) and comment.id not in commentIDs:
                    content = comment.body.lower().split(' ')
                    if 'bot' not in comment.body.lower():
                        for word in content:
                            if (str(word).endswith('.') or str(word).endswith(',') or str(word).endswith('!') or str(
                                    word).endswith('?')):
                                word = str(word).strip()[0:len(str(word).strip()) - 1]
                            for item in WORDS:
                                if word not in item and item not in word:
                                    wordList.append(word)
                                    commentIDs.append(comment.id)
        i += 1
    print(sub + " complete!")
    data = Counter(wordList)
    return data

def mostActiveUsers(sub, sample):
    users = []
    for post in reddit.subreddit(sub).hot(limit=sample):
        users.append(post.author)
        for comment in post.comments:
            if 'mod' not in comment.author and 'bot' not in comment.author:
                users.append(comment.author)
    userCount = Counter(users)
    return userCount

'''
format for text document:
subredditName/YYYY MM DD
'''
def getSubList(duplicates, howMany):
    print(pendulum.today())
    subList = []
    dupeSubNames = []
    newDuplicates = []
    i = 0
    while i < howMany:
        # create list of subs that are currently in list
        for dupe in duplicates:
            try:
                splitDupe = dupe.split("/")
                dupeSubNames.append(splitDupe[0])
                newDuplicates.append(splitDupe)
            except Exception as e:
                print()
                # do nothing

        for post in reddit.subreddit('all').hot(limit=100):
            if i < howMany:
                subName = post.subreddit.display_name
                if subName not in dupeSubNames:
                    dupeSubNames.append(subName)
                    newDuplicates.append([subName, pendulum.today('America/Chicago').format('YYYY MM DD')])
                    subList.append(subName)
                    print("Appended " + subName)
                    i += 1

                else:
                    currentIndex = 0
                    for item in newDuplicates:
                        if subName == item[0]:
                            lastTime = pendulum.DateTime.strptime(item[1], '%Y %m %d')
                            if 'week' in str(pendulum.today('America/Chicago').diff_for_humans(lastTime, absolute=True)):
                                print("appending " + subName + " from second function")
                                newDuplicates[currentIndex] = [subName, pendulum.today('America/Chicago').format('YYYY MM DD')]
                                subList.append(subName)
                                i += 1
                    currentIndex += 1
    with open('subs.txt', 'w') as f:
        for item in newDuplicates:
            print(item)
            print("Writing: " + str(item[0]) + "/" + str(item[1]) + " to subs.txt")
            f.write(str(item[0]) + "/" + str(item[1]) + "\n")
        f.close()

    return subList

def runAll(sampleSize, timeFrame):
    today = pendulum.today('America/Chicago').format('MM DD YYYY')
    while True:
        # If the number of times subs have been gathered and studied reaches 100, clear out all folders and reset
        # duplicate list so subs that have been studied can be studied again
        # List to stop duplicate subs being analyzed
        alreadyDone = populateSubList()

        print("getting subList")
        # For subreddit in list, study the subreddit
        for item in getSubList(alreadyDone, 5):
            # Subreddits to append to the alreadyDone list/text file
            print("Processing r/" + item)
            picList = []
            x = []
            y = []
            commentData = []
            commentIDs = []
            userList = []
            # get top 500 posts of the week/month
            # get all comments from each of the top 500 and add their words to a comment word list for the sub
            # get authors most used subs and add their top 5 to a userSubActivityList
            # perform counts on each necessary list
            # generate graphs and plots
            count = 0
            for post in reddit.subreddit(item).top(timeFrame, limit=sampleSize):
                if post.author is not None and post.author is not "":
                    userList.append(post.author)
                time = pendulum.from_timestamp(post.created_utc).format('H:mm')
                split = time.split(":")
                floatTime = float(int(split[1])/60)
                finalTime = int(split[0]) + floatTime
                x.append(finalTime)
                y.append(post.score)
                print("on post " + str(count) + ": " + post.title)
                for comment in post.comments.list():
                    if "More" not in str(type(comment)) and 'bot' not in comment.body.lower():
                        content = comment.body.lower().split(' ')
                        if comment.author is not "" and comment.author is not None:
                            userList.append(comment.author)
                        for word in content:
                            if (str(word).endswith('.') or str(word).endswith(',') or str(word).endswith(
                                    '!') or str(word).endswith('?')):
                                word = str(word).strip()[0:len(str(word).strip()) - 1]
                            if str(word).strip().lower() not in WORDS:
                                commentData.append(word)
                                commentIDs.append(comment.id)
                count += 1

            commentWordCount = Counter(commentData)
            print(commentWordCount.most_common(15))

            # create bar graph of most used words
            title = "The commenters in the top " + str(sampleSize) + " posts of the week in r/" + item + "\n most frequently used these words -- " + today
            picList.append(generateBarGraph(commentWordCount, item, title, "most_common_words"))

            userCount = Counter(userList)
            title = "The most active users in the top " + str(sampleSize) + " posts of the week in r/" + item + "\n were as follows  --  " + today
            picList.append(generateBarGraph(userCount, item, title, "most_active_users"))

            # create heatmap of times vs scores
            title = ["Scores vs Time of Day submitted for the \n top " + str(sampleSize) + " posts of the week in r/" + item + " -- " + today, "Score of Post", "Time Posted (24hr CST)"]
            picList.append(generatePlot(x, y, item, title, "heatmaps"))


            # upload images to reddit and make a text-post to the subreddit with both links in it.
            bodyText = ""
            print("attempting to upload to imgur")
            print(picList)
            for path in picList:
                notUploaded = True
                image = None
                while notUploaded:
                    try:
                        image = client.upload_from_path(path=path)
                        notUploaded = False
                    except Exception as e:
                        print(e)
                        sleep(60)
                bodyText += image.get('link') + "\n\n"

            bodyText += "\n\nI am a bot! -- [Source Code](https://github.com/PeskyWabbit/PeskyStatsBot) -- /r/PeskyStatsBot"

            try:
                print("trying to post to sub")
                postToSub(bodyText, subreddit=item)
            except Exception as e:
                print(e)
                print("Second to last exception")
                # add subreddit to list of subs to not repeat.
                with open("subs.txt", 'a') as f:
                    f.write(item + "/" + str(pendulum.today('America/Chicago').format('YYYY MM DD')) + "\n")
                f.close()

runAll(50, "week")
