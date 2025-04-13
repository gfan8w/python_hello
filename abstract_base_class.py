import abc
from abc import ABC


class File(ABC):
    @abc.abstractmethod
    def read(self):
        print("None file content")

class Text(File):
    def read(self):
        print("Text file content")


class PDF(File):
    def read(self):
        print("PDF file content")


txt1 = Text()
txt1.read()

#txt2 = File()   # error: Can't instantiate abstract class
                 # if the File class is inherited from ABC and annotated with @abc.abstractmethod
#txt2.read()