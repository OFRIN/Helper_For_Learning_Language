import queue
import multiprocessing as mp

from core.papago import Papago
from core.twinword import Twinword

from utility import * 

class Manager(mp.Process):
    def __init__(self, print_fn):
        super().__init__()

        self.daemon=True
        self.print_fn = print_fn

        self.papago = Papago()
        self.twinword = Twinword()

        self.queue = mp.Queue(maxsize=50)

    def push(self, text):
        self.queue.put(text)

    def run(self):
        while True:
            text = self.queue.get()

            if check_string_type(text):
                text = preprocessing_for_string(text)

                if len(text) > 0:
                    # 1. word or sentence
                    if check_sentence_or_word(text):
                        # 1.1. [sentence] korean or english
                        if check_korean_sentence(text):
                            result = self.papago.ko2en_translate(text)
                        else:
                            result = self.papago.en2ko_translate(text)

                    else:
                        # 2.1. [Word] korean or english
                        if check_korean_sentence(text):
                            result = self.papago.ko2en_translate(text)
                            result = self.twinword.get(result)
                        else:
                            result = self.twinword.get(text)

                    self.print_fn(result)