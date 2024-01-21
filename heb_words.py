#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from translate import Translator
from word2number import w2n
import re
import pandas as pd
import nltk
from nltk import pos_tag
from nltk.tokenize import word_tokenize

nltk.download("punkt", quiet=True)
nltk.download("averaged_perceptron_tagger", quiet=True)
heb_numbers_keywords = [
    "אחת",
    "שתיים",
    "שלוש",
    "ארבע",
    "חמש",
    "שש",
    "שבע",
    "שמונה",
    "תשע",
    "עשר",
    "עשרה",
    "עשרים",
    "שלושים",
    "ארבעים",
    "חמישים",
    "שישים",
    "שבעים",
    "שמונים",
    "תשעים",
    "מאה",
    "מאתיים",
    "שלוש מאות",
    "ארבע מאות",
    "חמש מאות",
    "שש מאות",
    "שבע מאות",
    "שמונה מאות",
    "תשע מאות",
    "אלף",
    "אלפיים",
    "שלושת אלפים",
    "ארבעת אלפים",
    "חמשת אלפים",
    "ששת אלפים",
    "שבעת אלפים",
    "שמונת אלפים",
    "תשעת אלפים",
    "עשרת אלפים",
    "מיליון",
    "אחת",
    "אחד",
    "שתי",
    "שתיים",
    "שניים",
    "שלוש",
    "שלושה",
    "ארבע",
    "ארבעה",
    "חמש",
    "חמישה",
    "שש",
    "שישה",
    "שבע",
    "שבעה",
    "שמונה",
    "תשע",
    "תשעה",
    "עשר",
    "עשרה",
]


def question2(text):
    values_to_replace = get_words_to_replace(text)
    for t in values_to_replace:
        old_text_heb = t[1]
        new_text_num = t[2]
        text = text.replace(old_text_heb, str(new_text_num))
    with open("modified_content.txt", "w") as file:
        file.write(text)
    return text


def get_words_to_replace(text):
    """
    Retrieve a list of words for replacement in the text.

    :param str text: The text in which numbers are to be found and replaced.

    :return: A list of words for replacement containing sublists of (English number, Hebrew number, the number as an integer).
    :rtype: list of tuple

    This function identifies Hebrew numbers in the text using the find_sequences function,
    translates them to English using the translate_hebrew_to_english function,
    and converts the translated words into integers using the word_to_num function from the word2number library.

    The information is aggregated into a list containing sublists of (English number, Hebrew number, the number as an integer).
    The list is sorted by the length of the Hebrew words in descending order.

    If the English word is empty after translation, something went wrong with the translation.
    Therefore, words with empty English translations are excluded from the final list.

    The resulting list is printed and returned.
    """
    words_to_replace = find_sequences(text, heb_numbers_keywords)
    eng_version = [translate_hebrew_to_english(w) for w in words_to_replace]
    nums = []
    for w in eng_version:
        try:
            nums.append(w2n.word_to_num(w))
        except ValueError:
            # One of the values wasn't translated correctly
            nums.append("")
            pass

    eng_heb_dict = list(zip(eng_version, words_to_replace, nums))
    sorted_words = sorted(eng_heb_dict, key=lambda x: len(x[1]), reverse=True)

    # If the english word was empty after translation, something went wrong with the translation.
    # Therefore, don't change that word.
    filtered_list = [(eng, heb, num) for eng, heb, num in sorted_words if eng != ""]
    print(filtered_list)
    return filtered_list


### Question 1
def get_article_content(url="https://www.ynet.co.il/laisha/article/b1al4tzyp"):
    """
    Fetch and return the content of an article from the specified URL. Additionally, save the content to a file.

    :param str url: The URL of the article. Default is a sample URL from ynet.co.il.

    :return: The article content in string form.
    :rtype: str

    The function fetches the HTML content of the specified URL, extracts the article content using BeautifulSoup,
    and saves the content to a file named "article_content.txt".

    If the article content is successfully fetched, it is returned as a string. If not, an appropriate message is printed.

    Dependencies:
    - Ensure that the `requests` and `BeautifulSoup` modules are properly imported before using this function.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Fetch the text via the class name (might need to change it for other websites)
    # This class name is applicable for some articles on ynet.co.il
    class_name = "public-DraftEditor-content"
    article_content = soup.find("div", {"class": class_name})

    if article_content:
        article_text = article_content.get_text()
        print("The content was saved to a file")
        with open("article_content.txt", "w", encoding="utf-8") as file:
            file.write(article_text)
        return article_text
    else:
        print("Article content wasnt fetched")


def translate_hebrew_to_english(text):
    """
    Translate Hebrew text to English using an external translation service.

    Parameters:
    - text (str): The input Hebrew text to be translated.

    Returns:
    - str: The translated English text.

    Dependencies:
    - Ensure that the `Translator` class from the translation library used is properly imported before using this function.
    """
    translator = Translator(to_lang="en", from_lang="he")
    translation = translator.translate(text)
    return translation


def find_sequences(sentence, words):
    """
    Identify sequences of words within a given sentence based on a list of specified words.
    The word list contains numbers written as words in Hebrew.

    :param str sentence: The input sentence in which sequences are to be identified.
    :param list words: A list of words defining the patterns to be searched for in the sentence.

    :return: A list containing all the sequences found in the input sentence that match the specified word patterns.
    :rtype: list of str
    """

    pattern = (
        r"\b(?:[א-ת]?"
        + "|[א-ת]?".join(words)
        + r")(?:\s(?:ו?"
        + "|ו?".join(words)
        + r"))*\b"
    )

    matches = re.findall(pattern, sentence)
    return matches


def find_num_word_tuple(text):
    """
    Extracts tuples of numbers and words from a given text.

    :param text: The input text where the function searches for the specified pattern.
    :type text: str

    :return: A list containing tuples, where each tuple consists of a number and
             the word following it in the text.
    :rtype: list of tuples

    :note: The regular expression allows for an optional prefix (in Hebrew) before the number.
    """
    pattern = r"\b[א-ת]*(\d+)\s*([a-zA-Zא-ת]+)\b"
    matches = re.findall(pattern, text)
    results = []
    for match in matches:
        number, word = match
        results.append((number, word))
        print(f"Number: {number}, Word: {word}")
    return results


def is_noun(heb_word):
    """
    Determine if a Hebrew word is a noun by translating it to English and analyzing its part of speech.

    :param str heb_word: The input Hebrew word to be analyzed.

    :return: True if the word is identified as a noun, False otherwise.
    :rtype: bool

    This function takes a Hebrew word as input, translates it to English using the `translate_hebrew_to_english` function,
    tokenizes the translated English word, and then uses part-of-speech tagging to identify if the word is a noun.
    The function returns True if the translated word is tagged as a noun (NN or NNS), and False otherwise.

    Dependencies:
    - Ensure that the `translate_hebrew_to_english`, `word_tokenize`, and `pos_tag` functions are properly defined
      and imported before using this function.
    """
    translated = translate_hebrew_to_english(heb_word)
    words = word_tokenize(translated)
    tagged_words = pos_tag(words)
    Type = tagged_words
    # Check if the first word is tagged as a noun (NN or NNS)
    if tagged_words and tagged_words[0][1] in ["NN", "NNS"]:
        return True
    else:
        return False


def question3(text):
    """
    Extract and display numeric values along with their associated Hebrew words in a DataFrame.

    :param str text: The processed text containing numeric values and their associated Hebrew words.

    :return: A DataFrame with columns "Number" and "Word" containing the extracted numeric values and their associated words.
    :rtype: pandas.DataFrame

    This function is designed to operate on text that has undergone processing in a previous step (using question2 function).
    It extracts numeric values and their corresponding Hebrew words from the input text, filters the results to include only
    nouns using the `is_noun` function, and then displays the data in a pandas DataFrame.

    The DataFrame has two columns: "Number" containing the numeric values (converted to integers), and "Word" containing
    the associated Hebrew words.
    """
    results = find_num_word_tuple(text)
    k = len(results)
    filter_nouns_func = lambda x: True if is_noun(x[1]) else False
    results = list(filter(filter_nouns_func, results))
    n = len(results)
    data = {
        "Number": [int(results[i][0]) for i in range(n)],
        "Word": [results[i][1] for i in range(n)],
    }
    df = pd.DataFrame(data)
    print(df)
    return df


def test_q2():
    with open("article_content.txt", "r") as file:
        content = file.read()
        question2(content)

def test_q3():
    with open("modified_content.txt", "r") as file:
        content = file.read()
    question3(content)

test_q3()
