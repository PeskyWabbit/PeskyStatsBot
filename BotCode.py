import praw
import time
import pendulum
from collections import Counter
import savefig
import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import BoundaryNorm
from scipy.stats import kde
from matplotlib.ticker import MaxNLocator
'''
Data to gather: 
'''
USERAGENT = 'web:PeskyStatsBot:v1.0 (by ",u",ThePeskyWabbit)'

DEFAULT_SUBS = ["announcements","Art","AskReddit","askscience","aww","blog","books","creepy","dataisbeautiful","DIY",
"Documentaries","EarthPorn","explainlikeimfive","food","funny","Futurology","gadgets","gaming","GetMotivated","gifs",
"history","IAmA","InternetIsBeautiful","Jokes","LifeProTips","listentothis","mildlyinteresting","movies","Music","news",
"nosleep","nottheonion","OldSchoolCool","personalfinance","philosophy","photoshopbattles","pics","science","Showerthoughts",
"space","sports","television","tifu","todayilearned","UpliftingNews","videos",
"worldnews", "WTF", "politics"]


SUBS_TO_STUDY = ["meirl"]
'''
Next up:

'''

def authenticate():
    print("Authenticating...")
    reddit = praw.Reddit('bot1', user_agent=USERAGENT)
    print("Authenticated as {}\n".format(reddit.user.me()))
    return reddit


auth = True
while (auth):
    try:
        reddit = authenticate()
        auth = False
    except:
        print("Authentication Failed, retying in 30 seconds.")
        time.sleep(30)

def getSubsRedditorsMostActiveSub(subreddit, howMany):
    # initialize fukction variables
    activityList = []
    userList = []

    # save the last (sample size) comment authors, excluding repeat author entries
    for comment in reddit.subreddit(subreddit).comments(limit=1000):
        if comment.author not in userList:
            # Add user to list
            userList.append(comment.author)
        if len(userList) == howMany:
            break

    print("user list of sample size " + str(howMany) + " has been created.")

    i = 0
    # iterate through the users in the list gathered from the target sub
    for redditor in userList:
        userSubList = []
        print("On user #" + str(i))
        i+=1
        # if the list entry is a valid entry (had some come back as none-type for some reason??
        if(redditor):
            for comment in redditor.comments.new(limit=500):
                # If this users comment was not in askreddit or the target sub, or any of the other subs that are being looked at, add the subreddit to the list
                if(str(comment.subreddit.display_name) not in DEFAULT_SUBS and str(comment.subreddit.display_name).lower() not in str(subreddit)
                and str(comment.subreddit.display_name) not in SUBS_TO_STUDY):
                    userSubList.append(str(comment.subreddit.display_name))
            data = Counter(userSubList)

            # find this users top 5 most active subreddits
            for sub in [x[0] for x in data.most_common(5)]:
                # check each and if it is a new sub, append it to the target sub's activity list
                print("adding " + str(sub))
                activityList.append(sub)

    data = Counter(activityList)
    commonList = data.most_common(25)
    with open(subreddit + ".txt", 'w') as f:
        f.write("Sample size: " + str(howMany) + "\n")
        for item in commonList:
            if(item[1] > 1):
                f.write(str(item) + "\n")
        f.close()

def frontPageTimes(sub, time, sample):
    posts = []
    postsAndKarma = []
    for submission in reddit.subreddit(sub).top(time, limit=sample):
        posts.append(submission)

    for item in posts:
        #print(pendulum.from_timestamp(int(item.created_utc)).format('H:mm:ss '))
        #print("https://www.reddit.com" + item.permalink)
        karma = item.score
        #print("AVG karma per minute: " + str(karma) + "\n")

        postsAndKarma.append([item, karma])

    postsAndKarma.sort(key = lambda x : x[1])

    x = []
    y = []
    with open("frontPageTimes.txt", 'a') as f:
        for elem in postsAndKarma:
            f.write(pendulum.from_timestamp(int(elem[0].created_utc)).format('H:mm:ss') + " -- " + str(elem[1]) + "\n")
            time = pendulum.from_timestamp(int(elem[0].created_utc)).format('H:mm')
            split = time.split(":")
            ftime = float(split[1])/60
            x.append(round(float(split[0])+ftime, 2))
            y.append(elem[1])

    nbins = 500
    x = np.array(x)
    y = np.array(y)
    np.array(x).astype(np.float)
    np.array(y).astype(np.float)
    k = kde.gaussian_kde([x, y])
    xi, yi = np.mgrid[x.min():x.max():nbins * 1j, y.min():y.max():nbins * 1j]
    zi = k(np.vstack([xi.flatten(), yi.flatten()]))

    # Make the plot
    #levels = MaxNLocator(nbins=100).tick_values(zi.min(), zi.max())
    #cmap = plt.get_cmap('plasma')
    #norm = BoundaryNorm(levels, ncolors=cmap.N)

    plt.pcolormesh(xi, yi, zi.reshape(xi.shape), cmap='gist_rainbow')
    plt.title("Top " + str(sample) + " posts from " + "r/" + sub)
    plt.xlabel("Time posted (24h format)")
    plt.ylabel("Total score")

    plt.savefig(os.getcwd() + "\\images\\" + sub + ".jpeg", bbox_inches='tight', dpi=500)
    plt.close()
    print(sub + " saved.")

def getSubList():
    postList = []
    print("Gathering sublist")
    for post in reddit.subreddit("all").top("month", limit=1000):
        if post.subreddit.display_name not in postList:
            postList.append(post.subreddit.display_name)

    print("Sublist acquired")
    return postList

for item in getSubList():
    frontPageTimes(item, "month", 100)




