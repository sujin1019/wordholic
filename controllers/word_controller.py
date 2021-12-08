from flask import Flask
from model.mongodb import conn_mongodb
from random import *
import math


class Kanji:    
    @staticmethod
    def get_kanji_list(level, num):
        db = conn_mongodb()        
        total_count = db.find({'level': level}).count()
        skipping_size = math.floor(random() * (total_count - num))
        skipping_size = skipping_size if skipping_size > 0 else 1 
        word_li = db.find({'level': level}).skip(skipping_size).limit(10)
        
        result_li = list()
        
        for word in word_li:
            n_level = word['level']
            furigana = word['furigana']
            kanji = word['kanji']
            
            result_li.append([n_level, furigana, kanji])

        return result_li
    