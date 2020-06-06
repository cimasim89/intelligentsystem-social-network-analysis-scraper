from selenium import webdriver
import json
import sys
import click
import traceback

VERSION = '1.0.0'


def normalize_date(date_to_format):
    """
    Normalize date to YYYY-MM_DD format required for use into search URL
    :param date_to_format: datetime
    :return: string
    """
    return date_to_format.date()


def write_data(data, filename):
    """
    Store passed data into file named filename in json format
    :param data: array of dict
    :param filename: string
    :return: None
    """
    print('Store {count} articol into {filename}...'.format(count=len(data), filename=filename))
    with open(filename, "w") as json_file:
        json.dump(data, json_file)


def map_article_to_dictionary(item):
    """
    Map article html element to article dict.
    :param item: html_element
    :return: article
    """
    article = {}
    title = item.find_element_by_tag_name("h1")
    article['title'] = title.text
    abstract = item.find_element_by_tag_name("p")
    article['abstract'] = abstract.text
    return article


def get_next_page_url(driver):
    """
    Get next page Url if exists.
    :param driver: scraper_driver
    :return: string | None
    """
    navbar = driver.find_elements_by_class_name("pagination")
    pages_links = navbar[0].find_elements_by_tag_name("li")
    element = pages_links[-1].find_element_by_tag_name("a")
    if element.text == 'Successiva':
        return element.get_attribute("href")
    else:
        return None


def prepare_scraper(driver_path='./chromedriver'):
    """
    Initialize scraper function
    :param driver_path: string
    :return: func
    """

    def inner(query, from_date, to_date, requested_pages=100, result_file_name='.result.json'):
        """
        Scrape execution
        :param query: string
        :param from_date: string
        :param to_date: string
        :param requested_pages:  int
        :param result_file_name: string
        :return: None
        """
        get_url = "https://ricerca.repubblica.it/ricerca/repubblica?" \
                  "query={query}&fromdate={from_date}&todate={to_date}&sortby=ddate&author=&mode=all" \
            .format(query=query, from_date=from_date, to_date=to_date)
        driver = webdriver.Chrome(driver_path)
        driver.get(get_url)
        articles_list = []
        for page in range(requested_pages):
            print('Scraping page {page} of {requested_pages}:'.format(page=(page + 1), requested_pages=requested_pages))
            try:
                articles_section = driver.find_elements_by_tag_name("article")
                if len(articles_section) == 0:
                    break
                articles_list = articles_list + list(map(map_article_to_dictionary, articles_section))
                print('- Total articles found: {counted}!\n'.format(counted=len(articles_list)))
                address = get_next_page_url(driver)
                if not address:
                    break
                driver.get(address)
            except:
                print('Error occurs at page {page}'.format(page=page), sys.exc_info()[0])
        write_data(articles_list, result_file_name)
        driver.close()

    return inner


@click.command()
@click.option('--driver-path', '-d', prompt='Give your scraper driver path',
              help='The data file.', type=click.Path(exists=True, file_okay=True, ))
@click.option('--result-filename', '-f', prompt='Give result Filename',
              help='Where data will be stored.')
@click.option('--query', '-q', prompt='Search query',
              help='The word that will be searched.')
@click.option('--pages', '-p', prompt='Page to scrape',
              help='How many pages will be scraped.', type=click.INT)
@click.option('--start-date', '-sd', prompt='Search start date',
              help='Date from start search.', type=click.DateTime(formats=['%Y-%m-%d', ]))
@click.option('--end-date', '-ed', prompt='Search end date',
              help='Date to end search.', type=click.DateTime(formats=['%Y-%m-%d', ]))
def main(driver_path, result_filename, query, pages, start_date, end_date):
    if end_date < start_date:
        print('Search dates request malformed! End date is before start date!', )
        exit(1)
    from_date = normalize_date(start_date)
    to_date = normalize_date(end_date)
    try:
        print('Starting scrape search: {query}...'.format(query=query))
        print('From {start_date} to {end_date}.'.format(start_date=start_date, end_date=end_date))
        scraper = prepare_scraper(driver_path)
        scraper(query=query, from_date=from_date, to_date=to_date, requested_pages=pages,
                result_file_name=result_filename)
        print('\nAll done...')
    except:
        print('Error occurs!', sys.exc_info()[0])
        print(traceback.format_exc())
        exit(1)


if __name__ == '__main__':
    print('<----------- Scraper Repubblica.it Version {} ------------->'.format(VERSION))
    main()
