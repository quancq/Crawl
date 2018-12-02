import requests
from lxml import html
import utils, os
import re


def crawl_content(url=None):
    if url is None:
        url = "https://gacsach.com/doc-online/117613/tuoi-muoi-bay-phan-i-chuong-19-phan-1.html"

    root = html.document_fromstring(requests.get(url).content)

    title = root.cssselect(".page-title")[0].text
    # print("Title : ", title)

    content = root.cssselect(".field-items")[0].text_content()
    content = re.sub('\n+', '\n', content).strip()
    # print("Content : ", content)

    data = title + "\n\n" + content
    return data


def crawl_book(book_url):
    # book_url = "https://gacsach.com/sach-truc-tuyen/tuoi-muoi-bay-german-matveev"

    root = html.document_fromstring(requests.get(book_url).content)

    book_title = root.cssselect(".booktitle")[0].text.strip()
    print("Book title : ", book_title)

    book_intro = root.cssselect(".field-type-text-with-summary .field-item")[0].text_content()
    print("\nBook intro : ", book_intro)

    book_img_url = root.cssselect(".imagesach img")[0].attrib["src"]
    print("\nBook image url : ", book_img_url)

    a_elms = root.cssselect(".book-navigation li a")
    chater_urls = [(a.text, "https://gacsach.com" + a.attrib["href"]) for a in a_elms]

    print("\n{} Chapter urls : ".format(len(chater_urls)))

    chapter_contents = []
    for i, (chapter_name, url) in enumerate(chater_urls):
        # print(url)
        # if i > 4:
        #     break
        chapter_content = crawl_content(url)
        chapter_contents.append(chapter_content)
        print("Crawl {}/{} chapters done".format(i+1, len(chater_urls)))

    chapter_contents = "\n\n".join(chapter_contents)
    book_content = "\n\n".join([book_title, book_intro, chapter_contents])
    save_path = os.path.join("./Data/{}/{}.txt".format(book_title, book_title))
    utils.save_str(book_content, save_path)

    # response.css(".booktitle::text").extract_first().strip()
    # response.css(".field-type-text-with-summary .field-item ::text").extract()
    # response.css(".book-navigation li a::attr(href)").extract()


if __name__ == "__main__":
    pass
    book_url = "https://gacsach.com/bay-buoc-toi-mua-he_nguyen-nhat-anh.full"
    book_url = "https://gacsach.com/sach-truc-tuyen/tuoi-muoi-bay-german-matveev"
    crawl_book(book_url)
    # content = crawl_content()
    # print(content)
