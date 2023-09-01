import pandas as pd
import math



class ExampleClass:

    def __init__(self, number):
        self.number = number


    def add_one(self):
        return self.number + 1


    def power_num(self, pow_num: int):
        return math.pow(self.number, pow_num)