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
                
                furigana_list = list()
                kanji_list = list()
                
                for detail in detail_data:
                    tags = str(detail).split('<')          
                    
                    furigana_full = list()
                    kanji_full = list()
                    
                    tags_str = str(detail)
                    
                    if tags_str.find('furigana') == -1 and tags_str.find('f_kanji') == -1:
                        pattern = re.compile(r'>(.*?)</a>')
                        pure_hiragana = pattern.findall(tags_str)[0]
                        
                        furigana_list.append(pure_hiragana)
                        kanji_list.append(None)
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
                        'level': 5 - i,
                        'furigana': furigana_word,
                        'kanji': kanji_word
                    })
                
        db = conn_mongodb()
        db.insert_many(word_list)
        

