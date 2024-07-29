# DNACompressionTools
The currently available version uses a variation of the Lempel-Ziv-Welch (LZW) algorithm for lossless compression in order to compress a given string containing base pairs using k-mers of a fixed range in length.

Input (lzw_encode):

sequence - A string containing IUPAC bases

n - minimum k-mer length

m - maximum k-mer length

dictionary (optional, advanced) - customised starting dictionary for compression. Default is to include all sequences of base pairs of length n.

Output (lzw_encode):

result - encoded list of ints

dictionary - dict object used to compress the full sequence with entries:

dictionary[k] = i

k - k-mer

i - integer code


Ambiguous IUPAC symbols are assigned a compatible base pair identity at random.
