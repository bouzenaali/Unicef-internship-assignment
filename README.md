# UNICEF Data Science & AI/ML Internship

## Crisis Group Spider

### Overview

This project contains a Scrapy spider that scrapes crisis data from [CrisisWatch Database | Crisis Group](https://www.crisisgroup.org/crisiswatch/database) website.

### Project Structure (important files)

- `main.py`: Contains the `CrisisWatchSpider` class which is responsible for scraping data from the Crisis Group website.
- `output.csv`: Contains the scraped data in CSV format.
- `output.json`: Contains the scraped data in JSON format.


### How It Works

1. **Initialization**: The spider is initialized with the specified country IDs and generates start URLs based on these IDs.
2. **Start Requests**: The `start_requests` method generates initial requests to the start URLs with Playwright enabled.
3. **Parsing**: The `parse` method processes the response and extracts relevant crisis data. It uses XPath selectors to extract information such as country name, month and year, title, and paragraph.
4. **Data Extraction**: The extracted data is yielded as a dictionary containing the country name, month and year, title, and paragraph.

### Requirements
You first need to have the required dependencies:
```txt
Python3.11+
scrapy
playwright
```

### Running the Spider

To run the spider, use the following command:

```bash
python main.py
```
OR
```bash
python3 main.py
```

### Output

This will start the spider, scrape the data, and save it to `output.csv` and `output.json` in the same directory as the script.