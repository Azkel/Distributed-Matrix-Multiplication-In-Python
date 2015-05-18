_author__ = 'Michal Smyk'

import numpy.matlib
import random
import sys
import time
import math
import Pyro4


class ClientClass:
    def __init__(self):
        self.array = None

    def shift_a_matrix_left(self):
        for element in self.array:
            current_element = element[0].get_matrix_a()
            for el in reversed(element):
                temp = el.get_matrix_a()
                el.set_matrix_a(current_element)
                current_element = temp

    def shift_b_matrix_up(self, vector_length, block_count):
        for i in range(0, block_count):
            current_element = self.array[0][i].get_matrix_b()
            for element in reversed(self.array):
                temp = element[i].get_matrix_b()
                element[i].set_matrix_b(current_element)
                current_element = temp

    def skew(self, vector_length):
        for i in range(1, vector_length):
            current_element = self.array[0][i].get_matrix_b()
            for element in reversed(self.array):
                temp = element[i].get_matrix_b()
                element[i].set_matrix_b(current_element)
                current_element = temp
        for i in range(1, vector_length):
            current_element = self.array[i][0].get_matrix_a()
            for el in reversed(self.array[i]):
                temp = el.get_matrix_a()
                el.set_matrix_a(current_element)
                current_element = temp

    def generate_matrix(self, n, k):
        result = ''
        for x in range(0, n):
            for y in range(0, n):
                result += str(random.randint(0, k))+','
            result = result[:-1]+';'
        return result[:-1]

    def split_matrix(self, input_matrix, block_count, block_size):
        result_matrix = []
        for x in range(0, block_count):
            temporary_array = []
            for y in range(0, block_count):
                x_value = int(block_size*x)
                x_second_value = int(block_size*(x+1))
                y_value = int(block_size*y)
                y_second_value = int(block_size*(y+1))
                temporary_array.append(input_matrix[x_value:x_second_value, y_value:y_second_value])
            result_matrix.append(temporary_array)
        return result_matrix

    def get_result_matrix(self, size):
        result = []
        for element in self.array:
            temp = None
            for arr in element:
                if temp is None:
                    temp = arr.get_c_matrix()
                else:
                    matrix = arr.get_c_matrix()
                    temp = numpy.append(temp, matrix, axis=1)
            result.append(temp)
        result = numpy.append(*result, axis=0)
        print result

    def run(self, machineNumber, port_number, generator_from, generator_to):
        servers = ['PYRO:matrix@someserver.org:', 'PYRO:matrix@someotherserver.org:']
        machineNumber = int(machineNumber)
        block_size = int(array_size/machineNumber)
        block_count = int(array_size/block_size)
        numpy.set_printoptions(threshold=numpy.nan)
        matrix_a = numpy.matlib.matrix(self.generate_matrix(array_size, generator_from, generator_to))
        matrix_b = numpy.matlib.matrix(self.generate_matrix(array_size, generator_from, generator_to))
        matrixA = self.split_matrix(matrix_a, block_count, block_size)
        matrixB = self.split_matrix(matrix_b, block_count, block_size)
        Pyro4.config.SERIALIZER = "pickle"
        machine_count = 0
        self.array = []
        for x in range(0, block_count):
            temp_array = []
            for y in range(0, block_count):
                url = servers[machine_count % 2]+str(port_number)
                matrix = Pyro4.Proxy(url)
                matrix.clear_c_matrix()
                matrix.set_matrix_a(matrixA[x][y])
                matrix.set_matrix_b(matrixB[x][y])
                temp_array.append(matrix)
                machine_count += 1
                if machine_count % 2 == 0:
                    port_number += 1
            self.array.append(temp_array)
        self.skew(block_count)
        for i in range(0, machineNumber):
            for element in self.array:
                for value in element:
                    value.multiply()
            self.shift_a_matrix_left()
            self.shift_b_matrix_up(block_size, block_count)
        self.get_result_matrix(block_size)
        print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    start_time = time.time()
    port_number = 9601
    machineNumber = float(sys.argv[1])
    machineNumber = math.sqrt(machineNumber)
    array_size = int(sys.argv[2])
    if machineNumber.is_integer() and array_size % machineNumber == 0:
        client = ClientClass()
        client.run(machineNumber, port_number, int(sys.argv[3]), int(sys.argv[4]))
    else:
        print('Square root of machines count must be an integer!')
