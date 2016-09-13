# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# # Bài tập thực hành KnapSack - Hệ cơ sở tri thức 
# 1312078 - Phạm Thị Cẩm Duyên

# <codecell>

import numpy as np
import random

# <codecell>

"""Tạo class item với các thuộc tính : 
    + tên item 
    + khối lượng item 
    + giá trị item
"""
class item:
    def __init__(self,i_name,i_weight,i_value):
        self.name = i_name
        self.weight = i_weight
        self.value = i_value

# <codecell>

""" Thực hiện đọc file lấy dữ liệu của các items và tạo nên list đối tượng các item (items)
    Tham số đầu vào : tên file 
    Trả về : list các item đọc được từ file , và cân nặng giới hạn đọc được từ file 
"""

def readFile(file_name):
    fileObj = open(file_name,'r')
    data = fileObj.read()
    print "*************************Tập dữ liệu ban đầu *******************************"
    print data 
    
    line = data.split('\n')
    weight_limit = line[0].split(",")[0]           
    number_item = line[0].split(",")[1]           
    line.remove('')        # remove the blank line 
    
    items = []
    for i in range(1,len(line),1):
        attr = line[i].split(',')
        new_item = item(attr[0],attr[1],attr[2])
        items.append(new_item)
    return items,weight_limit

# <codecell>

""" Hàm tính độ thích nghi là fitness và khối lượng theo từng nhiễm sắc thể 
    Tham số đầu vào : 
        + items : list các đối tương item 
        + popu : quần thể với các nhiễm sắc thể 
        + popsize : kích thước của quần thể 
        + len_chorom : độ dài của nhiễm sắc thể 
    Trả về : Mảng chứa tất cả độ thích nghi của NST và Mảng chứa khối lượng của tất cả các NST
"""
def fit_weight_all(items,popu,pop_size,len_chorom):
    fitness = np.zeros(pop_size)
    weight_items = np.zeros(pop_size)
    for i in range(pop_size):
        for j in range(len_chorom):
            if popu[i][j] == 1:
                fitness[i] = fitness[i] + int(items[j].value)
                weight_items[i] = weight_items[i] + int(items[j].weight)
    return fitness,weight_items

"""
    Hàm cập nhật fitness và weight của NST có ví trị index trong quần thể sau khi tại ví trị dó NST bị thay đổi 
    Tham số đầu vào : 
        + fitness : độ thích nghi của tất cả các NST
        + weight_items : khối lượng của tất cả các NST
        + items : list các đối tương item 
        + popu : quần thể với các nhiễm sắc thể
        + len_chorom : độ dài của nhiễm sắc thể 
        + index : là vị trí NST
"""
def fit_weight_update(fitness,weight_items,items,popu,len_chorom,index):
    fitness[index] = 0
    weight_items[index] = 0
    for j in range(len_chorom):
        if popu[index][j] == 1:
            fitness[index] = fitness[index] + int(items[j].value)
            weight_items[index] = weight_items[index] + int(items[j].weight)

""" 
    Hàm tạo vòng tròn roulette
    Tham số đầu vào : 
        + fitness : độ thích nghi của tất cả các NST
        Thực hiện chia vòng tròn roulette theo phần trăm của cộng dồn fitness
    Trả về :
        Mảng gồm các phần tử là các phần của vòng tròn roulette 
"""
def roulette_parts(fitness):
    roulette = np.zeros(pop_size)
    for i in range(len(fitness)):
        roulette[i] = np.sum(fitness[:i+1]) / np.sum(fitness)
    return roulette

"""
    Tìm ví trí NST nào mà tương đương với giá trị quay roulette đó
    Tham số đầu vào : 
        + roulette :  Mảng gồm các phần tử là các phần của vòng tròn roulette 
        + value : giá trị quay vòng tròn roulette
    Trả về : 
        + ví trị của mảng roulette mà value được xếp vào
"""
def find(roulette, value): 
    # Giúp trả về ví trị đầu tiên trong mảng mà lớn hơn bằng bằng giá trị value
    return map(lambda x: x >=value, roulette).index(True)    

# <codecell>

file_name = 'data.txt'
items,weight_limit = readFile(file_name)

pop_size = 10             # kích thước quần thể 
len_chorom = len(items)   # Chiều dài bit của NST
# weight_limit = 400        Khối lượng giới hạn 

pcross = 0.4              # Xác suất kiếm tra lai 
pmul = 0.1                # Xác suất kiểm tra đột biến
iteration = 1000          # Số vòng lặp giới hạn 

# Tạo quần thể bằng cách random NST với số lượng là pop_size 
# Mỗi nhiếm sắc thể là chuỗi bit 0 1 với chiều dài là số lượng item 
popu = np.zeros((pop_size,len_chorom))
for i in range(pop_size):
    popu[i] = np.random.randint(2, size=len_chorom)
popu  = popu.astype(int)

# Gọi hàm trả về độ thích nghi là khối lượng của NST 
fitness,weight_items = fit_weight_all(items,popu,pop_size,len_chorom)
max_fitness = 0
res_weight = 0

num_iteration = 0
best_sol = np.zeros(len_chorom).astype(int)
# Thực hiện chọn lọc, lai và đột biến lặp với vòng lặp giới hạn nếu chia tìm được khối lượng thích hợp 
while num_iteration < iteration :
    # Tính fitness và weight 
    # NST nào có weight > weight giới hạn thì chọn bit 1 chuyển thành bit 0 ( ở đây em chọn bít 1 đầu tiền )
    # Sau đó cập nhật lại fitness và weight
    for i in range(pop_size):
        while weight_items[i] > weight_limit:
            idx_random = list(popu[i]).index(1)
            popu[i][idx_random] = 0
            fit_weight_update(fitness,weight_items,items,popu,len_chorom,i)
            
    if max(fitness) > max_fitness:
        max_fitness = max(fitness)
        best_sol = popu[list(fitness).index(max(fitness))]
        res_weight = weight_items[list(fitness).index(max(fitness))]
    # Tạo vòng tròn roulette0
    roulette = roulette_parts(fitness)
    
    # Random gía trị ngầu nhiên để chọn lọc NST theo vòng tron rollett
    # Thực hiện random với số lần bằng với số NST 
    # mỗi lần chọn ra được NST mới ta thay thế trực tiếp vào để được quần thể mới 
    new_popu = np.zeros((pop_size,len_chorom)).astype(int)
    for i in range(pop_size):
        random_value = np.random.uniform(0,1)
        idx_chorom =  find(roulette, random_value)
        new_popu[i] = popu[idx_chorom]
    
    # Random tạo xác suất lai cho từng NST trong quần thể
    p_cr = np.random.uniform(0,1,size=(1,pop_size))
    
    # Ta chọn ra những ví trị NST mà p < pcross
    # mảng chr_cr chứa giá trị là những ví trị NST thỏa xác suất để lai
    chr_cr = [i for i,v in enumerate(p_cr[0]) if v < pcross]
    
    
    # Sau đó ta chọn bất kỳ số chắn để tạo cặp 
    if len(chr_cr) % 2 != 0:
        choosen_chr_cr = random.sample(chr_cr, len(chr_cr) - 1)
    
    
    # Thực hiện lai  
    # Chọn ví trí bất kỳ bằng cách random idx_cr sau đó lai 
    for i in range(0,len(choosen_chr_cr),2):
        idx_cr = np.random.random_integers(0,len_chorom)
        chr1 = list(new_popu[choosen_chr_cr[i]][:idx_cr]) + list(new_popu[choosen_chr_cr[i+1]][idx_cr:])
        chr2 = list(new_popu[choosen_chr_cr[i+1]][:idx_cr]) + list(new_popu[choosen_chr_cr[i]][idx_cr:])
        new_popu[choosen_chr_cr[i]] = np.array(chr1)
        new_popu[choosen_chr_cr[i+1]] = np.array(chr2)
        
    
    # Random tạo xác suất đột biến cho từng bit của tất cả NST trong quần thể
    p_m = np.random.uniform(0,1,size=(pop_size,len_chorom))
    
    # Nếu mà tại bit nào có xác suất < xác suất đột biến pmul thì thực hiện đảo bit 
    for i in  range(pop_size):
        for j in range(len_chorom):
            if p_m[i][j] < pmul:
                if new_popu[i][j] == 1:
                    new_popu[i][j] = 0
                else:
                    new_popu[i][j] = 1

    popu = new_popu
    num_iteration = num_iteration + 1

print "**************************** Kết Quả ****************************************"
print "Cân nặng giới hạn là : " ,weight_limit
print "Túi tốt nhất có giá trị là : " + str(max_fitness) +" và nặng "+ str(res_weight) +"\n"
for i in range(len_chorom):
    if best_sol[i] == 1:
        print items[i].name,items[i].weight,items[i].value

