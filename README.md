## Installation

first you need to install the requirements of the projects using pip

```bash
pip install -r requirements.txt
```

second you need to have postgress installed and have an active database and an active user 
after you have installed postgres install pgadmin to be able to view the scraped products in the database 
then go to the CONNECTION_STRING property in the settings.py file and change it according to the comments written there

## Usage

to run the spider you type in the following command
```bash
scrapy crawl phones
```
the spider scraped 10 items per minute so be patient , it's meant to be that way so that amazon don't block us,
if you want to change that go to the settings.py file and comment out "DOWNLOAD_DELAY = 2" you will scrape
more products but you will be blocked faster , if you are blocked change your IP address or use a VPN and if you want to stop scraping press ctrl + c 
note that if you stopped scraping all the products that you have scraped before stopping will be saved in the database.

After you have scraped the products you run the following command 
```bash
python app.py
```
then after the server has loaded go to http://localhost:5000/graphiql, after GRAPHQL playground has loaded 
you can enter the following queries , or you can press ctrl + space to see the available fields
```bash
{
allProducts{
id
comments
imageUrls
link
rating
noOfReviews
description
ratingDistribution
features
}
}
```
this query gets you all the products in the database , and you can get or remove the field you want 
by removing the attributes between the curly braces, another query that is available is 

```bash
{
product(id: number){
id
comments
imageUrls
link
rating
noOfReviews
description
ratingDistribution
features
}
}
```
which allows you to retrieve a specific product by the number of id you pass
