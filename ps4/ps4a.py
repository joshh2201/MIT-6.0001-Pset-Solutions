# Problem Set 4A
# Name: Josh Hong

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    
    if len(sequence) == 1:
        return [sequence]
    else:
        perm = []
        for i in range(len(sequence)):
            letters = list(sequence)
            letters[0], letters[i] = letters[i], letters[0] # swap first letter with letter at index i
            for combo in get_permutations(''.join(letters)[1:]):    # reformat into string excluding first letter
                perm.append(letters[0]+ combo)
        return perm

if __name__ == '__main__':
#    #EXAMPLE
    example_input1 = 'abc'
    print('Input:', example_input1)
    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    print('Actual Output:', get_permutations(example_input1))
    print('-'*10)

    example_input2 = 'ab'
    print('Input:', example_input2)
    print('Expected Output:', ['ab', 'ba'])
    print('Actual Output:', get_permutations(example_input2))
    print('-'*10)

    example_input3 = 'xyz'
    print('Input:', example_input3)
    print('Expected Output:', ['xyz', 'xzy', 'yxz', 'yzx', 'zyx', 'zxy'])
    print('Actual Output:', get_permutations(example_input3))
    print('-'*10)
