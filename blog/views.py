from django.shortcuts import render
from django.conf import settings
import requests
from django.views import View
from datetime import datetime,timedelta

class BlogHome(View):
    images = []
    titles = []
    descriptions = []
    date = []
    forward = []

    def news_data(self):
        news_url = f'https://newsapi.org/v2/top-headlines?country=in&category=health&apiKey={settings.NEWS_API}'
        news = requests.get(news_url).json()
        news_data = news['articles']
        return news_data
    
    def formatDateTime(self,data):
        parsed_date = datetime.strptime(data, "%Y-%m-%dT%H:%M:%SZ")
        time_difference = datetime.utcnow() - parsed_date

        if time_difference < timedelta(minutes=1):
            return "just now"
        elif time_difference < timedelta(hours=1):
            minutes = int(time_difference.total_seconds() / 60)
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        elif time_difference < timedelta(hours=24):
            hours = int(time_difference.total_seconds() / 3600)
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif time_difference < timedelta(days=2) and parsed_date.date() == datetime.utcnow().date() - timedelta(days=1):
            return f"yesterday at {parsed_date.strftime('%H:%M:%S')}"
        elif time_difference < timedelta(days=7):
            days = int(time_difference.total_seconds() / (3600 * 24))
            return f"{days} day{'s' if days != 1 else ''} ago"
        elif time_difference < timedelta(days=30):
            weeks = int(time_difference.total_seconds() / (3600 * 24 * 7))
            return f"{weeks} week{'s' if weeks != 1 else ''} ago"
        elif time_difference < timedelta(days=365):
            months = int(time_difference.total_seconds() / (3600 * 24 * 30))
            return f"{months} month{'s' if months != 1 else ''} ago"
        elif time_difference >= timedelta(days=365):
            years = int(time_difference.total_seconds() / (3600 * 24 * 365))
            return f"{years} year{'s' if years != 1 else ''} ago"
        else:
            return parsed_date.strftime("%Y-%m-%d %H:%M:%S")
    
    def getData(self):
        data = self.news_data()
        for i in range(len(data)):
            f = data[i]
            self.titles.append(f['title'])
            self.descriptions.append(f['description'])
            if f['urlToImage'] is None:
                self.images.append('https://wmmedia.sgp1.cdn.digitaloceanspaces.com/blog.png')
            else:
                self.images.append(f['urlToImage'])
            self.date.append(self.formatDateTime(f['publishedAt']))
            self.forward.append(f['url'])
        mylist = zip(self.titles,self.descriptions,self.images,self.date,self.forward)
        return mylist

    def get(self,request):
        context = {
            'data':self.getData()
        }
        return render(request,'blog/home.html',context)