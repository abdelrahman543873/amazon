# Amazon Scraper

Back-End web scraper to fetch product's ratings and reviews from amazon, storing them into a Postgresql database. This repo also include a Jupyter Notebook that is used for data wrangling and analysis.

## Getting Started

### Postgresql

You must have `Postgresql` installed in your machine. To install it, open your terminal and execute:

```bash
sudo apt install postgresql
```

Then to activate the database server, run:

```bash
sudo service postgresql start
```

Create a postgresql database using the following command:

```bash
createdb <your_db_name>
```

Finally, make sure to go to `/amazon/settings.py` and update your database connection string with your credentials and the database name you just created.

### Installing Dependencies

Make sure to have `Python3` installed in your machine. To install all of the project's dependencies, make sure to be in the root directory of this project, then execute:

```bash
pip3 install -r requirements.txt
```

### Running the Spider

To start scraping data, run the following in your terminal:

```bash
scrapy crawl <desired_product>
```

e.g. ```scrapy crawl phones```

### Running the Server

To run the server, make sure to be in the root directory, then execute:

```bash
export FLASK_APP=application.py
flask run
```

This will run the server on [http://localhost:5000/graphiql](http://localhost:5000/graphiql) in production mode.

## Cleaning Data

### Installing Anaconda

Make sure to have [Anaconda](https://www.anaconda.com/products/individual) installed in your machine. If you do, skip to the next section.

To install `Anaconda` on Linux, download [this installer](https://repo.anaconda.com/archive/Anaconda3-2020.11-Linux-x86_64.sh), then navigate to the directory where it was downloaded at and run the following in your terminal:

```bash
bash Anaconda3-2020.11-Linux-x86_64.sh
```

Continue through default installation options. For a more thorough reference, vist [Anaconda Installation Docs](https://docs.anaconda.com/anaconda/install/linux/).

### Running Jupyter Notebook

Make sure to be in the root directory, then run the following in your terminal to launch the Jupyter Notebook sever:

```bash
jupyter notebook
```

The server is started, by default, at [http://localhost:8888](http://localhost:8888), from there, choose `rating_system_wrangle.ipynb` file.

Change your database connection string, then start running all the cells, in order. This will make the scraped data cleaner, tidier and then save into a new table named `master`.
