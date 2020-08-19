from instabot import Bot 
import os, os.path
import re
import requests,urllib
import praw,ffmpeg
import configparser
import concurrent.futures
import argparse
import time

global subreddit  
bot = Bot() 
bot.login(username = "freshly.squeeze",  
          password = "Epicgamerman2005") #LOGIN TO BOT

class redditImageScraper: #SCRAPE IMAGES
    def __init__(self, sub, limit, order):
        config = configparser.ConfigParser()
        config.read('conf.ini')
        self.sub = sub
        self.limit = limit
        self.order = order
        self.path = f'images/{self.sub}/'
        self.reddit = praw.Reddit(client_id=config['REDDIT']['client_id'],
                                  client_secret=config['REDDIT']['client_secret'],
                                  user_agent='Multithreaded Reddit Image Downloader v2.0 (by u/impshum)')

    def download(self, image):
        r = requests.get(image['url'])
        with open(image['fname'], 'wb') as f:
            f.write(r.content)

    def start(self):
        images = []
        try:
            if not os.path.exists(self.path):
                os.makedirs(self.path)
            go = 0
            if self.order == 'hot':
                submissions = self.reddit.subreddit(self.sub).hot(limit=None)
            elif self.order == 'top':
                submissions = self.reddit.subreddit(self.sub).top(limit=None,time_filter="day")
            elif self.order == 'new':
                submissions = self.reddit.subreddit(self.sub).new(limit=None)

            for submission in submissions:
                #try: #VIDEO STUFF
                vidurl = submission.media['reddit_video']['fallback_url'] #obtain video part
                audio_url = vidurl[:vidurl.rfind('/')] + '/DASH_audio.mp4' #obtain audio part (holy shit reddit documentation is shit, its dash_audio.mp4 not /audio, literal aids)
                vidurl = vidurl.split("?")[0] #formatting?
                try:
                    urllib.request.urlretrieve(audio_url,self.path + "audio.mp3") #download audio
                except:
                    pass
                if os.path.isfile(self.path + "audio.mp3"): #IF WE ACC GOT AUDIO
                    urllib.request.urlretrieve(vidurl,self.path + "video.mp4") #download vid
                    infile1 = ffmpeg.input(self.path + "video.mp4") #set ffmpeg stuff
                    infile2 = ffmpeg.input(self.path + "audio.mp3")


                    fname = self.path + submission.title[:30].rstrip() + ".mp4"
                    if not os.path.isfile(fname):
                        merged  = ffmpeg.concat(infile1, infile2, v=1, a=1) #merge
                        ffmpeg.output(merged[0], merged[1], fname) #output

                        os.remove(self.path + "video.mp4")
                        os.remove(self.path + "audio.mp3")
                        go += 1
                        print(go)
                        if go >= self.limit:
                            break
                else:
                    fname = self.path + submission.title[:30].rstrip() + ".mp4"
                    if not os.path.isfile(fname):
                        urllib.request.urlretrieve(vidurl,fname) #download without audio
                        go += 1
                        print(go)
                        if go >= self.limit:
                            break
                #except:
                #    pass
                
                if not submission.stickied and submission.url.endswith(('jpg', 'jpeg', 'png')): #photo stuff
                    if submission.url[-4:] == "jpeg": #to add correct file extension
                        fname = self.path + submission.title + submission.url[-5:] #include the .
                    else:
                        fname = self.path + submission.title + submission.url[-4:]
                    if not os.path.isfile(fname):
                        images.append({'url': submission.url, 'fname': fname})
                        go += 1
                        if go >= self.limit/2:
                            break
            if len(images):
                with concurrent.futures.ThreadPoolExecutor() as ptolemy:
                    ptolemy.map(self.download, images)
        except Exception as e:
            print(e)


def main():
    scraper = redditImageScraper(subreddit, 100, "hot")
    scraper.start() #START SCRAPER

while True: #run constantly
    choices=["dankvideos","memes","dankmemes"] #subreddits
    for i in choices: #cycle through them
        subreddit=i
        main()
                
        imgs = []
        path = "images/"+ subreddit #PATH OF SCRAPED IMAGES
        valid_images = [".jpg",".gif",".png",".tga",".mp4"]
        for f in os.listdir(path):
            ext = os.path.splitext(f)[1]
            if ext.lower() not in valid_images:
                continue
            imgs.append(str(os.path.join(path,f))) #ADD TO LIST

        imgsN = len(imgs) #get how many photos
        timeperpost = 1 #4320/imgsN #equal period between posting every 12 hours
        print(timeperpost)
        for i in imgs:
            if i.endswith(".jpeg"): #to add correct file extension
                text = i[:-5]
                text = text.replace(path,"")
                bot.upload_photo(i, 
                                caption = text + "\n \n #meme #memes #funny #dankmemes #memesdaily #funnymemes #lol #follow #dank #humor #like #love #dankmeme #tiktok #lmao #instagram #comedy #ol #anime #fun #dailymemes #memepage #edgymemes #offensivememes #memestagram #funnymeme #memer #fortnite #instagood #bhfyp") #UPLOAD LIST OF PHOTOS
            elif i.endswith(".mp4"): #to add correct file extension
                text = i[:-4]
                text = text.replace(path,"")
                try:
                    bot.upload_video(i, 
                                    caption = text + "\n \n #meme #memes #funny #dankmemes #memesdaily #funnymemes #lol #follow #dank #humor #like #love #dankmeme #tiktok #lmao #instagram #comedy #ol #anime #fun #dailymemes #memepage #edgymemes #offensivememes #memestagram #funnymeme #memer #fortnite #instagood #bhfyp") #UPLOAD LIST OF PHOTOS
                except:
                    bot.upload_video(i, 
                                    caption = "\n \n #meme #memes #funny #dankmemes #memesdaily #funnymemes #lol #follow #dank #humor #like #love #dankmeme #tiktok #lmao #instagram #comedy #ol #anime #fun #dailymemes #memepage #edgymemes #offensivememes #memestagram #funnymeme #memer #fortnite #instagood #bhfyp") #UPLOAD LIST OF PHOTOS

            else:
                text = i[:-4]
                text = text.replace(path,"")
                bot.upload_photo(i, 
                                caption = text + "\n \n #meme #memes #funny #dankmemes #memesdaily #funnymemes #lol #follow #dank #humor #like #love #dankmeme #tiktok #lmao #instagram #comedy #ol #anime #fun #dailymemes #memepage #edgymemes #offensivememes #memestagram #funnymeme #memer #fortnite #instagood #bhfyp") #UPLOAD LIST OF PHOTOS
                
            time.sleep(timeperpost)
            '''try:
                os.remove(i) #delete after uploading
            except Exception:
                pass #ELSE DO NOTHINbrBRRRRRRRRRRR'''

