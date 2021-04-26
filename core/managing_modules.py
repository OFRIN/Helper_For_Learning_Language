import time
import queue

from threading import Thread

from .english_modules import Papago, Twinword, Google_Dictionary

from tools.json_utils import read_json

class Manager(Thread):
    def __init__(self, queue, event_fn):
        super().__init__()
        
        self.daemon = True
        self.event_fn = event_fn

        self.info_dic = read_json('./data/private_information.json')

        self.papago = Papago(**self.info_dic['papago'])
        self.twinword = Twinword(**self.info_dic['twinword'])
        self.google_dict = Google_Dictionary()

        self.queue = queue
    
    def run(self):
        while True:
            try:
                text = self.queue.get_nowait()
            except queue.Empty:
                time.sleep(0.1)
                continue
            
            result = self.google_dict.get(text)
            self.event_fn(result)
            
            # result = self.google_dict.get(text)
            # self.print_fn(result)
            
            # if check_string_type(text):
            #     text = preprocessing_for_string(text)

            #     if len(text) > 0:
            #         # 1. word or sentence
            #         if check_sentence_or_word(text):
            #             # 1.1. [sentence] korean or english
            #             if check_korean_sentence(text):
            #                 result = self.papago.ko2en_translate(text)
            #             else:
            #                 result = self.papago.en2ko_translate(text)

            #         else:
            #             # 2.1. [Word] korean or english
            #             if check_korean_sentence(text):
            #                 result = self.papago.ko2en_translate(text)
            #                 result = self.twinword.get(result)
            #             else:
            #                 result = self.twinword.get(text)

            #         self.print_fn(result)