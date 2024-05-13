# 创建一个空数组
values = []
# 创建一个空的二维数组
two_dim_array = []
# 打开文本文件
with open('test_data.txt', 'r') as file:
    # 逐行读取文件内容
    for line in file:
        # 检查是否包含"------goal_position:"字段
        if '------goal_position:' in line:
            # 提取数据部分
            values_str = line.split('------goal_position: ')[1]
            # 分割数据为一个列表
            values_list = values_str.split(',')

            # 去除列表中每个元素的空格，并转换为整数
            values = [int(value.strip()) for value in values_list]
            two_dim_array.append(values)

# 打印二维数组
for row in two_dim_array:
    print(row)

# 提取第一行的第三个元素
element = two_dim_array[0][2]

# 打印提取的元素
print(element)
