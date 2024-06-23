#一、过滤掉word non saillant
#所有词
with open ("path1", "r",encoding="utf-8") as f1:
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
with open ("path2",encoding="utf-8") as f2:
    for x in lst3:
        frequency=lst2.count(x)
        sentence = x+"出现了"+str(frequency)+"次\n"
        f2.write(sentence)

#无字音节C的个数
print("无字音节C出现了"+str(lst2.count("C"))+"次")

#降序字频（无字音节C暂时视为同一音节）
with open ("path3","w",encoding="utf-8") as f3:
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

with open ("path4","w",encoding="utf-8") as f4:
    f4.write("character	Partial COGIDS\n")
#     f4.write(x+"	"+str(lst3.index(x)+1)+"\n")#另一种表示方法
    for COGID1,character in lst5:
        f4.write(character+"	"+str(COGID1)+"\n")

#用zip函数匹配汉字和层次标注
with open ("path5","r",encoding="utf-8") as f5:
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

with open ("path6","w",encoding="utf-8") as f6:
    f6.write("Word saillant\n")
    for x in lst1:
        f6.write(x)

#二、赋予词partial COGID（暂时不考虑无字音节C）
with open ("path7",encoding="utf-8") as f7:
    f7.write("Partial COGIDS\n")
    it=iter(range(35))#迭代器对象
    for character in lst1:
        if character in ["\n", " "]:
            f7.write(character)
        elif character == "C":
#将无字音节C从749（748是最后一个有字音节的COGID）到783（一共有35个无字音节C）依次赋予partial COGID            
            char_COGID=749+next(it)
            f7.write(str(char_COGID))
        else:
            char_COGID=lst3.index(character)+1
            f7.write(str(char_COGID))

#三、Partial COGIDS转换为Full COGIDS
#不考虑层次的COGID转换
#依据换行符分割词（共4302个词）
with open ("path8","r",encoding="utf-8") as f8:
    text1=f8.read()
#print(text1)
lst1=text1.split("\n")
print("lst1 =", lst1)
print(len(lst1))

#合并同类项得到不重合的词构成的list（共859个词）
lst2=[]
for x in lst1:
    if x in lst2:
        pass
    else:
        lst2.append(x)
print("lst2 =", lst2)
print(len(lst2))

#为每个词赋予Full COGID
lst3=list(enumerate(lst2,start=1))
print("lst3 =", lst3)
with open ("path9",encoding="utf-8") as f9:
    f9.write("Word with borrowing2	Full COGID\n")
    for x in lst1:
        Full_COGID1=lst2.index(x)+1#另一种表现方法
        f9.write(x+"	"+str(Full_COGID1)+"\n")

#排除借词的COGID转换
#依据换行符分割词（共3660个词）
with open ("path10","r",encoding="utf-8") as f10:
    text2=f10.read()
#print(text1)
lst4=text2.split("\n")
print("lst4 =", lst4)
print(len(lst4))

#合并同类项得到不重合的词构成的list（共775个词）
lst5=[]
for x in lst4:
    if x in lst5:
        pass
    else:
        lst5.append(x)
print("lst5 =", lst5)
print(len(lst5))

#为每个词赋予Full COGID
lst6=list(enumerate(lst5,start=1))
print("lst6 =", lst6)
with open ("path11","w",encoding="utf-8") as f11:
    f11.write("Word without borrowing2	Full COGID\n")
    for x in lst4:
        Full_COGID1=lst5.index(x)+1#另一种表现方法
        f11.write(x+"	"+str(Full_COGID1)+"\n")        
