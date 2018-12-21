
import json
import os

import PIL
from PIL import Image

import urllib
import urllib.request

from book_data import BOOKS

IMAGE_WIDTH  = 168
IMAGE_HEIGHT = 248
TEMPLATE =  """"<SEQ_NUM>": {
    "title": "<TITLE>",
    "image": "<GOODREADS_IMAGE_URL>",
    "genre": "<GENRE>"
  }"""



def resize(src_image, dst_image):
    img = Image.open(src_image)
    img = img.resize((IMAGE_WIDTH, IMAGE_HEIGHT), PIL.Image.ANTIALIAS)
    img.save(dst_image)


def _get_filename_from_url(url):

    parse_result = urllib.parse.urlparse(url)
    path, filename = os.path.split(parse_result.path)

    return filename


def download(url, dst_image):
    #image = urllib.URLopener()
    #image.retrieve(url, dst_image)
    urllib.request.urlretrieve(url, dst_image)


def foo():
    #print (json.dumps(BOOKS, indent=4))
    genres = {}
    books = BOOKS.get('books')
    for book in books:
        genre_list = book.get('genre').split(',')
        for genre in genre_list:
              if genre.strip() not in genres.keys():
                  genres[genre.strip()] = [book.get('title')]
              else:
                  genres.get(genre.strip()).append(book.get('title'))

    for genre in genres.keys():
        print ('%s: %d' %(genre, len(genres.get(genre))))
        print ('='*80)
        for title in genres.get(genre):
            print ('%80s' %(title))
        print ('\n')


def generate_html():
    genres = []
    books = BOOKS.get('books')
    for book in books:
        genre_list = book.get('genre').split(',')
        for genre in genre_list:
            genre = genre.strip()
            if genre not in genres:
                genres.append(genre)

    html = '<OPTION value="All">All Genres</OPTION>\n'
    for genre in genres:
        html += '<OPTION value="%s">%s</OPTION>\n' %(genre.replace(" ", ""), genre)

    return html

def generate_js():
    books = BOOKS.get('books')
    count = 0
    js = ""
    for book in books:
        count += 1
        image = os.path.join('images', _get_filename_from_url(book.get('goodreads').get('image')))
        book_data = TEMPLATE.replace("<TITLE>", book.get('title'))
        book_data = book_data.replace("<SEQ_NUM>", str(count))
        book_data = book_data.replace("<GOODREADS_IMAGE_URL>", image)
        book_data = book_data.replace("<GENRE>", book.get('genre').replace(" ", ""))
        if book.get('goodreads').get('myreview'):
            book_data = book_data[:-4] + ",\n"
            book_data += '    "review": "%s"' %book.get('goodreads').get('myreview')
            book_data += '\n  }'
        js += book_data
        js += ",\n"
    js = js[:-2]
    js = "var NUM_BOOKS = %d;\nvar BOOKS = {\n%s\n}" %(count, js)

    return js

def resize_book_images():
    if not os.path.exists('original'):
        os.mkdir('original')

    if not os.path.exists('images'):
        os.mkdir('images')

    books = BOOKS.get('books')
    for book in books:
        image = book.get('goodreads').get('image')
        print ('Resizing: %s' %image)
        download(image, os.path.join('original', _get_filename_from_url(image)))
        resize(
            os.path.join('original', _get_filename_from_url(image)),
            os.path.join('images', _get_filename_from_url(image))
            )



if '__main__' == __name__:
    resize_book_images()
    js_data = generate_js()
    fd = open('data.js', 'w')
    fd.write(js_data)
    fd.close()
    #print (generate_html())
