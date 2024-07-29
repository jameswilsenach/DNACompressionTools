import numpy as np
# Constants for the base pairs and padding symbol
BASE_PAIRS = ['A', 'G', 'C', 'T']
AMB_PAIRS = ['Y','N','K','S','W','M','R']
TOT_PAIRS = BASE_PAIRS+AMB_PAIRS

PADDING_SYMBOL = 'X'
import numpy as np

def generate_strings(length):
    """Generate all possible strings of a given length from the base pairs"""
    if length == 0:
        return ['']
    shorter_strings = generate_strings(length - 1)
    return [s + base for s in shorter_strings for base in BASE_PAIRS]

def handle_amb(B):
    if B=='W':
        return ('A','T')
    elif B=='S':
        return ('C','G')
    elif B=='M':
        return ('A','C')
    elif B == 'K':
        return ('G','T')
    elif B == 'R':
        return ('A','G')
    elif B == 'Y':
        return ('C','T')
    elif B == 'N':
        return BASE_PAIRS   
    

def generate_padded_strings(length):
    """Generate strings of the given length padded with the padding symbol at terminal positions"""
    strings = generate_strings(length)
    padded_strings = []
    for i in range(1, length):
        for s in generate_strings(i):
            padded_strings.append(s + PADDING_SYMBOL * (length - i))
    return strings + padded_strings

def get_encoder_dictionary(n):
        initial_strings = generate_padded_strings(n)
        dictionary = {s: i for i, s in enumerate(initial_strings)}
        return dictionary

def get_decoder_dictionary(n):
        initial_strings = generate_padded_strings(n)
        dictionary = {i: s for i, s in enumerate(initial_strings)}
        return dictionary

def lzw_encode(sequence, n, m,dictionary=None):
    """LZW encoder with a minimum code length of n and a maximum code length of m"""
    # Initialize the dictionary with all strings of length n and their terminally padded versions
    if dictionary is None:
        dictionary = get_encoder_dictionary(n)
    
    dict_size = len(dictionary)

    if not sequence:
        return [], dictionary

    p = sequence[:n] if len(sequence) >= n else sequence + PADDING_SYMBOL * (n - len(sequence))
    p = list(p)
    for i in range(len(p)):
        if p[i] in AMB_PAIRS:
         p[i] = np.random.choice(handle_amb(p[i]))
    p = ''.join(p)
    result = []
    idx = n

    while idx < len(sequence):
        pc = p
        while idx < len(sequence):
            if sequence[idx] in AMB_PAIRS:
                BPs = handle_amb(sequence[idx])
                bp = np.random.choice(BPs)
                pc+= bp
            else:
                pc += sequence[idx]
            if pc in dictionary:
                idx += 1
                p = pc
            else:
                break
        
        result.append(dictionary[p])
        
        if pc not in dictionary and len(pc) <= m:
            dictionary[pc] = dict_size
            dict_size += 1
        npad = n - len(sequence[idx:idx+n]) 
        p = sequence[idx:idx+n] + PADDING_SYMBOL * npad
        p = list(p)
        for i,c in enumerate(p):
            if p[i] in AMB_PAIRS:
                bp = handle_amb(p[i])
                p[i] = np.random.choice(bp)
        p = ''.join(p)
        idx += n

    if p != 'X'*n:
        result.append(dictionary[p])

    return result, dictionary

def lzw_decode(encoded, n, m, dictionary=None):
    """LZW decoder with a minimum code length of n and a maximum code length of m"""
    
    # Initialize the dictionary with all strings of length n and their terminally padded versions
    if dictionary is None:
        dictionary = get_decoder_dictionary(n)
    
    dict_size = len(dictionary)

    if not encoded:
        return "",dictionary

    result = []
    w = dictionary[encoded[0]]
    encoded = encoded[1:]
    result.append(w)

    for k in encoded:
        if k in dictionary:
            entry = dictionary[k]
        else:
            entry = w + w[:1]  # Handle the cScSc exception

        result.append(entry)

        # Add w + entry[:1] to the dictionary if it's within the maximum length
        if len(w + entry[:1]) <= m:
            dictionary[dict_size] = w + entry[:1]
            dict_size += 1
        
        w = entry
    
    return ''.join(result).replace(PADDING_SYMBOL, ''),dictionary
