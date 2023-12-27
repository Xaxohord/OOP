import math
#определяем класс Поинт
class Point: 
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
#Определяем класс Вектор и добавляем ему методы
class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        
    #сложение    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
    
    #вычитание
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
    
    #обратный вектор
    def inverse(self):
        return Vector(-self.x, -self.y, -self.z)
    
    #скалярное произведение 2х векторов
    def scalar_product(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    #векторное произведение 
    def vector_product(self, other):
        x = self.y * other.z - self.z * other.y
        y = self.z * other.x - self.x * other.z
        z = self.x * other.y - self.y * other.x
        return Vector(x, y, z)
    
    #смешанное произведение
    def mixed_product(self, b, c):
        return self.scalar_product(b.vector_product(c))
    
    #длина
    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    
    #единичный вектор
    def normalize(self):
        magnitude = self.magnitude()
        return Vector(self.x / magnitude, self.y / magnitude, self.z / magnitude)
    
    #угол между векторами
    def angle_between(self, other):
        cosine_angle = self.scalar_product(other) / (self.magnitude() * other.magnitude())
        return math.acos(cosine_angle)
    
    #коллинеарность(пропорциональные стороны)
    def are_collinear(self, other):
        return self.vector_product(other).magnitude() == 0
    
    #компланарность(смешанное произведение =0)
    def are_coplanar(self, b, c):
        return self.mixed_product(b, c) == 0
    
    #создание вектора из 2х точек
    @staticmethod
    def from_points(p1, p2):
        return Vector(p2.x - p1.x, p2.y - p1.y, p2.z - p1.z)
    
    #расстояние между векторами
    @staticmethod
    def distance_between(p1, p2):
        return Vector.from_points(p1, p2).magnitude()

def parse_input(input_str):
    x, y, z = map(float, input_str.split(','))
    return x, y, z

def main():
    while True:
        print('Выберите операцию:\n'
              '1. Сложение\n'
              '2. Вычитание\n'
              '3. Скалярное произведение\n'
              '4. Векторное произведение\n'
              '5. Коллинеарность\n'
              '6. Компланарность\n'
              '7. Угол между векторами\n'
              '8. Выход')
        choice = input('Введите номер операции: ')
        
        if choice == '8':
            break

        v1_input = input('Введите координаты вектора 1 (формат: x,y,z): ')
        x, y, z = parse_input(v1_input)
        v1 = Vector(x, y, z)
        
        if choice in ['1', '2', '3', '4', '5', '7']:
            v2_input = input('Введите координаты вектора 2 (формат: x,y,z): ')
            x, y, z = parse_input(v2_input)
            v2 = Vector(x, y, z)

        if choice == '1':
            result = v1.__add__(v2)
            print(f'Результат: {result.x}, {result.y}, {result.z}')
        elif choice == '2':
            result = v1.__sub__(v2)
            print(f'Результат: {result.x}, {result.y}, {result.z}')
        elif choice == '3':
            result = v1.scalar_product(v2)
            print(f'Результат: {result}')
        elif choice == '4':
            result = v1.vector_product(v2)
            print(f'Результат: {result.x}, {result.y}, {result.z}')
        elif choice == '5':
            result = v1.are_collinear(v2)
            print(f'Результат: {result}')
        elif choice == '7':
            angle = v1.angle_between(v2)
            print(f'Результат: {math.degrees(angle)} градусов')
        elif choice == '6':
            v2_input = input('Введите координаты вектора 2 (формат: x,y,z): ')
            x, y, z = parse_input(v2_input)
            v2 = Vector(x, y, z)
            v3_input = input('Введите координаты вектора 3 (формат: x,y,z): ')
            x, y, z = parse_input(v3_input)
            v3 = Vector(x, y, z)
            result = v1.are_coplanar(v2, v3)
            print(f'Результат: {result}')

if __name__ == '__main__':
    main()

    
