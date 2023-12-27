class Array3d:
    def __init__(self, dim0, dim1, dim2):
        self.dim0 = dim0   #ширина
        self.dim1 = dim1   #высота
        self.dim2 = dim2   #глубина
        self.length = dim0*dim1*dim2
        self.arr = [0]*self.length

    def __str__(self):  # Преобразовываем написание массива
        result = ""
        for i in range(self.dim0):
            result += f"Глубина: {i}\n"
            for j in range(self.dim1):
                for k in range(self.dim2):
                    result += f"{self.arr[self.transform_index(i, j, k)]} "
                result += "\n"
            result += "\n"
        return result

    def transform_index(self, i, j, k):
        return i + self.dim0 * (j + self.dim1 * k)  #перевод индекса

    def GetValues1(self, i):  # Получаем срез по первому приближению = двумерный массив
        result = ""
        for j in range(self.dim1):
            result += "\n"
            for k in range(self.dim2):
                result += f"{self.arr[self.transform_index(i, j, k)]} "
        return result

    def GetValues2(self, i, j):  # Получаем срез по второму приближению = одномерный массив
        result = ""
        for k in range(self.dim2):
            result += f"{self.arr[self.transform_index(i, j, k)]} "
        return result

    def SetValues1(self, i, array):  # Устанавливаем значение в массиве для заданной одной координаты (ставим необходимый двумерный массив)
        for k in range(self.dim2):
            for j in range(self.dim1):
                self.arr[self.transform_index(i, j, k)] = array[k][j]
        return self.arr

    def SetValues2(self, i, j, array):  # Устанавливаем значение в массиве для заданных двух координат (ставим необходимый одномерный массив)
        for k in range(self.dim2):
            self.arr[self.transform_index(i, j, k)] = array[k]
        return self.arr

        # cоздает массив заполненный 1
    def np_ones(self):
            self.arr = [1] * self.length

        # cоздает массив заполненный 0
    def np_zeros(self):
            self.arr = [0] * self.length

        # cоздает массив заполненный определенным числом
    def np_fill(self, value):
            self.arr = [value] * self.length



if __name__ == '__main__':
    array = Array3d(3, 3, 3)
    array.SetValues1(0, [[1,2,3],[2,3,1],[3,1,2]])
    array.SetValues2(1, 0, [9,9,9])

    print(array.GetValues1(0))
    print("-----------------")
    print(array.GetValues2(0, 2))
    print("-----------------")
    print(array)


