class Person:
    def fun(self,a):
        return a
    
    def fun(self,a,b):
        return a+b
    
class Customer(Person):
    def fun(self,a):
        return a*2