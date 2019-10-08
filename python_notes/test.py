class User(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def SetName(self, name):
        self.name = name

class Bird:
    def __init__(self):
        self.hungry = True
    def eat(self):
        if self.hungry:
            print('Aaaah ...')
            self.hungry = False
        else:
            print('No,thanks!')
class SongBird(Bird):
    def __init__(self):
        Bird.__init__(self)
        self.sound = 'Squawk!'
    def sing(self):
        print(self.sound)
        return True

sb = SongBird()
sb.eat()