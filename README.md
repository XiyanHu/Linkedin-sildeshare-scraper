# Linkedin-sildeshare-scraper
Linkedin slideshare web crawler downloading files on [SlideShare](https://www.slideshare.net/).
## Installation

* Python 2.7.*

* Beautiful Soup 4
```
$ pip install bs4
```
* Selenium Webdriver
```
$ pip install selenium
``` 

* Replace or Update chromedriver to latest version according to your OS. [Download](http://chromedriver.storage.googleapis.com/index.html) 

## Usage

1. Open the sharesilde_crawler.py with a text editor. 
2. Set parameters.
![scraper settings](https://github.com/XiyanHu/Linkedin-sildeshare-scraper/blob/master/screenshots/scraper%20settings.png)
* output_path: the path you want to save files. Use _ABSOLUTE PATH_!
* start_point: the page you start to scrape. I have set one for you, but you can change it!
* username: Your Linkedin account. You'd better register another account for testing in case that Linkedin blocked your original account. :)(I used Selenium so it seems not gonna happen. But just in case.)
* password: Your Linkedin password.
* search_depth: Depth you want search into. I used DFS in search algorithms. The program will stop and certain depths. You can also stop the program manually.

3. Run the program
```
$ python sharesilde_crawler.py
```

Linkedin will limit the number of downloads in 24 hours each account. So you can try more test accounts.


## Results
![results](https://github.com/XiyanHu/Linkedin-sildeshare-scraper/blob/master/screenshots/results.png)

The scraper will automatically download files in your output directory.(Resumes)

## ToDoList
* headless doesn't work...
* Maybe Multiprocessing
* Detect duplicate downloaded files
