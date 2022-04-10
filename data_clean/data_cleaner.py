
if __name__ == "__main__":

    code_set = set() # set is a data structure, used to store non repeated elements. (= sql distinct)
    with open('data.csv') as f:
        lines = f.readlines()
        for line in lines:
            li = line.split('\t') # define a list, and split each line in csv then put them into the list.
            # print(li)
            code = li[0] # define code to store the first element in each row
            if code != '股票代码':
                code_set.add(code)

    print('股票代码数量统计：', len(code_set), '\n', '股票代码：', code_set)

    with open('rlt.txt', 'w') as f:
        f.writelines('股票代码数量统计：'+ str(len(code_set))+'\n')
        for c in code_set:
            f.writelines(c+',')