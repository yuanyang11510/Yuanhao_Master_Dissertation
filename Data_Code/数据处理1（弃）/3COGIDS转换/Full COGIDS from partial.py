#Partial COGIDS转换为Full COGIDS
#不考虑层次的COGID转换
#依据换行符分割词（共4302个词）
with open ("C:/Users/11510/Desktop/Partial COGIDS avec.txt","r",encoding="utf-8") as f8:
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
with open ("C:/Users/11510/Desktop/Full COGIDS avec.txt","w",encoding="utf-8") as f9:
    f9.write("Word with borrowing2	Full COGID\n")
    for x in lst1:
        Full_COGID1=lst2.index(x)+1#另一种表现方法
        f9.write(x+"	"+str(Full_COGID1)+"\n")

#排除借词的COGID转换
#依据换行符分割词（共3660个词）
with open ("C:/Users/11510/Desktop/Partial COGIDS sans.txt","r",encoding="utf-8") as f10:
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
with open ("C:/Users/11510/Desktop/Full COGIDS sans.txt","w",encoding="utf-8") as f11:
    f11.write("Word without borrowing2	Full COGID\n")
    for x in lst4:
        Full_COGID1=lst5.index(x)+1#另一种表现方法
        f11.write(x+"	"+str(Full_COGID1)+"\n")        



