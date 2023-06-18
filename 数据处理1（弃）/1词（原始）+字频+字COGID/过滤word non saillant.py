#过滤掉word non saillant
#所有词
with open ("C:/Users/11510/Desktop/词（原始）.txt", "r",encoding="utf-8") as f1:
    char=f1.read()
#print("char =", char)

#依据所有词构建的list
lst1=list(char)
print("lst1 =", lst1)
# for x in lst1:
#     if x == "\n":
#         lst1.remove(x)
#     elif x== " "#这种方法会导致最后剩下一个" "没有被移除，原因暂时不清楚
#         lst1.remove(x)
#     else:
#         pass
# print(lst1)

#过滤掉空格和换行符
lst2=[]
for x in lst1:
    if x in [" ", "\n"]:
        pass
    else:
        lst2.append(x)
print("lst2 =", lst2)

#合并同类项后不重复汉字构成的list（但是每个C都是不同的音节，这里暂时视为相同的音节）
lst3=[]
for x in lst2:
    if x not in lst3:
        lst3.append(x)
    else:
        pass
print("lst3 =", lst3)

#按照汉字原来出现的顺序排列的字频（无字音节C暂时视为同一音节）
with open ("C:/Users/11510/Desktop/汉字字频.txt","w",encoding="utf-8") as f2:
    for x in lst3:
        frequency=lst2.count(x)
        sentence = x+"出现了"+str(frequency)+"次\n"
        f2.write(sentence)

#无字音节C的个数
print("无字音节C出现了"+str(lst2.count("C"))+"次")

#降序字频（无字音节C暂时视为同一音节）
with open ("C:/Users/11510/Desktop/汉字字频（降序）.txt","w",encoding="utf-8") as f3:
    dic1={}
    for x in lst3:
        dic1[x]=lst2.count(x)
    print("dic1 =", dic1)
    
    lst4 = sorted(dic1.items(), key=lambda x:x[1], reverse=True)
    print("lst4 =", lst4)
    for character,frequency in lst4:
        sentence = character+"出现了"+str(frequency)+"次\n"
        f3.write(sentence)

#赋予单个汉字partial COGID（无字音节C除外）
lst3.remove("C")
print("lst3 =", lst3)
lst5=list(enumerate(lst3, start=1))
print("lst5 =", lst5)

with open ("C:/Users/11510/Desktop/Partial COGIDS(character).txt","w",encoding="utf-8") as f4:
    f4.write("character	Partial COGIDS\n")
#     f4.write(x+"	"+str(lst3.index(x)+1)+"\n")#另一种表示方法
    for COGID1,character in lst5:
        f4.write(character+"	"+str(COGID1)+"\n")

#用zip函数匹配汉字和层次标注
with open ("C:/Users/11510/Desktop/WENYAN.txt","r",encoding="utf-8") as f5:
    wenyan=f5.read()
#print("wenyan =", wenyan)
print("lst1 =", lst1)
lst6=list(wenyan)
print("lst6 =", lst6)
print(len(lst1))
print(len(lst6))#验证音节和层次标注间的一一对应
lst7=list(zip(lst1,lst6))
print("lst7 =", lst7)
#过滤掉标注为0（non saillant）的音节
lst8=[]
for (x,y) in lst7:
    if y=="0":
       pass
    else:
        lst8.append((x,y))
print("lst8 =", lst8)
tuple1, tuple6=zip(*lst8)
lst1=list(tuple1)
lst6=list(tuple6)
print("lst1 =", lst1)
print("lst6 =", lst6)

with open ("C:/Users/11510/Desktop/词(saillant).txt","w",encoding="utf-8") as f6:
    f6.write("Word saillant\n")
    for x in lst1:
        f6.write(x)

