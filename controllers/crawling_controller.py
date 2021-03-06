from model.mongodb import conn_mongodb
import requests
from bs4 import BeautifulSoup
import re

class DataCrawling:
    @staticmethod
    def collect_data():
        DOMAIN = 'https://www.kanshudo.com'
        URI = '/collections/wikipedia_jlpt'
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(DOMAIN + URI, headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')

        outer_div = soup.select('div.infopanel')
        word_list = list()

        for divs in outer_div:
            a_list = divs.select('div.coll_div a')

            for i, a in enumerate(a_list):
                detail_url = DOMAIN + a.attrs['href']
                print(detail_url)
                detail_res = requests.get(detail_url, headers=headers)
                inner_soup = BeautifulSoup(detail_res.content, 'html.parser')
                detail_data = inner_soup.select('div.jr_inner div.jukugo')
                
                level = int(re.search('-N(.+?)-', detail_url).group(1))

                for detail in detail_data:
                    meaning_list = list()
                    
                    # meaning
                    detail_meanings = detail.parent.parent.select('div.jukugo_reading div.vm')
                    for m in detail_meanings:
                        pattern = re.compile(r'. </span>(.*?)</div>')
                        meaning = pattern.findall(str(m))
                        
                        if len(meaning) == 0:
                            pattern = re.compile(r'</span></div>(.*?)</div>')
                            meaning = pattern.findall(str(m))
                        
                        meaning = meaning[0].replace(u'\xa0', u'')
                        
                        meaning = re.sub('<span>(.*?)</span>', '', meaning)
                        words = meaning.split(';')
                        
                        for word in words:
                            print(word.strip())
                            meaning_list.append(word.strip())
                
                    # reading
                    tags = str(detail).split('<')          

                    furigana_full = list()
                    kanji_full = list()

                    tags_str = str(detail)

                    if tags_str.find('furigana') == -1 and tags_str.find('f_kanji') == -1:
                        pattern = re.compile(r'>(.*?)</a>')
                        pure_hiragana = pattern.findall(tags_str)[0]
                        
                        word_list.append({
                            'level': level,
                            'furigana': pure_hiragana,
                            'kanji': None,
                            'meanings': meaning_list
                        })
                        continue

                    for tag in tags:                
                        if tag.find('furigana') != -1:
                            furigana = re.sub('.*>', '', tag)
                            furigana_full.append(furigana)
                        if tag.find('f_kanji') != -1:
                            kanji = re.sub('.*>', '', tag)
                            kanji_full.append(kanji)
                        if tag.find('/span>') != -1 and len(tag) > 6:
                            okurigana = re.sub('.*>', '', tag)
                            furigana_full.append(okurigana)
                            kanji_full.append(okurigana)

                    furigana_word = ('').join(furigana_full)
                    kanji_word = ('').join(kanji_full)

                    word_list.append({
                        'level': level,
                        'furigana': furigana_word,
                        'kanji': kanji_word,
                        'meanings': meaning_list
                    })
                
        db = conn_mongodb()
        db.insert_many(word_list)
