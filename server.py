from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory=".")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

morse_code = {
    'a': '.-','b': '-...',   
    'c': '-.-.','d': '-..',    
    'e': '.','f': '..-.',   
    'g': '--.','h': '....',   
    'i': '..','j': '.---',
    'k': '-.-','l': '.-..',   
    'm': '--','n': '-.',     
    'o': '---','p': '.--.',   
    'q': '--.-','r': '.-.',    
    's': '...','t': '-',
    'u': '..-','v': '...-',   
    'w': '.--','x': '-..-',   
    'y': '-.--','z': '--..',   
    '0': '-----','1': '.----',
    '2': '..---','3': '...--',  
    '4': '....-','5': '.....',  
    '6': '-....','7': '--...',  
    '8': '---..','9': '----.',
    '.': '.-.-.-',',': '--..--',
    '?': '..--..',"'": '.----.',
    '!': '-.-.--','/': '-..-.',
    '(': '-.--.',')': '-.--.-',
    '&': '.-...',':': '---...',
    ';': '-.-.-.','=': '-...-',
    '+': '.-.-.','-': '-....-',
    '_': '..--.-','"': '.-..-.',
    '$': '...-..-','@': '.--.-.',
    ' ': '//'
}

morse_to_text = {v: k for k, v in morse_code.items()}

def shifting(word, mode, key):
    alphabets, digits = "abcdefghijklmnopqrstuvwxyz", "0123456789"
    full_set = alphabets + digits
    shifted_text, counter = [], 0

    for letter in word:
        if letter in alphabets or letter in digits:
            index = alphabets.index(letter) if letter in alphabets else digits.index(letter)

            key_x = key[counter % len(key)]

            if key_x in alphabets:
                shifting_value = alphabets.index(key_x)
                counter += 1
            elif key_x in digits:
                shifting_value = int(key_x)
                counter += 1
            else:
                shifting_value = 0    

            if mode == "encryption":
                if letter in alphabets:
                    shifted_text.append(alphabets[(index + shifting_value) % len(alphabets)])
                else:
                    shifted_text.append(digits[(index + shifting_value) % len(digits)])
            elif mode == "decryption":
                if letter in alphabets:
                    shifted_text.append(alphabets[(index - shifting_value) % len(alphabets)])
                else:
                    shifted_text.append(digits[(index - shifting_value) % len(digits)])
        else:
            shifted_text.append(letter)

    return "".join(shifted_text)

def convert_morse(text_O, mode):
    text = []

    if mode == "encryption":
        for letter in text_O:
            if letter in morse_code:
                text.append(morse_code[letter])
            else:
                text.append(letter)
        return "/".join(text)
    elif mode == "decryption":
        text_O = text_O.replace(" ", "//")
        parts = text_O.split("/")
        for letter in parts:
            if letter in morse_to_text:
                text.append(morse_to_text[letter])
            elif letter == "":
                text.append(" ")
            else:
                text.append(letter)
        return "".join(text)

def morse_to_0_1(text, mode):
    text_O = []

    if mode == "encryption":
        for item in text:
            for letter in item:
                if letter == ".":
                    text_O.append("0")
                elif letter == "-":
                    text_O.append("1")
                elif letter == "/":
                    text_O.append("/")
                else:
                    text_O.append(letter)
    elif mode == "decryption":
        for letter in text:
            if letter == "0":
                text_O.append(".")
            elif letter == "1":
                text_O.append("-")
            elif letter == "/":
                text_O.append("/")
            elif letter == " ":
                text_O.append(" ")
            else:
                text_O.append(letter)
    return "".join(text_O)

def interchange_0_1(text, mode):
    text_O = []

    for item in text:
        if item == "0":
            text_O.append("1")
        elif item == "1":
            text_O.append("0")
        elif item == "/":
            text_O.append("/")
        elif item == " ":
            text_O.append(" ")
        else:
            text_O.append(item)

    return "".join(text_O)

def reversing(text, mode):
    parts = text.split("/")
    text_reverse = [part[::-1] for part in parts] 
    return "/".join(text_reverse)

def encryption(text, mode, key): 
    shiftingx = shifting(text, mode, key)  
    text_morse = convert_morse(shiftingx, mode)
    convert_0 = morse_to_0_1(text_morse, mode) 
    interchange_0 = interchange_0_1(convert_0, mode)
    encrypted_text = reversing(interchange_0, mode).replace("////", "//")
    return encrypted_text

def decryption(text, mode, key):
    text_reverse = reversing(text, mode)
    text_interchange = interchange_0_1(text_reverse, mode)
    text_morse = morse_to_0_1(text_interchange, mode)
    shifted_text = convert_morse(text_morse, mode)
    decrypted_text = shifting(shifted_text, mode, key)
    return decrypted_text


@app.post("/send")
async def receive_data(data: dict):
    text = data["text"]
    key = data["key"]
    mode = data["mode"]
    if mode == "encryption":
        print(encryption(text, mode, key))
        return {"encrypted_text": encryption(text, mode, key)}
    elif mode == "decryption":
        print(decryption(text, mode, key))
        return {"decrypted_text": decryption(text, mode, key)}

if "__main__" == "__name__":
    app.run()
