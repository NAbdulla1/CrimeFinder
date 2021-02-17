from scraper.run_scraper import Scraper
from contextlib import closing
import sqlite3
import db_info
from text_preprocessor import preprocessor
from sentence_classifier.classifier import SentenceClassifier
from bangla_ner.location_processor import get_location
import districts
from opencage_location_api.OpenCageApi import get_approx_coordinate


def get_latest_articles():
    """
    the scraper will store the articles in the database
    and will set the 'processed' column of the articles to 0 means false
    :return:
    """
    scraper = Scraper()
    scraper.run_spiders()

    latest_articles = []
    with closing(sqlite3.connect(db_info.db_name)) as connection:
        with closing(connection.cursor()) as cursor:
            latest_articles = cursor.execute("SELECT * FROM articles where processed = 0").fetchall()
    return latest_articles


def combine_address(all_addresses):
    addr_str = ''
    addrset = set()
    district_found = False
    for addr in all_addresses:
        for ap in addr:
            if ap not in addrset:
                if district_found and ap in districts.districts:
                    return addr_str.strip()
                if ap in districts.districts:
                    district_found = True
                addr_str += ap
                addr_str += ' '
                addrset.add(ap)
    return addr_str.strip()


if __name__ == '__main__':
    latest_articles = get_latest_articles()
    sentenceClassifier = SentenceClassifier()   
    for article_row in latest_articles:
        (news_id, date, article, init_location, _) = article_row
        sentences = preprocessor.separate_sentences(article)
        loc_sentence_count = 0
        count = 0
        addresses = []
        for sentence in sentences:
            count+=1
            # todo process sentence
            if sentenceClassifier.is_location_sentence(sentence):
                #print(sentence)
                address_parts = get_location(sentence)
                addresses.append(address_parts)
                loc_sentence_count += 1 if len(address_parts) > 0 else 0
                if loc_sentence_count >= 2:
                    break
            if count >= 6:
                break

        address = combine_address(addresses)
        #print("address", address)
        #print()
        with closing(sqlite3.connect(db_info.db_name)) as connection:
            with closing(connection.cursor()) as cursor:
                if len(address) > 0:
                    coordinate = get_approx_coordinate(address)
                    coordinate = str(coordinate[0]) + ", " + str(coordinate[1])
                    cursor.execute(
                        "INSERT INTO news_location VALUES(?, ?, ?)",
                        (news_id, address, coordinate)
                    )
                cursor.execute("UPDATE articles SET processed = ? where news_id = ?",
                               (1, news_id))
            connection.commit()
