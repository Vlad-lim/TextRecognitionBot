import easyocr

token = '5506077277:AAHaeQOsRDWRLl7at29L_V7dMjBXDFRJOWI'

YouKassaToken = '381764678:TEST:38107'

def Text_recognition(src):

    reader = easyocr.Reader(['en', 'ru'])
    result = reader.readtext(src, detail=0, paragraph=True)

    return result

