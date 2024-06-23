#读取原始的CHARACTER,COGID和WENYAN并依据换行符分割成大单元（各有4302个大单元）
with open ("C:/Users/11510/Desktop/CHARACTER.txt","r",encoding="utf-8") as f1:
    text1=f1.read()
#print(text1)
list1=text1.split("\n")

with open ("C:/Users/11510/Desktop/COGID.txt","r",encoding="utf-8") as f2:
    text2=f2.read()
#print(text2)
list2=text2.split("\n")

with open ("C:/Users/11510/Desktop/WENYAN.txt","r",encoding="utf-8") as f3:
    text3=f3.read()
#print(text3)
list3=text3.split("\n")
print("list1=",list1,"\nlen1=",len(list1))
print("list2=",list2,"\nlen2=",len(list2))
print("list3=",list3,"\nlen3=",len(list3))

#消除CHARACTER,COGID和WENYAN中多余的空格
list4,list5,list6=[],[],[]
for x in list1:
    x=x.strip(" ")
    x=" ".join(x.split())
    list4.append(x)
for y in list2:    
    y=y.strip(" ")
    y=" ".join(y.split())
    list5.append(y)
for z in list3:    
    z=z.strip(" ")
    z=" ".join(z.split())
    list6.append(z)
print("list4=",list4,"\nlen4=",len(list4))
print("list5=",list5,"\nlen5=",len(list5))
print("list6=",list6,"\nlen6=",len(list6))
text4="\n".join(list4)
text5="\n".join(list5)
text6="\n".join(list6)
#原始数据手动输入的最低标准:每一个CONCEPT下的CHARACTER,COGID和WENYAN内部最小单元的个数是相同的
#若消除多余空格后长度仍然一致则基本可以认为符合该标准，但是精确检测需要另外设计算法，此处不讨论（M. List已经帮忙检测出WENYAN中遗漏的最小单元）

#写入文件
with open ("C:/Users/11510/Desktop/CHARACTER_arranged.txt","w",encoding="utf-8") as f4:
    f4.write("CHRACTERS\n"+text4)
with open ("C:/Users/11510/Desktop/COGID_arranged.txt","w",encoding="utf-8") as f5:
    f5.write("COGIDS\n"+text5)
with open ("C:/Users/11510/Desktop/WENYAN_arranged.txt","w",encoding="utf-8") as f6:
    f6.write("WENYAN\n"+text6)
#自此，CHARACTER,COGID和WENYAN达到了严格的一一对应

#，方便下面对CHARACTER,COGID和WENYAN（尤其是COGID）进行严格分列
# #一方面，将CHRACTER,COGID和WENYAN分解为不含空格/换行符（排列格局）的最小单元（各有5909个最小单元）
# list7=text4.split()#也可以是text1
# list8=text5.split()#也可以是text2
# list9=text6.split()#也可以是text3
# print("list7=",list7,"\nlen7=",len(list7))
# print("list8=",list8,"\nlen8=",len(list8))
# print("list9=",list9,"\nlen9=",len(list9))

# #用zip函数对齐CHARACTER,COGID和WENYAN的最小单元
# list10=list(zip(list7,list8,list9))
# print("list10=",list10,"\nlen10=",len(list10))
# 
# #过滤WENYAN中标注为0（non salient）的音节（过滤后各有5415个最小单元）
# list11=[]
# for (x,y,z) in list10:
#     if z=="0":
#        pass
#     else:
#         list11.append((x,y,z))
# print("list11=",list11,"\nlen11=",len(list11))
# tuple1,tuple2,tuple3=zip(*list11)
# list12=list(tuple1)
# list13=list(tuple2)
# list14=list(tuple3)
# print("list12=",list12,"\nlen12=",len(list12))
# print("list13=",list13,"\nlen13=",len(list13))
# print("list14=",list14,"\nlen14=",len(list14))

# #现有：
# #含有空格/换行符（分布格局）的CHARACTER,COGID和WENYAN的最小单元
# #不含有空格/换行符（分布格局）的过滤掉syllable non salient之后的CHRACTER,COGID和WENYAN的最小单元
# #由此得到过滤掉syllable non salient的CHARACTER,COGID和WENYAN的大单元（大单元=最小单元+分布格局）
#以上走了弯路，可以忽略

#另一方面，将CHARACTER,COGID和WENYAN分解为最小单元（包括空格/换行符，各有11818个最小单元）
list15,list16,list17=[],[],[]
for x in list4:
    x1=x.replace(" "," / ")
    x2=x1.split()
    x2.append("\n")
    for x in x2:
        list15.append(x)
for y in list5:
    y1=y.replace(" "," / ")#此处将空格替换为" / "非常关键，若替换乘双空格"  "，后续分割出的空格会变成零字符""
    y2=y1.split()
    y2.append("\n")#为每个大单元最后加上换行符
    for y in y2:
        list16.append(y)
for z in list6:
    z1=z.replace(" "," / ")
    z2=z1.split()
    z2.append("\n")
    for z in z2:
        list17.append(z)
print("list15=",list15,"\nlen15=",len(list15))
print("list16=",list16,"\nlen16=",len(list16))
print("list17=",list17,"\nlen17=",len(list17))  
#实际上对于CHARACTER和WENYAN，可以直接使用list()函数进行分割，因为它们的最小单元（包括空格/换行符）都是一个字符，
#但是COGID的最小单元长度是不确定的，因此不适用此方法，此处专门为COGID设计了算法，并且该算法同样适用于CHARACTER和COGID

#用zip函数对齐CHARACTER,COGID和WENYAN的最小单元
list18=list(zip(list15,list16,list17))
print("list18=",list18,"\nlen18=",len(list18))

#过滤WENYAN中标注为0（non salient）的音节（过滤后各有11324个最小单元，即过滤掉了11818-11324=494个字）
list19=[]
for (x,y,z) in list18:
    if z=="0":
       pass
    else:
        list19.append((x,y,z))
print("list19=",list19,"\nlen11=",len(list19))
tuple1,tuple2,tuple3=zip(*list19)
list20=list(tuple1)
list21=list(tuple2)
list22=list(tuple3)
print("list20=",list22,"\nlen20=",len(list20))
print("list21=",list21,"\nlen21=",len(list21))
print("list22=",list22,"\nlen22=",len(list22)) 

#将"/"替换回空格
list23,list24,list25=[],[],[]
for x in list20:
    if x =="/":
        list23.append(" ")
    else:
        list23.append(x)
for y in list21:
    if y =="/":
        list24.append(" ")
    else:
        list24.append(y)
for z in list22:
    if z =="/":
        list25.append(" ")
    else:
        list25.append(z)        
print("list23=",list23,"\nlen23=",len(list23))
print("list24=",list24,"\nlen24=",len(list24))
print("list25=",list25,"\nlen25=",len(list25))

#再次消除CHARACTER,COGID和WENYAN中多余的空格
text7="".join(list23)
text8="".join(list24)
text9="".join(list25)
list26=text7.split("\n")
list27=text8.split("\n")
list28=text9.split("\n")
print("list26=",list26,"\nlen26=",len(list26))
print("list27=",list27,"\nlen27=",len(list27))
print("list28=",list28,"\nlen28=",len(list28))

list29,list30,list31=[],[],[]
for x in list26:
    x=x.strip(" ")
    x=" ".join(x.split())
    list29.append(x)
for y in list27:    
    y=y.strip(" ")
    y=" ".join(y.split())
    list30.append(y)
for z in list28:    
    z=z.strip(" ")
    z=" ".join(z.split())
    list31.append(z)
print("list29=",list29,"\nlen29=",len(list29))
print("list29=",list30,"\nlen30=",len(list30))
print("list30=",list31,"\nlen31=",len(list31))
text10="\n".join(list29)
text11="\n".join(list30)
text12="\n".join(list31)

#写入文件
with open ("C:/Users/11510/Desktop/CHARACTER_salient.txt","w",encoding="utf-8") as f7:
    f7.write("CHRACTERS\n"+text10)
with open ("C:/Users/11510/Desktop/COGID_salient.txt","w",encoding="utf-8") as f8:
    f8.write("COGIDS\n"+text11)
with open ("C:/Users/11510/Desktop/WENYAN_salient.txt","w",encoding="utf-8") as f9:
    f9.write("WENYAN\n"+text12)