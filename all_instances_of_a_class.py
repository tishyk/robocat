Python does not keep track of all instances of a class (or of a built-in type), so if you need this functionality, you have to implement it yourself. One way to do it is to store a weak reference to each instance in class attribute. Here’s an example:

import weakref

class MyClass:

    _instances = set()

    def __init__(self, name):
        self.name = name
        self._instances.add(weakref.ref(self))

    @classmethod
    def getinstances(cls):
        dead = set()
        for ref in cls._instances:
            obj = ref()
            if obj is not None:
                yield obj
            else:
                dead.add(ref)
        cls._instances -= dead

a = MyClass("a")
b = MyClass("b")
c = MyClass("c")

del b

for obj in MyClass.getinstances():
    print obj.name # prints 'a' and 'c'
An simpler, brute-force approach is to ask the gc module for a list of all known objects, and filter out the objects that belong to the relevant class:

import gc

for obj in gc.get_objects():
    if isinstance(obj, MyClass):
        print obj.name
However, since an application is likely to have thousands of active objects, this variant isn’t very efficient.
