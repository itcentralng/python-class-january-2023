<<<<<<< HEAD
=======
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def bio(self):
        return "Hi my name is {} and I am {} years old".format(self.name, self.age)

person1 = Person('Aisha', 21)
person2 = Person('Halima', 16)

print(person1.bio())
print(person2.bio())

class Teacher(Person):
    def setClass(self, classname):
        self.classname = classname
    
    def classInfo(self):
        return "Hi my name is {} and I teach {}".format(self.name, self.classname)

teacher1 = Teacher("Jamil", 19)
teacher1.setClass("Primary 6")
print(teacher1.bio())
print(teacher1.classInfo())


>>>>>>> d22448d7b8b5873617bdad2bfdcf17ca0e416a33
class Animal:
    def __init__(self, name, type):
        self.name = name
        self.type = type
<<<<<<< HEAD
    class Dog:
        def set_breed(self, breed)
=======
    
class Dogs(Animal):
    def set_breed(self, breed):
        self.breed = breed
# ASSIGMENT
"""
Convert the state and capital game into a class blueprint for those kind of games. Make it work well with a dictionary or state and capital game.
"""
>>>>>>> d22448d7b8b5873617bdad2bfdcf17ca0e416a33
