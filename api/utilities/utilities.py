from spylls.hunspell import Dictionary
from split_words import Splitter

dictionary = Dictionary.from_files('dictionary/de_DE')
splitter = Splitter()

def is_german(word):
    true_bases = ["sonn", "lich", "end", "jugend", "lung", "hand"]
    false_bases = ["ans", "an", "und", "freund", "ist", "ich", "etsch", "lug", "eichen", "agieren","erker","huldigung","okratisches"]  
    suffixes = ["", "e", "er", "en"]
    prefixes = ["", "ge", "ver", "be"] 
       
    true_words = {prefix + base + suffix for base in true_bases for prefix in prefixes for suffix in suffixes}
     
    if word.lower() in false_bases:
        return False
    if word.lower() in true_words: 
        return True
    
    return dictionary.lookup(word.capitalize())


def compound_splitter(word, depth=2):
        not_compound_word=["nationen","und","brandenburger","versprochen","adresse","jemanden","ergeben","zusammen","bernauer"] 
        compounds = [] 
        if word.lower() in not_compound_word:
            return [word]
        splits = splitter.split_compound(word)
    
        if not splits or depth == 0:
            return []

        for i in range(min(len(splits), 3)):
            first_part = splits[i][1].lower()
            second_part = splits[i][2].lower()

            
            if first_part == second_part:
                if word.istitle():
                    first_part=first_part.title()
                return [first_part]
            
        
            if ((((is_german(first_part) or is_german(first_part[:-1])) or is_german(second_part)) and depth==2 and len(first_part)+len(second_part)>=13) or ((is_german(first_part) or is_german(first_part[:-1])) and is_german(second_part))):
                first_split = compound_splitter(first_part, depth - 1)
                second_split = compound_splitter(second_part, depth - 1)

                if first_split and second_split:
                    compounds.extend(first_split)
                    compounds.extend(second_split)
                else:
                    compounds.append(first_part)
                    compounds.append(second_part)
                break

        if compounds == []:
            compounds = [word]
        
        compounds=[c.lower() for c in compounds]
        if word.istitle():
            compounds[0]=compounds[0].title()
        
        return compounds 

def separate_prefix(word):
        prefixes = ["an", "ab", "auf", "aus", "dis", "ein", "her", "hin", "haupt", "in", "dar", "durch",
                    "los", "mit", "nach","ge", "von", "vor", "weg", "um", "un", "ur", "ent", "er", "ver", "zer", "miss",
                    "miß", "niss", "niß", "ex", "non", "super", "trans", "kon", "hoch", "stink", "stock", "tief",
                    "tod", "erz", "unter", "über", "hinter", "wider", "wieder", "weiter", "zurück", "zurecht",
                    "zusammen", "hyper", "inter","phy","sys","ruhm","rühm","alex","be","gym"]
        
        excluded_suffixes = ["ssen", "ts", "er"] 
        excluded_words = ["und", "geben", "wege", "ins","besten","geht","universität","antwortet","gestern","beeren","gelb","bernauer"]
        excluded_prefixes = ["eine", "eini","berlin","erst"]
        special_case = "gereist" 
        word_lower=word.lower() 
   
        for prefix in prefixes:
            word_suffix = word[len(prefix):]
             
            if (
                word_lower.startswith(prefix) and 
                len(word_suffix)>1 and
                word_suffix not in excluded_suffixes and 
                word_lower not in excluded_words and 
                not any(word_lower.startswith(ex_prefix) for ex_prefix in excluded_prefixes) and 
                (not word_lower.startswith("ger") or word_lower == special_case)
            ):  
                if word.istitle():
                    prefix=prefix.title()
                    
                return [prefix, word_suffix]

        return ["", word]


def syllable_splitter(word):
        
        vowels = ['a', 'e', 'i', 'o', 'u', 'ä', 'ö', 'ü','é','è', 'ei', 'ai', 'ey', 'ay', 'eu', 'äu', 'ie', 'au', 'aa', 'ee', 'oo']
        vowelsdouble = ['ei', 'ai', 'ey', 'ay', 'eu', 'äu', 'ie', 'au', 'aa', 'ee', 'oo']
        consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z', 'ß', 'sch', 'ch', 'ck', 'qu', 'ph']
        new_word = []
        forbidden=['sk','br']
        no_split_word=["gate"]
         
   
        if word.lower() in no_split_word:
           return word
        
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
        
        # VthV->V-thV
        i=0
        while i<(len(new_word)- 3):
            if new_word[i] in vowels and new_word[i+1]=="t" and new_word[i+2]=="h" and new_word[i+3] in vowels:
                new_word = new_word[:i+1] + ['-'] + new_word[i+1:]
                continue
            i+=1

         
        # VCCV->VC-CV
        i=0
        while i<(len(new_word)- 3):
           
            if "".join(new_word).lower()=="restaurant":
                new_word = new_word[:i+2] + ['-'] + new_word[i+2:]
                continue
            elif new_word[i] in vowels and new_word[i+1] in consonants and new_word[i+2] in consonants and new_word[i+3] in vowels and new_word[i+1]+new_word[i+2] not in forbidden and "".join(new_word).lower()!="adresse":
              
                new_word = new_word[:i+2] + ['-'] + new_word[i+2:]
                continue
            i+=1
        
        # VCCCV->VCC-CV
        i=0
        while i<(len(new_word)- 4):
            if new_word[i] in vowels and new_word[i+1] in consonants and new_word[i+2] in consonants and new_word[i+3] in consonants and new_word[i+4] in vowels:
                new_word = new_word[:i+3] + ['-'] + new_word[i+3:]
                continue
            i+=1

        # VCV->V-CV 
        i=0
        while i<(len(new_word)- 2):
            
            if new_word[i] in vowels and new_word[i+1] in consonants and new_word[i+2] in vowels and (i!=0 or new_word[i] in vowelsdouble) and "".join(new_word[i:i+3])!="ice":
                if "".join(new_word[i:i+3])=="iru":     
                    new_word = new_word[:i+2] + ['-'] + new_word[i+2:]
                    continue
                new_word = new_word[:i+1] + ['-'] + new_word[i+1:]
            
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
 
         # CVVC->CV-VC (double vowel)
        #i=0 
        #while i<(len(new_word)- 2):
         
          #  if new_word[i] in consonants and new_word[i+1] in vowelsdouble and new_word[i+2] in consonants:
           #     new_word = new_word[:i+1] + list(new_word[i+1]) + new_word[i+2:]
          #      new_word = new_word[:i+2] + ['-'] + new_word[i+2:]
           #     continue  
          #  i+=1 
         
        # VCCV->V-CCV
        i=0
        while i<(len(new_word)- 3):
            if new_word[i] in vowels and new_word[i+1] in consonants and new_word[i+2] in consonants and new_word[i+3] in vowels and "".join(new_word).lower()!="adresse":
                
                new_word = new_word[:i+1] + ['-'] + new_word[i+1:]
                continue
            i+=1
        
        # 2 ista suglasnika u sredini riječi se dijele
        i=0
        while i<(len(new_word)- 2): 
            if new_word[i] in consonants and new_word[i+1] in consonants and new_word[i]== new_word[i+1] and new_word[i+2]  in vowels:
                

                new_word = new_word[:i+1] + ['-'] + new_word[i+1:]
                continue
            i+=1

         # 2 ista suglasnika u sredini riječi se ne dijele
        i=0
        while i<(len(new_word)- 3):
            if new_word[i] in consonants and new_word[i+1] in consonants and new_word[i]== new_word[i+1] and new_word[i+2] in consonants and new_word[i+3] in vowels:
                

                new_word = new_word[:i+2] + ['-'] + new_word[i+2:]
                continue
            i+=1
 
        new_word_string=""
        for el in new_word:
            new_word_string+=el
        new_word_string=new_word_string.replace("-"," ")
        if word.istitle()==True:
             
            new_word_string=new_word_string[0].upper()+new_word_string[1:]
       
        return new_word_string