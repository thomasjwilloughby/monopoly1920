from typing import Callable, Self
import weakref
#the following code draws inspiration
#from: https://stackoverflow.com/questions/1904351/python-observer-pattern-examples-tips

class Observer:
    """Observer class to represent an observer that can observe events"""

    #static attribute
    _observers: list[weakref.ref[Self]] = []

    def __init__(self):
        """Constructor for the Observer class"""
        self._observers.append(weakref.ref(self))

        #things that can be observed
        self._observables: dict[str, str] = {}

    def __del__(self):
        print(f"Removing Observer {self}")
        try:
            self._observers.remove(weakref.ref(self))
        except:
            ...

    # Store callback names instead of bound methods to ensure Observers cab be garbage collected
    # bound methods keep strong refreces to thier object which in this case causes a refrence loop
    def observe(self, event_name, callback_name):
        """Function to observe an event
        :param event_name: the name of the event to observe
        :param callback: the name of the method to call when the event occurs
        """

        # Ensure callback_name exists on self object and is callable
        if callable(getattr(self, callback_name)):
            self._observables[event_name] = callback_name
        else:
            raise ValueError("callback name must match an existing callable attribute on self (ie. a method)")

    @property
    def observables(self):
        return self._observables

    @staticmethod
    def get_observers():
        """Function to get all observers"""
        return Observer._observers

class Event:
    """Event class to represent an event that can be observed"""

    def __init__(self, event_name, data):
        """Constructor for the Event class"""
        self.__name = event_name
        self.__data = data
        print(f"Event created: {self.__name}")
        self.notify()

    def notify(self):
        """Function to fire the event"""
        for observer in Observer.get_observers():
            observer = observer()
            if self.__name in observer.observables.keys():
                callback: Callable = getattr(observer, observer.observables[self.__name])
                callback(self.__data)



