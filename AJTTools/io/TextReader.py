from io import StringIO

class TextFileReader:
    def __init__(self,filepath,encoding):
        self.filepath = filepath
        self.encoding = encoding

    def __enter__(self):
        self.file = open(self.filepath,mode='r',encoding=self.encoding)
        self.read = self.file.read
        self.tell = self.file.tell
        self.seek = self.file.seek
        return self

    def __exit__(self,exc_type, exc_val, exc_tb):
        self.file.close()
    
    def readUntilOccurrence(self,occurrence : str) -> str:
        data = ""
        char = self.read(1)
        while char != occurrence and char != "":
            data += char
            char = self.read(1)
        if char == "":
            raise EOFError("Error while reading text file: EOF reached")
        return data
    
    def readUntilOccurrenceOrEOFSkipCR(self,occurrence : str) -> str:
        data = ""
        char = self.read(1)
        while char != occurrence and char != "":
            if char not in ['\n','\r']:
                data += char
            char = self.read(1)
        return data, char == ""
    
    def readUntilOccurrenceOrEOF(self,occurrence : str) -> str:
        data = ""
        char = self.read(1)
        while char != occurrence and char != "":
            data += char
            char = self.read(1)
        return data, char == ""
    

class TextStreamReader:
    def __init__(self,string : str):
        self.stream = StringIO(string)
        self.read = self.stream.read
        self.tell = self.stream.tell
        self.seek = self.stream.seek
        self.getvalue = self.stream.getvalue
    
    def readUntilOccurrence(self,occurrence : str) -> str:
        data = ""
        char = self.read(1)
        while char != occurrence and char != "":
            data += char
            char = self.read(1)
        if char == "":
            raise EOFError("Error while reading text file: EOF reached")
        return data
    
    def readUntilOccurrenceOrEOFSkipCR(self,occurrence : str) -> str:
        data = ""
        char = self.read(1)
        while char != occurrence and char != "":
            if char not in ['\n','\r']:
                data += char
            char = self.read(1)
        return data, char == ""
    
    def readUntilOccurrenceOrEOF(self,occurrence : str) -> str:
        data = ""
        char = self.read(1)
        while char != occurrence and char != "":
            data += char
            char = self.read(1)
        return data, char == ""