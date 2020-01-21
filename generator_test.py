from time import sleep
from functools import wraps


# 协程预激装饰器
def coroutine(fn):

    @wraps(fn)
    def wrapper(*args, **kwargs):
        gen = fn(*args, **kwargs)
        next(gen)
        return gen

    return wrapper

# 生成器 - 数据生产者
def countdown_gen(n, consumer):
    consumer.send(None)
    while n > 0:
        consumer.send(n)
        n -= 1
    consumer.send(None)


# 生成器 - 数据生产者，装饰器版
def countdown_gen1(n, consumer):
    #consumer.send(None)
    while n > 0:
        consumer.send(n)
        n -= 1
    consumer.send(None)


# 协程 - 数据消费者
@coroutine
def countdown_con():
    while True:
        n = yield
        print(f't {n}')
        if n:
            print(f'Countdown {n}')
            sleep(1)
        else:
            print('Countdown Over!')


def main():
    countdown_gen1(5, countdown_con())


if __name__ == '__main__':
    main()