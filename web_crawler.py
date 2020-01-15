import requests
from bs4 import BeautifulSoup
import tldextract


def web_crawler(url, depth):
    if depth > 1:
        return
    sub_domain, domain, suffix = tldextract.extract(url)

    url_path = "http://" + sub_domain + "." + domain + "." + suffix
    page = requests.get(url)
    if page.status_code != 200:
        return

    soup = BeautifulSoup(page.content, 'html.parser')
    all_paragraphs = soup.find_all(text=True)
    pruned_paragraphes = []
    for paragraph in all_paragraphs:
        if len(paragraph.strip().split(" ")) > 10:
            pruned_paragraphes.append(paragraph.strip())

    if len(pruned_paragraphes) == 0:
        return

    content = ''.join(pruned_paragraphes)

    data = {'token': 'CSC3065',
            'url': url,
            'content': content}

    # sending post request and saving response as response object
    requests.post(url='https://qse.samirthapa.com/site', data=data)

    links = []
    for link in soup.findAll('a'):
        if link.has_attr('href'):
            if link['href'].startswith("/"):
                links.append(url_path + link['href'])

    for link in links:
        web_crawler(link, depth + 1)


web_crawler("http://quotes.toscrape.com/tag/humor/page/1/", 0)
