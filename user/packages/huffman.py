import heapq
import os
import sys


################################################################## Containers For Compressing

path = ""
heap = []
codes = {}
string=""
reverse_mapping = {}
download="C:/Users/AshishPC/Desktop/WattsApp/download"+"/"
upload="C:/Users/AshishPC/Desktop/WattsApp/upload"+"/"

####################################################################  Auxiliary Functions
def byte_to_char(byte):
    i=int(byte,2)
    c=chr(i)
    return c

def char_to_str(c):
    n=ord(c)
    return ('0'*(7-len(bin(n)[2:])) +str(bin(n)[2:]))

def writeInFile(file_name,content):
	file=open(file_name,"w")
	file.write(content)
	file.close()

def read_file(file_name):
	print(file_name)
	file=open(file_name,"r")
	r=file.read()
	file.close()
	return r

#################################################################### Heap Node
class HeapNode:
	def __init__(self, char, freq):
		self.char = char
		self.freq = freq
		self.left = None
		self.right = None
	def __lt__(self, other):
		return self.freq < other.freq
	def __eq__(self, other):
		if(other == None):
			return False
		if(not isinstance(other, HeapNode)):
			return False
		return self.freq == other.freq


###########################################################Compress


#Step 1
def make_frequency_dict(text):
	frequency = {}
	for character in text:
		if not character in frequency:
			frequency[character] = 0
		frequency[character] += 1
	return frequency


#Step 2
def make_heap(frequency):
	for key in frequency:
		node = HeapNode(key, frequency[key])
		heapq.heappush(heap, node)
	return heap

#Step 3
def merge_nodes():
	while(len(heap)>1):
		node1 = heapq.heappop(heap)
		node2 = heapq.heappop(heap)
		merged = HeapNode(None, node1.freq + node2.freq)
		merged.left = node1
		merged.right = node2
		heapq.heappush(heap, merged)

def make_codes_helper(root, current_code):
	if(root == None):
		return
	if(root.char != None):
		codes[root.char] = current_code
		reverse_mapping[current_code] = root.char
		return
	make_codes_helper(root.left, current_code + "0")
	make_codes_helper(root.right, current_code + "1")

# Step 4
def make_codes():
	root = heapq.heappop(heap)
	current_code = ""
	make_codes_helper(root, current_code)


#Step 5
def get_encoded_text(text):
	encoded_text = ""
	for character in text:
		encoded_text += codes[character]
	return encoded_text

#Step 6
def pad_encoded_text(encoded_text):
	extra_padding = 7 - len(encoded_text) % 7
	for i in range(extra_padding):
		encoded_text += "0"
	padded_info = "{0:07b}".format(extra_padding)
	encoded_text = padded_info + encoded_text
	return encoded_text

#Step 7
def convert_to_char_string(padded_encoded_text):
    if(len(padded_encoded_text) % 7 != 0):
        print("Encoded text not padded properly")
        exit(0)
    b=""
    for i in range(0,len(padded_encoded_text),7):
        byte = padded_encoded_text[i:i+7]
        b=b+byte_to_char(byte)
    return b







def  compress(path="",str1=""):
	text=str1
	if path!="":
		with open(path, 'r') as file:
			text=file.read()
	text=text.rstrip()
	frequency =  make_frequency_dict(text)
	make_heap(frequency)
	merge_nodes()
	make_codes()
	encoded_text=get_encoded_text(text)
	padded_encoded_text=pad_encoded_text(encoded_text)
	b = convert_to_char_string(padded_encoded_text)
	print("Percentage Compression {:0.2f}".format((len(text)-len(b))/len(text)*100))  #print("{:.2f}".format(round(a, 2)))
	filename=upload+"email"
	if path!="":
		filename, file_extension = os.path.splitext(path)
	reverse_str= str(reverse_mapping)
	writeInFile(filename+"_dict.txt",reverse_str)
	percent=(sys.getsizeof(text)-sys.getsizeof(b))/sys.getsizeof(text)*100
	if percent<=0:
		text=text
		os.remove(filename+"_dict.txt")
	else:
		text=b
	return (text) #########3return if not file



#############################################################  decompress ###################################################

def get_reverse_mapping(filename=download+"email.txt"):
    filename=filename.split('.')[0]+"_dict.txt"
    f=open(filename,"r")
    r=f.read()
    f.close()
    os.remove(filename)
    dict=eval(r);
    return dict

def decode_text(un_padded_str,reverse_map):
    str=""
    text=""
    for i in range(0,len(un_padded_str)):
        str=str+un_padded_str[i]
        if str in reverse_map:
            c=reverse_map[str]
            text=text+c
            str=""
    return text

def decompress(path="",str=""):
    text=str
    if path!="":
        text=read_file(path)
    padding_bits=ord(text[0])
    text=text[1:]
    padded_str=""
    for c in text:
        padded_str=padded_str+char_to_str(c)
    un_padded_str=padded_str[0:-padding_bits]
    if path!="":
        map=get_reverse_mapping(path)
    else:
        map=get_reverse_mapping()
    return(decode_text(un_padded_str,map))








def compress_text(file_name="",string=""):
    if file_name=="" and string=="":
        return ""
    if file_name=="":
        return compress(file_name,string)
    file=upload+file_name
    s= compress(file,string)
    writeInFile(file,s)
    return s

def decompress_text(file_name="",string=""):
    if file_name=="" and string=="":
        return ""
    if file_name=="":
        return decompress(file_name,string)
    file=download+file_name
    s=decompress(file,str)
    writeInFile(file,s)
    return s;

########################################################################################################################################
download="uploads/"
upload="uploads/"

'''
s1=""
s2=""
s1=compress_text(file_name="ashish.txt",string="I am Ashish Singh")
print(s1)
s2=decompress_text(file_name="",string=s1)
print(s2)
'''
##########################################################################################################################################3
