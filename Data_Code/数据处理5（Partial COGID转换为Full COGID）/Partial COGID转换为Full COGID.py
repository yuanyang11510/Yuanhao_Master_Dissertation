#Partial COGIDS转换为Full COGIDS
#不考虑层次的COGID转换
#依据换行符分割词（共4302个词）
with open ("C:/Users/11510/Desktop/Partial COGIDS avec.txt","r",encoding="utf-8") as f8:
    text1=f8.read()
#print(text1)
list1=text1.split("\n")
print("list1=",list1,"len1=",len(list1))

#合并同类项得到不重合的词构成的list（共840个词）
list2=[]
for x in list1:
    if x in list2:
        pass
    else:
        list2.append(x)
print("list2=",list2,"len2=",len(list2))

#为每个词赋予Full COGID
list3=list(enumerate(list2,start=1))
print("list3=",list3,"len3=",len(list3))
with open ("C:/Users/11510/Desktop/Full COGIDS avec.txt","w",encoding="utf-8") as f9:
    f9.write("Full COGID\n")
    for x in list1:
        Full_COGID1=list2.index(x)+1#另一种表现方法
        f9.write(str(Full_COGID1)+"\n")

#排除借词的COGID转换
#依据换行符分割词（共3662个词）
with open ("C:/Users/11510/Desktop/Partial COGIDS sans.txt","r",encoding="utf-8") as f10:
    text2=f10.read()
#print(text1)
list4=text2.split("\n")
print("list4=",list4,"len4=",len(list4))

#合并同类项得到不重合的词构成的list（共764个词）
list5=[]
for x in list4:
    if x in list5:
        pass
    else:
        list5.append(x)
print("list5=",list5,"len5=",len(list5))

#为每个词赋予Full COGID
list6=list(enumerate(list5,start=1))
print("list6=",list6,"len6=",len(list6))
with open ("C:/Users/11510/Desktop/Full COGIDS sans.txt","w",encoding="utf-8") as f11:
    f11.write("Full COGID\n")
    for x in list4:
        Full_COGID1=list5.index(x)+1#另一种表现方法
        f11.write(str(Full_COGID1)+"\n")        



