import datetime as dt

def convert_filenumber_to_str(filenumber):

        string = str(filenumber)
        strlength = len(string)
        result = "0" * (3-strlength) + string
        return result


print(convert_filenumber_to_str()))