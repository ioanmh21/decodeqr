from PIL import Image
import numpy as np
import masks
import rotate
import decode_functions as df

def afmat(mat):
    with open('output.txt','w') as file:
        for line in mat:
            for x in line:
                file.write(str(x)+' ')
            file.write('\n')

# afisare cod qr
def display(mat):
    global n
    newmat=[[0 for x in range(n+2)]]
    for line in mat:
        new_line=[0]
        for x in line:
            new_line.append(x)
        new_line.append(0)
        newmat.append(new_line)
    newmat.append([[0 for x in range(len(mat)+2)]])

    scale = 20
    scaled_matrix = np.kron(mat, np.ones((scale, scale)))

    inverted_matrix=1-scaled_matrix

    image = Image.fromarray(inverted_matrix * 255)
    image.show()

#citire cod qr
mat=[]
with open('input.txt','r') as file:
    for line in file:
        row = list(map(int, line.strip().split()))
        mat.append(row)
mat=np.array(mat)

n=len(mat)
version = ((n - 21) // 4) + 1

data_mat=masks.get_data_matrix(mat)

format_info = df.extract_format_information(mat)
mask_pattern = df.get_mask_pattern(format_info)
error_correction_level = df.get_error_correction_level(format_info)
error_correction_bits = df.get_error_correction_bits(format_info)

mat = masks.mask(masks.correct_mask(mask_pattern),mat)

data_bits = df.extract_data_bits(mat)

mode = df.get_encoding_mode(data_bits)
count = df.get_character_count(data_bits,mode)
data = df.extract_data(data_bits[4 + count[0]:], mode, count[1])

print(data)
