# Problem Set 4C
# Name: Josh Hong
# Collaborators:
# Time Spent: x:xx

from operator import index
import string
from pathlib import Path
from ps4a import get_permutations

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(Path(__file__).parent /file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


### END HELPER CODE ###

# constants
WORDLIST_FILENAME = 'words.txt'
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object
                
        text (string): the message's text

        A SubMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)
    
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words.copy()
                
    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)
        
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled 
        according to vowels_permutation. The first letter in vowels_permutation 
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52 
        keys of all the uppercase letters and all the lowercase letters.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        transpose_dict = {}
        map_vowels = vowels_permutation + vowels_permutation.upper()
        perm_index = 0
        for letter in string.ascii_letters:
            if letter not in map_vowels:
                transpose_dict[letter] = letter
            else:
                transpose_dict[letter] = map_vowels[perm_index]
                perm_index += 1
        return transpose_dict
    
    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary
        
        Returns: an encrypted version of the message text, based 
        on the dictionary
        '''
        msg_chars = list(self.get_message_text())
        for ind, char in zip(range(len(msg_chars)),msg_chars):
            if char in 'aeiouAEIOU':
                msg_chars[ind] = transpose_dict[char]
        return ''.join(msg_chars)
        
class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        SubMessage.__init__(self,text)

    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message 
        
        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.
        
        If no good permutations are found (i.e. no permutations result in 
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message    
        
        Hint: use your function from Part 4A
        '''
        perms = get_permutations('aeiou')
        score_dict ={}
        for perm in perms:
            score = 0
            decoded_msg = self.apply_transpose(self.build_transpose_dict(perm))
            for word in decoded_msg.split():
                if is_word(self.valid_words, word):
                    score += 1
            score_dict[score] = decoded_msg
        best_score = max(score_dict.keys())
        return score_dict[best_score]

if __name__ == '__main__':
    # Test Cases
    message1 = SubMessage("Hello World!")
    permutation = "eaiuo"
    enc_dict = message1.build_transpose_dict(permutation)
    print("Original message:", message1.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Hallu Wurld!")
    print("Actual encryption:", message1.apply_transpose(enc_dict))
    enc_message1 = EncryptedSubMessage(message1.apply_transpose(enc_dict))
    print(enc_message1.get_message_text())
    print("Decrypted message:", enc_message1.decrypt_message())
    print('-' *10)
    
    message2 = SubMessage("Problem sEt four!")
    permutation = "ouaie"
    enc_dict = message2.build_transpose_dict(permutation)
    print("Original message:", message2.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Priblum sUt fier!")
    print("Actual encryption:", message2.apply_transpose(enc_dict))
    enc_message2 = EncryptedSubMessage(message2.apply_transpose(enc_dict))
    print(enc_message2.get_message_text())
    print("Decrypted message:", enc_message2.decrypt_message())