class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char   # stored as an integer - the ASCII character code value
        self.freq = freq   # the freqency associated with the node
        self.left = None   # Huffman tree (node) to the left
        self.right = None  # Huffman tree (node) to the right

    def set_left(self, node):
        self.left = node

    def set_right(self, node):
        self.right = node

    def __lt__ (self,other):
        return comes_before(self,other)

def comes_before(a, b):
    """Returns True if tree rooted at node a comes before tree rooted at node b, False otherwise"""
    if a.freq < b.freq:
        return True
    elif a.freq == b.freq:
        return a.char < b.char
    else:
        return False

def combine(a, b):
    """Creates and returns a new Huffman node with children a and b, with the "lesser node" on the left
    The new node's frequency value will be the sum of the a and b frequencies
    The new node's char value will be the lesser of the a and b char ASCII values"""
    char = min(a.char,b.char)
    freq = a.freq + b.freq
    huffman_node = HuffmanNode(char,freq)
    
    if a < b:
        huffman_node.set_left(a)
        huffman_node.set_right(b)
    # else:
    #     huffman_node.set_left(b)
    #     huffman_node.set_right(a)

    return huffman_node

def cnt_freq(filename):
    """Opens a text file with a given file name (passed as a string) and counts the 
    frequency of occurrences of all the characters within that file"""

    freq = [0] * 256
    f = open(filename, "r")
    
    for i in f:
        for j in i:
            freq[ord(j)] += 1

    f.close()

    return freq 

def create_huff_tree(char_freq):
    """Create a Huffman tree for characters with non-zero frequency
    Returns the root node of the Huffman tree"""

    nodes = []

    for idx,i in enumerate(char_freq):
        if i != 0:
            nodes.append(HuffmanNode(idx,i))
    
    nodes.sort()
    
    while len(nodes) > 1:
        temp = combine(nodes[0], nodes[1])
        del (nodes[0])
        del (nodes[0])       
        nodes.append(temp)
        nodes.sort()

    return nodes[-1]


def create_code(node):
    """Returns an array (Python list) of Huffman codes. For each character, use the integer ASCII representation 
    as the index into the arrary, with the resulting Huffman code for that character stored at that location"""

    codes = [''] * 256

    code = ''

    return create_code_helper(node, codes, code)


def create_code_helper(node, codes, code):
    """returns codes for characters after traversing down the root node. Everytime it goes left, it records a 0 
    it goes right it records a 1."""
    temp = code
    temp2 = code

    if node.left != None:
        temp += '0'
        create_code_helper(node.left, codes, temp)

    elif node.right == None and node.left == None:
        codes[node.char] = temp

    if node.right != None:
        temp2 += '1'
        create_code_helper(node.right, codes, temp2)

    elif node.right == None and node.left == None:
        codes[node.char] = temp2

    return codes

def create_header(freqs):
    """Input is the list of frequencies. Creates and returns a header for the output file
    Example: For the frequency list asscoaied with "aaabbbbcc, would return "97 3 98 4 99 2" """

    header = ""
    for idx,i in enumerate(freqs):
        if i > 0:
            header += "{} {} ".format(idx, i)
    return header[:-1]
    
def huffman_encode(in_file, out_file):
    """Takes inout file name and output file name as parameters
    Uses the Huffman coding process on the text from the input file and writes encoded text to output file
    Take note of special cases - empty file and file with only one unique character"""

    try:
        in_f = open(in_file, 'r')
    except:
        raise FileNotFoundError

    out = open(out_file, 'w', newline='')

    to_encode = ''

    for line in in_f:
        to_encode += line

    if to_encode != '':
        frequencies = cnt_freq(in_file)
        tree = create_huff_tree(frequencies)

        if tree.left == None and tree.right == None:
            frequencies = cnt_freq(in_file)
            out.write(create_header(frequencies))

        else:
            frequencies = cnt_freq(in_file)
            out.write(create_header(frequencies))
            out.write('\n')
            codes = create_code(tree)
            
            for i in to_encode:
                out.write(codes[ord(i)])

    out.close()
    in_f.close()

def parse_header(header_string):
    """takes a header string creating by the huffman encode and returns a list of frequencies by pairing every 
    two values (ord, freq#) and appending it to the list """
    freq = [0] * 256

    header = header_string.split()

    for i in range(0,len(header) - 1, 2):
        freq[int(header[int(i)])] = int(header[int(i) + 1])

    return freq


def huffman_decode(encoded_file, decode_file):
    """Takes an encoded file name and decoded file name as parameters
    Uses the huffman coding process on the text from the encoded file and writes a decoded text to the output file
    Gets frequencies from the header"""
    try:
        in_f = open(encoded_file, 'r')
    except:
        raise FileNotFoundError

    out = open(decode_file, 'w', newline='')
    to_decode = ''

    header = in_f.readline()

    to_decode = in_f.readline()

    if header != '':
        frequencies = parse_header(header)
        tree = create_huff_tree(frequencies)

        if tree.left == None and tree.right == None:
            for i in range(tree.freq):
                out.write(chr(tree.char))

        # if to_decode != '':
        #     codes = create_code(tree)
        #     current_code = ''
        else:
            temp = tree
            for i in to_decode:
                # current_code += i

                if i == '0':
                    temp = temp.left
                    if temp.left == None and temp.right == None:
                        out.write(chr(temp.char))
                        temp = tree
                elif i == '1':
                    temp = temp.right
                    if temp.left == None and temp.right == None:
                        out.write(chr(temp.char))
                        temp = tree


                # for idx,j in enumerate(codes):
                #     if current_code == j:
                #         out.write(chr(idx))
                #         current_code = ''
                #         break

        # elif header != '' and tree.left == None and tree.right == None:
        #     for i in range(tree.freq):
        #         out.write(chr(tree.char))

    out.close()
    in_f.close()


