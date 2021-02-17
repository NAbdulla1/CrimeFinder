import re
import bengali_stopwords


def separate_sentences(article):
    sentences = [sen.strip() for sen in re.split('[।?!]', article)]
    return sentences


def remove_bangla_numbers(sentence):
    bangla_nums = bengali_stopwords.bengali_numbers_upto_99()
    for num in bangla_nums:
        sentence = sentence.replace(num, '')
    return sentence


def remove_special_symbols(sentence):
    sentence = sentence.replace('(', '')
    sentence = sentence.replace(')', '')
    sentence = sentence.replace(',', '')
    sentence = sentence.replace(u'\xa0', u' ')
    return sentence


def remove_stopwords(sentence):
    stopwords = bengali_stopwords.bangla_stopwords()
    new_sentence = []
    for word in sentence.split():
        if word not in stopwords and len(word) > 0:
            new_sentence.append(word)
    new_sentence = ' '.join(new_sentence)
    return new_sentence


def preprocess(sentence):
    sentence = remove_bangla_numbers(sentence)
    sentence = remove_special_symbols(sentence)
    # sentence = remove_stopwords(sentence)
    return sentence
