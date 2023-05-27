import pandas as pd

def fileHandler(file):
    with open("some/file/name.txt", "wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return type(file)