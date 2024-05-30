import re
from split_words import Splitter
from api.utilities.utilities import compound_splitter, separate_prefix, syllable_splitter

splitter = Splitter()

def processing_input(sentence):
        
        words = re.findall(r"[\w']+|[.,!?;:„“]", sentence)
        compound_list = []
        for word in words:
            if word.isalnum():
                final_split = compound_splitter(word)
                print(final_split)
                compound_list.extend(final_split)
            else:
                compound_list.append(word)
        
        return compound_list

def processing_compounds(word):
        
        prefix, suffix = separate_prefix(word)
        prefix2, suffix = separate_prefix(suffix)
        prefix_syllables=syllable_splitter(prefix)
        prefix2_syllables=syllable_splitter(prefix2)
        suffix_syllables = syllable_splitter(suffix)

        if prefix_syllables != "" and prefix2_syllables != "":
            syllable_list = prefix_syllables + " " + prefix2_syllables + " " + suffix_syllables

        elif prefix_syllables != "" and prefix2_syllables == "":
            syllable_list = prefix_syllables + " " + suffix_syllables

        else:
            syllable_list = suffix_syllables
        
        return syllable_list


def split_input(input):
    compound_list = processing_input(input)
    syllable_list = [processing_compounds(compound) for compound in compound_list]
    syllable_string=" ".join(syllable_list)
    syllable_string=re.sub(r'\s{2,}', ' ', syllable_string)
    syllable_string = re.sub(r'\s+([.,!?;:“])', r'\1', syllable_string)
    final_syllable_string = re.sub(r'([„“])\s+', r'\1', syllable_string)

     
    return final_syllable_string
