from core.english_modules import Manager

if __name__ == '__main__':
    option = {
        'print_fn' : print
    }
    manager = Manager(**option)
    manager.start()

    while True:
        manager.push(input())

# from multiprocessing import Process, Queue
# import random

# def rand_num():
#     num = random.random()
#     print(num)

# if __name__ == "__main__":
#     queue = Queue()
    
#     processes = [Process(target=rand_num, args=()) for x in range(4)]

#     for p in processes:
#         p.start()

#     for p in processes:
#         p.join()