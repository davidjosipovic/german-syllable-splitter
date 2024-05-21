from flask import Flask, request
import re
import string
from split_words import Splitter
from spylls.hunspell import Dictionary
import json

app = Flask(__name__)
splitter = Splitter()
dictionary = Dictionary.from_files('dictionary/de_DE')


@app.route("/api/python", methods=["POST"])
def syllableSplitter():
    request_data = request.get_json()
    input=request_data['input']

    def is_german(word):
        if word=="Ans" or word=="An" or word=="und":
            return False
        if word=="Ich" or word=="ich":
            return False
        if word=="Etsch":
            return False
        return dictionary.lookup(string.capwords(word))

    def split_and_check_german_compounds(word, depth=2):
        bad_words=["Nationen,und"]
        compounds = []
        if word in bad_words:
            return [word]
        splits = splitter.split_compound(word)
    
        if not splits or depth == 0:
            return []

        for i in range(min(len(splits), 3)):
            first_part = splits[i][1]
            second_part = splits[i][2]
            if first_part == second_part:
                return [first_part]
            
        
            if ((((is_german(first_part) or is_german(first_part[:-1])) or is_german(second_part)) and depth==2 and len(first_part)+len(second_part)>=13) or ((is_german(first_part) or is_german(first_part[:-1])) and is_german(second_part))):
                first_split = split_and_check_german_compounds(first_part, depth - 1)
                second_split = split_and_check_german_compounds(second_part, depth - 1)

                if first_split and second_split:
                    compounds.extend(first_split)
                    compounds.extend(second_split)
                else:
                    compounds.append(first_part)
                    compounds.append(second_part)
                break

        if compounds == []:
            compounds = [word]
        return compounds



    def split_sentence_and_check_german_compounds(sentence):
        words = re.findall(r"[\w']+|[.,!?;:]", sentence)
        final_splits = []
        for word in words:
            if word.isalnum():
                final_split = split_and_check_german_compounds(word)
                final_splits.extend(final_split)
            else:
                final_splits.append(word)
        return final_splits

    def separate_prefix(word):
        prefixes = ["an", "ab", "auf", "aus", "dis", "ein", "fehl", "her", "hin", "haupt", "in", "dar", "durch",
                    "los", "mit", "nach","ge","leb", "von", "vor", "weg", "um", "un", "ur", "ent", "er", "ver", "zer", "miss",
                    "miß", "niss", "niß", "ex", "non", "super", "trans", "kon", "hoch", "stink", "stock", "tief",
                    "tod", "erz", "unter", "über", "hinter", "wider", "wieder", "weiter", "zurück", "zurecht",
                    "zusammen", "hyper", "inter"]

        for prefix in prefixes:
            if word.startswith(prefix) and word[len(prefix):]!="ssen" and word[len(prefix):]!="ts" and word[len(prefix):]!="er" and word!="und" :
                return [prefix, word[len(prefix):]]

        return ["", word]

    def split_word_into_syllables(word):
        
        vowels = ['a', 'e', 'i', 'o', 'u', 'ä', 'ö', 'ü', 'ei', 'ai', 'ey', 'ay', 'eu', 'äu', 'ie', 'au', 'aa', 'ee', 'oo']
        vowelsdouble = ['ei', 'ai', 'ey', 'ay', 'eu', 'äu', 'ie', 'au', 'aa', 'ee', 'oo']
        consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z', 'ß', 'sch', 'ch', 'ck', 'qu', 'ph']
        new_word = []
        forbidden=['sk','br']
        
        i = 0
        while i < len(word):
            char = word[i]
            char_lower = char.lower()

            if (char_lower == 't' and i < len(word) - 3 and word[i:i+4] == 'tsch' and i==0) or (char_lower == 'h' and i > 0 and word[i-1:i+3] == 'tsch' and i==0) :
                new_word.append('tsch')
                i += 4
                continue


            if char_lower == 's' and i < len(word) - 2 and word[i+1:i+3] == 'ch':
                new_word.append('sch')
                i += 3
                continue

            sequence = char_lower
            j = i + 1
            while j < len(word) and sequence in vowels + consonants and sequence + word[j].lower() in vowels + consonants:
                sequence += word[j].lower()
                j += 1

            new_word.append(sequence)
            i = j
        
        # VCCV->VC-CV
        i=0
        while i<(len(new_word)- 3):
            if new_word[i] in vowels and new_word[i+1] in consonants and new_word[i+2] in consonants and new_word[i+3] in vowels and new_word[i+1]+new_word[i+2] not in forbidden:
                new_word = new_word[:i+2] + ['-'] + new_word[i+2:]
                continue
            i+=1
        
        

        # VCCCV->VCC-CV
        i=0
        while i<(len(new_word)- 4):
            if new_word[i] in vowels and new_word[i+1] in consonants and new_word[i+2] in consonants and new_word[i+3] in consonants and new_word[i+3] in vowels:
                new_word = new_word[:i+3] + ['-'] + new_word[i+3:]
                continue
            i+=1

        # VCV->V-CV
        i=0
        while i<(len(new_word)- 2):
            if new_word[i] in vowels and new_word[i+1] in consonants and new_word[i+2] in vowels and (i!=0 or new_word[i] in vowelsdouble):
                new_word = new_word[:i+1] + ['-'] + new_word[i+1:]
                continue
            i+=1

        # VstV->Vs-tV
        i=0
        while i<(len(new_word)- 3):
            if new_word[i] in vowels and new_word[i+1]=="s" and new_word[i+2]=="t" and new_word[i+3] in vowels:
                new_word = new_word[:i+2] + ['-'] + new_word[i+2:]
                continue
            i+=1

        # VCstV->VCs-tV
        i=0
        while i<(len(new_word)- 4):
            if new_word[i] in vowels and new_word[i+1] in consonants and new_word[i+2]=="s" and new_word[i+3]=="t" and new_word[i+4] in vowels:
                new_word = new_word[:i+3] + ['-'] + new_word[i+3:]
                continue
            i+=1
        
        # VstCV->Vs-tCV
        i=0
        while i<(len(new_word)- 4):
            if new_word[i] in vowels and new_word[i+1]=="s" and new_word[i+2]=="t" and new_word[i+3] in consonants and new_word[i+4] in vowels:
                new_word = new_word[:i+2] + ['-'] + new_word[i+2:]
                continue
            i+=1

        # VxtCV->Vx-tCV
        i=0
        while i<(len(new_word)- 4):
            if new_word[i] in vowels and new_word[i+1]=="x" and new_word[i+2]=="t" and new_word[i+3] in consonants and new_word[i+4] in vowels:
                new_word = new_word[:i+2] + ['-'] + new_word[i+2:]
                continue
            i+=1

        # VtzV->Vt-zV
        i=0
        while i<(len(new_word)- 3):
            if new_word[i] in vowels and new_word[i+1]=="t" and new_word[i+2]=="z" and new_word[i+3] in vowels:
                new_word = new_word[:i+2] + ['-'] + new_word[i+2:]
                continue
            i+=1

        # VCtzV->VCt-zV
        i=0
        while i<(len(new_word)- 4):
            if new_word[i] in vowels and new_word[i+1] in consonants and new_word[i+2]=="t" and new_word[i+3]=="z" and new_word[i+4] in vowels:
                new_word = new_word[:i+3] + ['-'] + new_word[i+3:]
                continue
            i+=1

        # VtzCV->Vtz-CV
        i=0
        while i<(len(new_word)- 4):
            if new_word[i] in vowels and new_word[i+1]=="t" and new_word[i+2]=="z" and new_word[i+3] in consonants and new_word[i+4] in vowels:
                new_word = new_word[:i+3] + ['-'] + new_word[i+3:]
                continue
            i+=1

        # VpfV->Vp-fV
        i=0
        while i<(len(new_word)- 3):
            if new_word[i] in vowels and new_word[i+1]=="p" and new_word[i+2]=="f" and new_word[i+3] in vowels:
                new_word = new_word[:i+2] + ['-'] + new_word[i+2:]
                continue
            i+=1

        # VCpfV->VCp-fV
        i=0
        while i<(len(new_word)- 4):
            if new_word[i] in vowels and new_word[i+1] in consonants and new_word[i+2]=="p" and new_word[i+3]=="f" and new_word[i+4] in vowels:
                new_word = new_word[:i+3] + ['-'] + new_word[i+3:]
                continue
            i+=1

        
        # VpfCV->Vpf-CV
        i=0
        while i<(len(new_word)- 4):
            if new_word[i] in vowels and new_word[i+1]=="p" and new_word[i+2]=="f" and new_word[i+3] in consonants and new_word[i+4] in vowels:
                new_word = new_word[:i+3] + ['-'] + new_word[i+3:]
                continue
            i+=1

        # CVVC->CV-VC
        i=0
        while i<(len(new_word)- 3):
            if new_word[i] in consonants and new_word[i+1] in vowels and new_word[i+2] in vowels and new_word[i+3] in consonants:
                new_word = new_word[:i+2] + ['-'] + new_word[i+2:]
                continue
            i+=1
        
    # VCCV->V-CCV
        i=0
        while i<(len(new_word)- 3):
            if new_word[i] in vowels and new_word[i+1] in consonants and new_word[i+2] in consonants and new_word[i+3] in vowels:
                new_word = new_word[:i+1] + ['-'] + new_word[i+1:]
                continue
            i+=1
        
        # 2 ista suglasnika u sredini riječi se dijele
        i=0
        while i<(len(new_word)- 3):
            if new_word[i+1] in consonants and new_word[i+2] in consonants and new_word[i+1]== new_word[i+2] :
                new_word = new_word[:i+2] + ['-'] + new_word[i+2:]
                continue
            i+=1


        new_word_string=""
        for el in new_word:
            new_word_string+=el
        return new_word_string.replace("-"," ")

    def finish_word(word):
        prefix, suffix = separate_prefix(word)
        prefix2, suffix = separate_prefix(suffix)

        prefix=split_word_into_syllables(prefix)
        prefix2=split_word_into_syllables(prefix2)
        separated_suffix = split_word_into_syllables(suffix)

        if prefix != "" and prefix2 != "":
            separated_word = prefix + " " + prefix2 + " " + separated_suffix
        elif prefix != "" and prefix2 == "":
            separated_word = prefix + " " + separated_suffix
        else:
            separated_word = separated_suffix

        return separated_word

    # Define the sentence

    # Call the function to split and check if the parts are German
    final_splits = split_sentence_and_check_german_compounds(input)
    # Apply syllable splitting to every word in the sentence
    final_splits_syllable = [finish_word(word.lower()) for word in final_splits]
    final_splits_syllable=" ".join(final_splits_syllable)
    final_splits_syllable=re.sub(r'\s{2,}', ' ', final_splits_syllable)
    final_splits_syllable = re.sub(r'\s+([.,!?;:])', r'\1', final_splits_syllable)
    # Join the splits into a single string with spaces
    final_splits_syllable=json.dumps(final_splits_syllable)
    # Join the splits into a single string with spaces
    print(final_splits_syllable)
    

    return final_splits_syllable