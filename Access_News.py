import requests
import json

api_key = "baa39d60d9104b6c81cafdbb2ece674c"
url = "https://newsapi.org/v2/top-headlines?q=covid&apiKey="+api_key


def AccessNews(url):
    response = requests.get(url)
    data = json.loads(response.text)
    articles = data["articles"]
    output = []

    for article in articles:
        title = article["title"]
        author = article["author"]
        date = article["publishedAt"]
        description = article["description"]
        content = article["content"]
        url = article["url"]
        image = article["urlToImage"]
        
        article_data = {
            "title": title,
            "author": author,
            "date": date,
            "description": description,
            "content": content,
            "url": url,
            "image": image
        }
        output.append(article_data)
    return output


news_json = AccessNews(url)

with open("CovidNews.json", "w") as f:
    json.dump(news_json, f, indent = 3)
