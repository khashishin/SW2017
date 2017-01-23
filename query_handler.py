import crawler

lemma_dict = crawler.get_lemma_dict()

def get_tf(term, document):
    # print term, "in", document, term in document, "count",document.count(term), "len", len(document)
    return float(document.count(term)) / len(document)


def get_idf(term, documents):
    try:
        return float(len(documents)) / sum([term in document for document in documents]) # ile_docs/w_ilu_docsach_jest_term
    except ZeroDivisionError:
        return 0

def get_base_form(word):
    try:
        return lemma_dict[word.lower().encode('utf-8')]
    except KeyError:
        return word.lower()

def news_is_relevant(query, target_news, city_to_news_mapping):
    measure = 0
    all_titles = []
    all_contents = []

    for news_list in city_to_news_mapping.itervalues(): # "miasto": [News, News]
        for news in news_list:
            lemmatized_title = []
            for word in news.title.split():
                lemmatized_title.append(get_base_form(word))
            all_titles.append(lemmatized_title)
            all_contents.append(news.lemmatized_words)

    lemmatized_title = []

    for word in target_news.title.split():
        lemmatized_title.append(get_base_form(word))
    # print all_contents

    for word_of_query in query.split():
        measure_for_word = 2 * (get_tf(word_of_query, lemmatized_title) * get_idf(word_of_query, all_titles)) \
                  + get_tf(word_of_query, target_news.lemmatized_words) * get_idf(word_of_query, all_contents)
        measure += measure_for_word
    if measure > 0:
        print measure

    return measure > 0





