# Question 1 
Fetch and return the content of an article from the specified URL. Additionally, save the content to a file.


```python
#!pip install bs4
import requests
from bs4 import BeautifulSoup
def get_article_content(url='https://www.ynet.co.il/news/article/hj5gj13yp'):
    # Given a URL, this function will return the article content in a string form
    # as well as saving the content to a file.
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

```

# Question 2
## Idea
I approached the problem in following way:
1. Use regex in order to identify the words that represent a number in hebrew within a text, using a set of indicative words
2. Translate those words into English
3. Convert the English words into integers
4. Replace the Hebrew words in the original text with their corresponding integers


```python
heb_numbers_keywords = ['אחת', 'שתיים', 'שלוש', 'ארבע', 'חמש', 'שש', 'שבע', 'שמונה', 'תשע', 'עשר', 'עשרה', 'עשרים',
                        'שלושים', 'ארבעים', 'חמישים', 'שישים', 'שבעים', 'שמונים', 'תשעים', 'מאה', 'מאתיים', 'שלוש מאות',
                        'ארבע מאות', 'חמש מאות', 'שש מאות', 'שבע מאות', 'שמונה מאות', 'תשע מאות', 'אלף', 'אלפיים',
                        'שלושת אלפים', 'ארבעת אלפים', 'חמשת אלפים', 'ששת אלפים', 'שבעת אלפים', 'שמונת אלפים',
                        'תשעת אלפים', 'עשרת אלפים', 'מיליון', 'אחת', 'אחד',  'שתי', 'שתיים', 'שניים', 'שלוש',
                        'שלושה', 'ארבע', 'ארבעה', 'חמש', 'חמישה', 'שש', 'שישה', 'שבע', 'שבעה', 'שמונה', 'תשע', 'תשעה',
                        'עשר', 'עשרה']
```


```python
#!pip install word2number
from word2number import w2n
import re
```

## Implementation
The function find_sequences recieves two arguments: the text to search in and the list of words to search for.

This regex was designed with hebrew linguistics in mind, capturing single words that represent a number of a "string" of words that together form a number i.e "מאה חמישים ושלוש"


```python
def find_sequences(sentence:str, words:str):
    pattern = (
        r"\b(?:[א-ת]?"
        + "|[א-ת]?".join(words)
        + r")(?:\s(?:ו?"
        + "|ו?".join(words)
        + r"))*\b"
    )
    matches = re.findall(pattern, sentence)
    return matches

```

The translation function from hebrew to english.


```python
#!pip install translate
from translate import Translator

def translate_hebrew_to_english(text:str):
    translator = Translator(to_lang="en", from_lang="he")
    translation = translator.translate(text)
    return translation
```

Now we want to retrieve a list of words for replacement in the text.
* This function 
    * identifies Hebrew numbers in the text using the find_sequences function
    * translates them to English using the translate_hebrew_to_english function
    * converts the translated words into integers using the word_to_num function from the word2number library.

* The information is aggregated into a list containing sublists of (English number, Hebrew number, the number as an integer).




```python
def get_words_to_replace(text:str):
    words_to_replace = find_sequences(text, heb_numbers_keywords)
    eng_version = [translate_hebrew_to_english(w) for w in words_to_replace]
    nums = []
    for w in eng_version:
        try:
            nums.append(w2n.word_to_num(w))
        except:
            # One of the values wasn't translated correctly
            nums.append("")
            pass

    eng_heb_dict = list(zip(eng_version, words_to_replace, nums))
    sorted_words = sorted(eng_heb_dict, key=lambda x: len(x[1]), reverse=True)

    # If the english word was empty after translation, something went wrong with the translation.
    # Therefore, don't change that word.
    filtered_list = [(eng, heb, num) for eng, heb, num in sorted_words if num != '']
    return filtered_list
```

After implementing the previous functions, I combined them into a single function. 

This function also includes the additional functionality of replacing each word in the text that represents a number with the actual numerical value.


```python
def question2(text:str):
    values_to_replace = get_words_to_replace(text)
    for t in values_to_replace:
        old_text_heb = t[1]
        new_text_num = t[2]
        text = text.replace(old_text_heb, str(new_text_num))
    with open('modified_content.txt','w' ) as file:
        file.write(text)
    return text
```

## Tests - Question 2
I checked 5 articles, from the same news website, counting manually the number of occurences of words that represent number and compared it to the function's output.


```python
from heb_words import get_article_content, get_words_to_replace


def test_q2():
    # The five articles
    url1 = 'https://www.ynet.co.il/laisha/article/b1al4tzyp'
    url2= 'https://www.ynet.co.il/news/article/bjoj5g2fp'
    url3 ='https://www.ynet.co.il/news/article/h1vvdb3y6'
    url4 ='https://www.ynet.co.il/news/article/skqk5k2kp'
    url5 = 'https://www.ynet.co.il/news/article/hj5gj13yp'
    articles = [url1,url2,url3,url4,url5]
    # The text extracted from each article
    article_texts = list(map(get_article_content,articles))
    # apply the core function of question 2 on all articles.
    words_replace_in_articles =list(map(get_words_to_replace,article_texts ))
    # count how many words were indiciated as numbers
    counted_words_to_replace = list(map(len, words_replace_in_articles))
    # personally checked how many words that represent numbers are there in the i-th article.
    human_checks = [12,3,1,9,2]    
    print(f'Amount of words detected by the function {counted_words_to_replace}\nAmount of real words {human_checks}')

test_q2()
```

    The content was saved to a file
    The content was saved to a file
    The content was saved to a file
    The content was saved to a file
    The content was saved to a file
    Amount of words detected by the function [13, 3, 1, 9, 2]
    Amount of real words [12, 3, 1, 9, 2]


## Results
I checked 5 articles, from the same news website. I counted manually the number of occurences of words that represent number and compared it to the function's output.

The results for question 2 are as showed:
| Article | False positive | False negative | Total words that are representing numbers |
|---------|----------------|----------------|------------------------------------------|
|       1 |              0 |              0 |                                        12 |
|       2 |              0 |              1 |                                        3 |
|       3 |              0 |              0 |                                        1 |
|       4 |              0 |              0 |                                        9 |
|       5 |              1 |              0 |                                       2 |

Although only five articles were considered, the function for question 2 performed well.
I'll show two types of false detection:
1. Multiple meanings, e.g שבעה can be interpreted as funeral in Hebrew and seven.
2. Wrong translation. Since the function considers the English translation of the Hebrew word, there are cases where the word can be translated into two words with different meaning. e.g שני can be translated to scarlet or two.


# Question 3


In order to solve the question, I assume a term is being counted most likely will appear after the number that quantifies it.

* This function takes a text input and searches for patterns where a number is followed by a space and another word. 
* The regular expression used in the function also allows for an optional prefix in Hebrew characters before the number. 
* The function returns a list of tuples, where each tuple contains the extracted number and the following word.


```python
import re


def find_num_word_tuple(text:str):
    pattern = r'\b[א-ת]*(\d+)\s*([a-zA-Zא-ת]+)\b'
    matches = re.findall(pattern, text)
    results = []
    for match in matches:
        number, word = match
        results.append((number,word))
    return results
```

I assumed that that word that appears after the number is a noun, which is the counted term.

The following function determine if a Hebrew word is a noun by translating it to English and analyzing its part of speech. 


```python
import nltk
from nltk import pos_tag
from nltk.tokenize import word_tokenize
nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
def is_noun(heb_word:str):
    translated = translate_hebrew_to_english(heb_word)
    words = word_tokenize(translated)
    tagged_words = pos_tag(words)
    # Check if the first word is tagged as a noun (NN or NNS)
    if tagged_words and tagged_words[0][1] in ['NN', 'NNS']:
        return True
    else:
        return False

```

Finally we combine the functions together, in order to answer question 3.
The function below extract and display numeric values along with their associated Hebrew words in a DataFrame.


```python
import pandas as pd

from heb_words import find_num_word_tuple, is_noun

def question3(text:str):
    # the given text is after the processing done in question2, therefore we can look for numeric values
    results = find_num_word_tuple(text)
    # filter the words that aren't nouns
    filter_nouns_func = lambda x: True if is_noun(x[1]) else False
    results = list(filter(filter_nouns_func,results))                
    n = len(results)
    data = {"Number": [int(results[i][0]) for i in range(n)], 
            "Word": [results[i][1] for i in range (n)]}
    df = pd.DataFrame(data)
    return df

with open('modified_content.txt', 'r') as modified_file:
        content = modified_file.read()
        print(question3(content))
```

        Number     Word
    0        3     ימים
    1        2      שאר
    2       18     שנים
    3        5     דקות
    4        2   אמניות
    5        3  סיפורים
    6       14   מחזיקה
    7       84     מנחל
    8       25      שנה
    9        7     שנים
    10       2      שכל
    11       2    קלטות
    12       2     אותו
    13      15      שנה
    14      10     שנים
    15       2    הצגות


## Testing - Question 3
For two articles, I compared the output for question3 function and verified it manually. 

The output for the article:
https://www.ynet.co.il/news/article/hj5gj13yp


|   | Number | Word   |
|---|--------|--------|
| 0 |      9 | צווים   |
| 1 |     27 | הירשמו |
| 2 |     10 | ימים   |

The row with index 1 is false and it is explained by viewing the article - the word and the number where part of a promotion text within the article (not part of the text). The rest is correct.



The output for the article:
https://www.ynet.co.il/news/article/bjoj5g2fp
|    | Number | Word    |
|----|--------|---------|
|  0 |      3 | קצינים  |
|  1 |    535 | חיילי    |
|  2 |     27 | מבאר    |
|  3 |     10 | בוגרים   |
|  4 |     24 | מתל     |
|  5 |    108 | ימים    |
|  6 |     51 | בגולני   |
|  7 |      1 | בדור     |
|  8 |      7 | לית     |
|  9 |      0 | בבית    |
| 10 |     98 | פתחה   |
| 11 |     50 | מחבלים |

The results are fetched 7 quantified terms, while the rest are false positive.
The function fetches all the right numbers, but includes other cases as well:
1. Age - In the case of "בן 24 מתל אביב" it returns מתל as the quantified term. Since מתל can be translated to english as a noun, it is returned as a qauntified term.
2. Numbered term - In the case where a number appears, but instead of quantity its part of the meaning of the word. e.g גדוד 51 בגולני, where the number is related to the number that appears before the number and it doesn't reflect a quantity but instead it's part of the name.
3. Time - in the case of a number shown in the text such as 13:00 בבית העלמין, the number doesn't meant quantity but instead describe a time.


# Question 4
In order to sort all the articles by their similirity to a single article chosen, we will have to define some metrics.
I chose to use TF-IDF for vectorization of the articles and then define similarity with cosine similarity.

I would approach the problem using the following pipeline:
## Preprocessing
Parse the text and modify it:
1. Convert words to their original form (lemmatization)
2. Remove punctuation
3. In English, change the case of all words to lower case
4. Each number that is written as a word needs to converted to a number.

## Vectorize each document
Compute the TF-IDF vectors for each document. TF-IDF takes into account the importance of each term in a document relative to its frequency in the entire corpus.

* To compute TF (term frequency) we compute occurrence of a word in a article / the number of words in the article. 

* To compute the IDF (Inverse document frequency) we compute the log(total number of articles/(the number of documents containing that query word + 1))

* To compute TF-IDF we multiply those two values.

We take following steps:
1. Create a set of all the words in the corpus.
2. Create the following matrix:

| articles | w1 | w2 | w3 | w4 |
| -------- | --- | --- | --- | --- |
| a1       |    |    |    |    |
| a2       |    |    |    |    |
| a3       |    |    |    |    |
 

For each cell, compute the tf-idf value. For example, `TF(w1,a1)*IDF(w1,corpus)` will be the value for the dirst cell.



## Calculate the pairwise distance
Now we have a matrix that holds the TF-IDF value for each word, we can use cosine similarity to measure the similarity between two vectors, based on their angle.

* Cosine similarity is defined as: $S_C(A1,A2) = cos(\theta)= \frac{A1.A2}{(||A1||*||A2||)}$.
In words, it means dividing the dot product of two vectors A1,A2 by the multiplication of their magnitude.

* Calculating each pair of articles, we can store the results in a matrix:

| articles | a1  | a2  | a3  |
| -------- | --- | --- | --- |
| a1       |  1  |     |     |
| a2       |     |  1  |     |
| a3       |     |     |  1  |

* If we want to sort the articles based upon how similar they are to article $i$, we can extract the $i$ row with the corresponding article number.
* The higher (maximum value is 1) the value, the more similar it is to article $i$.


## Result
Finally, we can arrange the extracted row in descending order based on the values and present the outcomes in a tabular format.


# Question 5

The function's input will be urls of the two articles and their corresponding tables (output of question 3).

First we create a table that contain only the rows that appear on both tables, meaning the rows were the terms being counted are identical.

In order to determine the liklyhood of two identical object that were countedm we will determine some values:
* The similarity of the two articles - The more similar the articles are, it increases the option the objects (with the same name) are identical.
* The level of similarity of the paragraphs where the term was mentioned - if we use question 4 output on the two paragraphs, we get the similarity value of the two. The more similar, it is more likely that they are talking about the same term.
* If the value assigned as the quantity of that term is equal on both articles, it's another reason to link the two terms.


If we aggregate these we can calculate the probability the two terms are identical.
