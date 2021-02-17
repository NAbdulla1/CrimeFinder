import re
import sqlite3
from contextlib import closing

import scrapy

import crime_keywords
import db_info
import districts


def extract_text(response):
    article = response.css('div.some-class-name2')
    paragraphs = article.css('p::text').getall()
    text = ''
    for para in paragraphs:
        text += para
    return text


def take_district(reporter_district_unprocessed):
    if 'পড়া যাবে' in reporter_district_unprocessed or 'বিজ্ঞপ্তি' in reporter_district_unprocessed:
        return ""
    district = districts.get_district(reporter_district_unprocessed)
    if len(district) != 0:
        return district
    reporter_district_unprocessed = reporter_district_unprocessed.replace('প্রতিনিধি', '')
    reporter_district_unprocessed = reporter_district_unprocessed.replace('বিশেষ', '')
    reporter_district_unprocessed = reporter_district_unprocessed.replace('সংবাদদাতা', '')
    reporter_district_unprocessed = reporter_district_unprocessed.replace('নিজস্ব', '')
    reporter_district_unprocessed = reporter_district_unprocessed.replace('প্রতিবেদক', '')
    reporter_district_unprocessed = reporter_district_unprocessed.replace('থেকে', '')
    reporter_district_unprocessed = reporter_district_unprocessed.replace('প্রতি‌নি‌ধি', '')
    reporter_district_unprocessed = reporter_district_unprocessed.replace(' ও ', ' ')
    reporter_district_unprocessed = reporter_district_unprocessed.replace('প্রতি‌নি‌ধি', '')
    reporter_district_unprocessed = reporter_district_unprocessed.replace('প্রতি‌নিধি', '')
    reporter_district_unprocessed = reporter_district_unprocessed.replace('অনলাইন ডেস্ক', '')
    reporter_district_unprocessed = reporter_district_unprocessed.replace('অনলাইন ডেক্স', '')
    reporter_district_unprocessed = reporter_district_unprocessed.replace('অ‌ফিস', '')
    reporter_district_unprocessed = reporter_district_unprocessed.replace('কালের কণ্ঠ অনলাইন', '')
    reporter_district_unprocessed = reporter_district_unprocessed.replace('কালের কণ্ঠ ডেস্ক', '')
    reporter_district_unprocessed = re.split(',', reporter_district_unprocessed)[::-1]
    for part in reporter_district_unprocessed:
        if '(' in part:
            st = part.index('(')
            en = part.find(')')
            if en == -1:
                en = st
            part2 = ''
            for i in range(0, len(part)):
                if not (st <= i <= en):
                    part2 += part[i]
            part = part2
        if len(part.strip()) > 0:
            return part.strip()
    return ""


class Kalerkantho(scrapy.Spider):
    name = "kalerkantho"
    start_urls = ['https://www.kalerkantho.com/online/country_news/0']
    recent_news_ids = []
    skip_next = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.skip_next = False

        with closing(sqlite3.connect(db_info.db_name)) as connection:
            with closing(connection.cursor()) as cursor:
                self.recent_news_ids = [row[0] for row in
                                        cursor.execute("SELECT news_id FROM articles where processed = 1"
                                                       " ORDER BY news_id DESC")]

    def parse(self, response, **kwargs):
        lst = response.css('a.title')
        titles = response.css('a.title::text').getall()
        assert len(titles) == len(lst)
        for (link, title) in zip(lst, titles):
            kws = crime_keywords.contains_keyword(title)
            if len(kws) > 0:
                yield response.follow(link, callback=self.parse2,
                                      cb_kwargs={'crime_types': crime_keywords.get_types(kws)})

        if self.skip_next:
            return

        next_page = response.xpath("//a[contains(text(), '>')]/@href").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse2(self, response, **kwargs):
        url = response.url
        (year, month, day, news_id) = url.split(sep="/")[-4:]

        crime_types = kwargs['crime_types']

        reporter_district = response.xpath('/html/body/div[6]/div[7]/div[2]/div[1]/p[1]/text()').get()

        news_id = "kk_" + news_id
        text = extract_text(response)
        date = f'{day}-{month}-{year}'
        reporter_district = take_district(reporter_district)

        if self.skip_next or news_id in self.recent_news_ids:
            self.skip_next = True
            print(f"{news_id} skipped")
            return

        with closing(sqlite3.connect(db_info.db_name)) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute("INSERT INTO articles VALUES(?, ?, ?, ?, ?)",
                               (news_id, date, text, reporter_district, 0))
                for crime_type in crime_types:
                    cursor.execute("INSERT INTO news_crime_types VALUES(?, ?)", (news_id, crime_type))
            connection.commit()

        yield {
            'news_id': news_id,
            'date': date,
            'crime_types': crime_types,
            'article': text,
            'init_location': reporter_district
        }

        # /html/body/div[6]/div[7]/div[2]/div[1]/p[1]  # reporter and district
        # /html/body/div[6]/div[7]/div[2]/div[1]/p[2]  # date and time in bengali
        # print({'title': response.xpath('/html/body/div[6]/div[7]/h2/text()').get()})  # title of the article
