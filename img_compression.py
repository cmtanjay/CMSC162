import variables

def run_length_coding():
    print()

# Creating tree nodes
class NodeTree(object):

    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def children(self):
        return (self.left, self.right)

    def nodes(self):
        return (self.left, self.right)

    def __str__(self):
        return '%s_%s' % (self.left, self.right)


# Main function implementing huffman coding
def huffman_code_tree(node, left=True, binString=''):
    if type(node) is int:
        return {node: binString}

    (l, r) = node.children()
    d = dict()
    d.update(huffman_code_tree(l, True, binString + '0'))
    d.update(huffman_code_tree(r, False, binString + '1'))
    return d
    
def huffman_coding(self):
    if not variables.image_data:
        print("No PCX Image Loaded")
        self.add_text_to_statusbar("Status: No PCX image loaded", x=120, y=20, fill="white", font=("Arial", 9,))
    else:
        colors = []
        count = []
        i=0      
        
        while(i < len(variables.image_data)):
            if variables.image_data[i] not in colors:
                colors.append(variables.image_data[i])
                count.append([len(colors)-1, 1])
            else:
                count[colors.index(variables.image_data[i])][1] += 1
            print(i)
            i += 1
            
        print(colors)
        print(count)

        # Sort the 2D array based on the values in the second column
        sorted_array = sorted(count, key=lambda x: x[1])

        # Print the sorted array
        for row in sorted_array:
            print(row)
            
        nodes = sorted_array
        i = 0
        while len(nodes) > 1:
            (key1, c1) = nodes[-1]
            (key2, c2) = nodes[-2]
            nodes = nodes[:-2]
            node = NodeTree(key1, key2)
            nodes.append((node, c1 + c2))

            nodes = sorted(nodes, key=lambda x: x[1], reverse=True)
            print(i)
            i+=1

        huffmanCode = huffman_code_tree(nodes[0][0])

        print(huffmanCode)

        coded = ""
        huffman_coded = []

        for color in variables.image_data:
            code = colors.index(color)
            coded = coded + huffmanCode[code]
        
        print(f"huf_len: {len(coded)}")
            
        # print(coded)
        
def decode_huffman(huffman_coded):
    print("dsahjasd")