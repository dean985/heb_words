#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from translate import Translator
from word2number import w2n
import re

heb_numbers_keywords = ['אחת', 'שתיים', 'שלוש', 'ארבע', 'חמש', 'שש', 'שבע', 'שמונה', 'תשע', 'עשר', 'עשרה', 'עשרים',
                        'שלושים', 'ארבעים', 'חמישים', 'שישים', 'שבעים', 'שמונים', 'תשעים', 'מאה', 'מאתיים', 'שלוש מאות',
                        'ארבע מאות', 'חמש מאות', 'שש מאות', 'שבע מאות', 'שמונה מאות', 'תשע מאות', 'אלף', 'אלפיים',
                        'שלושת אלפים', 'ארבעת אלפים', 'חמשת אלפים', 'ששת אלפים', 'שבעת אלפים', 'שמונת אלפים',
                        'תשעת אלפים', 'עשרת אלפים', 'מיליון', 'אחת', 'אחד', 'שתי', 'שתיים', 'שניים', 'שלוש',
                        'שלושה', 'ארבע', 'ארבעה', 'חמש', 'חמישה', 'שש', 'שישה', 'שבע', 'שבעה', 'שמונה', 'תשע', 'תשעה',
                        'עשר', 'עשרה']


def question2(text):
    words_to_replace = find_sequences(text, heb_numbers_keywords)
    eng_version = [translate_hebrew_to_english(w) for w in words_to_replace]
    nums = []
    for w in eng_version:
        try:
            nums.append(w2n.word_to_num(w))
        except ValueError:
            # One of the values wasn't translated correctly
            nums.append('')
            pass

    eng_heb_dict = list(zip(eng_version, words_to_replace, nums))
    sorted_words = sorted(eng_heb_dict, key=lambda x: len(x[1]), reverse=True)
    modified_text = ''
    for t in sorted_words:
        old_text_heb = t[1]
        if t[0] == '':
            # Something went wrong with translation, keep the original word
            new_text_num = t[1]
        else:
            # Translation was successful
            new_text_num = str(t[2])
        modified_text = text.replace(old_text_heb, new_text_num)
    return modified_text







def get_article_content(url='https://www.ynet.co.il/laisha/article/b1al4tzyp'):
    # Given a URL, this function will return the article content in a string form
    # as well as saving the content to a file.
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Fetch the text via the class name (might need to change it for other websites)
    # This class name is applicable for some articles on ynet.co.il
    class_name = 'public-DraftEditor-content'
    article_content = soup.find('div', {'class': class_name})

    if article_content:
        article_text = article_content.get_text()
        print("The content was saved to a file")
        with open('article_content.txt', 'w', encoding='utf-8') as file:
            file.write(article_text)
        return article_text
    else:
        print('Article content wasnt fetched')


def translate_hebrew_to_english(text):
    translator = Translator(to_lang="en", from_lang="he")
    translation = translator.translate(text)
    return translation
    
def find_sequences(sentence, words):
    # pattern = r'\b(?:ו?' + '|ו?'.join(words) + r')(?:\s(?:ו?' + '|ו?'.join(words) + r'))*\b'
    pattern = r'\b(?:[א-ת]?' + '|[א-ת]?'.join(words) + r')(?:\s(?:ו?' + '|ו?'.join(words) + r'))*\b'

    matches = re.findall(pattern, sentence)
    return matches
