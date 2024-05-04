from flask import Flask
app = Flask(__name__)

def separate_prefixes(word):
    prefixes = ["an", "ab", "auf", "aus", "dis", "ein", "fehl", "her", "hin", "haupt", "in", "dar", "durch",
                "los", "mit", "nach","ge", "von", "vor", "weg", "um", "un", "ur", "ent", "er", "ver", "zer", "miss",
                "miß", "niss", "niß", "ex", "non", "super", "trans", "kon", "hoch", "stink", "stock", "tief",
                "tod", "erz", "unter", "über", "hinter", "wider", "wieder", "weiter", "zurück", "zurecht",
                "zusammen", "hyper", "inter"]

    for prefix in prefixes:
        if word.startswith(prefix) and word[len(prefix)] in 'bcdfghjklmnpqrstvwxyzß':
            return [prefix, word[len(prefix):]]

    return ["",word]

def separate_word(word):
    vowels = 'aeiouäöü'
    consonants = 'bcdfghjklmnpqrstvwxyzß'
    
    # Rastavljanje tsch
    if 'tsch' in word:
        index = word.index('tsch')
        if index == 0:
            return 'tsch ' + word[4:]
        elif index == len(word) - 4:
            return word[:index] + ' tsch'
        else:
            if word[index-1] in vowels:
                return word[:index] + 't sch' + word[index+4:]
            else:
                return word[:index] + ' tsch ' + word[index+4:]

    # Rastavljanje VCCV -> VC-CV
    for i in range(len(word) - 3):
        if word[i] in vowels and word[i+1] in consonants and word[i+2] in consonants and word[i+3] in vowels:
            return word[:i+2] + ' ' + word[i+2:]

    # Rastavljanje VCCCV -> VCC-CV
    for i in range(len(word) - 4):
        if word[i] in vowels and word[i+1] in consonants and word[i+2] in consonants and word[i+3] in consonants and word[i+4] in vowels:
            return word[:i+3] + ' ' + word[i+3:]

    # Rastavljanje VCV -> V-CV
    for i in range(len(word) - 2):
        if word[i] in vowels and word[i+1] in consonants and word[i+2] in vowels:
            return word[:i+1] + ' ' + word[i+1:]

    return word


# Test
word = "abgefahren"
prefix, suffix = separate_prefixes(word)
prefix2, suffix = separate_prefixes(suffix)

separated_suffix = separate_word(suffix)
if(prefix!="" and prefix2!=""):
    separated_word = prefix + " " + prefix2 + " " + separated_suffix
elif(prefix!="" and prefix2==""):
    separated_word = prefix + " " + separated_suffix
else:
    separated_word = separated_suffix


print(f"The separated word is: {separated_word}")


@app.route("/api/python")
def hello_world():
    return separated_word