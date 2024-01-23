from heb_words import get_words_to_replace,get_article_content, question2, question3

url1 = 'https://www.ynet.co.il/news/article/hj5gj13yp'
url2= 'https://www.ynet.co.il/news/article/bjoj5g2fp'
url3 ='https://www.ynet.co.il/news/article/h1vvdb3y6'
url4 ='https://www.ynet.co.il/news/article/skqk5k2kp'
url5 = 'https://www.ynet.co.il/laisha/article/b1al4tzyp'
articles = [url1,url2,url3,url4,url5]
article_texts = list(map(get_article_content,articles))


def test_q2():
    # apply the core function of question 2 on all articles.
    words_replace_in_articles =list(map(get_words_to_replace,article_texts ))
    # count how many words were indiciated as numbers
    counted_words_to_replace = list(map(len, words_replace_in_articles))
    # personally checked how many words that represent numbers are there in the i-th article.
    human_checks = [2,3,1,9,12]    
    print(f'Amount of words detected by the function {counted_words_to_replace}\nAmount of real words {human_checks}')


def test_q3():
    # Articles modified after the question2 function
    articles_modified = [question2(article) for article in article_texts]
    articles_df = [question3(article) for article in articles_modified ]

    for i,table in enumerate(articles_df):
        print(f'Table {i}:\n{table}\n')


test_q2()