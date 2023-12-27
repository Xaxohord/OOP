import numpy as np
from abc import ABC, abstractmethod
#код определяет абстрактный базовый класс Интеграл и два его подкласса - Sympsons и Trapeze
#Оба они реализуют метод calc()  который вычисляет приближенное значение определенного интеграла 
#для указанной функции f на промежутке [low, up] с использованием метода Симпсона и метода Трапеции
#__init__ является конструктором класса. Он присваивает функции f верхний и нижний предел
# self является объектом. self используется для сохранения аргументов, переданных в конструктор,
# и для обращения к этим атрибутам в методах calc
class Integral(ABC):
    def __init__(self, f, low, up):
        self.f = f
        self.low = low
        self.up = up

    @abstractmethod
    def calc(self):
        pass

class Sympsons(Integral):
    def calc(self):
        return (self.up - self.low) * (self.f(self.up) + self.f(self.low) + 4 * self.f((self.up + self.low) / 2)) / 6

class Trapeze(Integral):
    def calc(self):
        total = 0
        arr = np.linspace(self.low, self.up, num=10**6)
        for i in arr:
            total += 2 * self.f(i)
        return (arr[1] - arr[0]) * (total - self.f(arr[0]) - self.f(arr[-1])) / 2



#Выведет приближенное значение определенного интеграла функции sin(x) на промежутке [0, π]
#как методом Симпсона так и методом Трапеции
import math

def func(x):
    return math.sin(x)

s = Sympsons(func, 0, math.pi)
result_s = s.calc()

t = Trapeze(func, 0, math.pi)
result_t = t.calc()

print("Simpson's method:", result_s)
print("Trapezoidal method:", result_t)
