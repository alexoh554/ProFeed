# ProFeed
ProFeed is a web application made with the flask module in python. ProFeed is not affiliated with the NHL, NBA, NFL, or MLB in any way.

## Description
ProFeed displays news from professional sports, and users can set preferences for the leagues they wish to follow. These settings are saved in a SQLite3 database along with the user's account information.

### Screenshots
![Screenshot](/screenshots/login.png?raw=true)
![Screenshot](/screenshots/signup.png?raw=true)
![Screenshot](/screenshots/feed.png?raw=true)

## Getting started
### Requirements
* [Python](https://www.python.org/)

### Installation
* In the command line run:
```
git clone https://github.com/alexoh554/ProFeed.git
```

* Install modules in requirements.txt:
```
pip install -r requirements.txt
```

* Run the program with `flask run`

## License
* [License](LICENSE.md)

## Acknowledgements
* All articles in the news feed are displayed using [ESPN's RSS Feature](https://www.espn.com/espn/news/story?page=rssinfo)
