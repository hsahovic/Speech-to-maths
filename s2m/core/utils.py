from numpy import log10

def natural_log (x) :
    return int (log10(x))

def _set_words (words) : 
    if type (words) == list : 
        for el in words : 
            if type (el) != str : 
                raise ValueError ("Incorrect value for Number Parser. Argument must be of type str or list of str") 
        return words
    elif type (words) == str : 
        return words.split (' ') 
    else : 
        raise ValueError ("Incorrect value for Number Parser. Argument must be of type str or list of str") 