from model.mongodb import conn_mongodb
from random import *
import math
from bson.objectid import ObjectId


class Kanji:    
    @staticmethod
    def get_kanji_list(level, num):
        db = conn_mongodb()        
        total_count = db.count_documents({ '$and': [{'level': level}, {'kanji': { '$ne': None }}]})
        skipping_size = math.floor(random() * (total_count - num))
        skipping_size = skipping_size if skipping_size > 0 else 1
        
        word_li = db.find({ '$and': [{'level': level}, {'kanji': { '$ne': None }}]}).skip(skipping_size).limit(10)
        result_li = list()
        
        for word in word_li:
            row_id = word['_id']
            n_level = word['level']
            furigana = word['furigana']
            kanji = word['kanji']
            
            result_li.append([row_id, n_level, furigana, kanji])

        return result_li
    
    @staticmethod
    def get_hint(row_id):
        db = conn_mongodb()
        result = db.find_one({'_id': ObjectId(row_id)})
        first_word = result['furigana'][0:1]
        
        return {
            'first_word': first_word,
            'hint_len': len(result['furigana'])
        }
        
    @staticmethod
    def check_answer(user_answer):
        db = conn_mongodb()
        answer_list = list()
        
        for key in user_answer.keys():
            u_answer = user_answer[key][0].strip()
            obj_id = user_answer[key][1]
            
            answer = db.find_one({'_id': ObjectId(obj_id)})['furigana']       
            
            if u_answer == answer:
                answer_list.append('o')
            else:
                answer_list.append('x')
        
        return answer_list
            

class Quiz:
    @staticmethod
    def get_word_list(level, num): 
        db = conn_mongodb()
        total_count = db.count_documents({'level': level})
        skipping_size = math.floor(random() * (total_count - num))
        skipping_size = skipping_size if skipping_size > 0 else 1
        
        word_li = db.find({'level': level}).skip(skipping_size).limit(10)
        result_li = list()
        
        for word in word_li:
            row_id = word['_id']
            n_level = word['level']
            furigana = word['furigana']
            kanji = word['kanji'] if word['kanji'] != None else '-'
            
            result_li.append([row_id, n_level, furigana, kanji])

        return result_li
    
    @staticmethod
    def check_answer(user_answer):
        print(user_answer)
        
        db = conn_mongodb()
        answer_list = list()
        
        for key in user_answer.keys():
            u_answer = user_answer[key][0].strip()
            obj_id = user_answer[key][1]
            
            meanings = db.find_one({'_id': ObjectId(obj_id)})['meanings']
            
            if u_answer in meanings:
                answer_list.append('o')
            else:
                answer_list.append('x')
        
        return answer_list