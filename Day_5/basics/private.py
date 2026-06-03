class Person:
  def __init__(self, name, age):
    self.name = name
    self.__age = age # Private property

  def get_age(self):
    return self.__age
  
p1 = Person("Emil", 25)
print(p1.name)
print(p1.get_age()) # This will cause an error