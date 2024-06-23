#检测每个CONCEPT下不重复COGID的个数
#读取包含CONCEPT_ID和COGID的文件并转换为一一对应的CONCEPT_ID和COGID组成的list
with open ("C:/Users/11510/Desktop/CONCEPT-COGID_with borrowings.txt","r",encoding="utf-8") as f:
    text1=f.read()
list1=text1.split("\n")
print("list1=",list1,"\nlen1=",len(list1))
list2=[]
for x in list1:
    x_list=x.split("\t")
    list2.append(x_list)
print("list2=",list2,"\nlen2=",len(list2))

#按照CONCEPT_ID（设定为换行符）进行分割，使同一个CONCEPT_ID下的COGID归在一起
list3_2=[]#COGID
list3_2.append("1")
list3_1=[]#CONCEPT_ID
list3_1.append("1")
for x in range(1,len(list2)-1):
    x_list1=list2[x]
    x1=x_list1[0]
    y1=x_list1[1]
    
    x_list2=list2[x-1]
    x2=x_list2[0]
    y2=x_list2[1]
    if x1==x2:
        list3_2.append(y1)
        list3_1.append(x1)
    else:
        list3_2.append("\n")
        list3_2.append(y1)
        list3_1.append("\n")
        list3_1.append(x1)        
print("list3_2=",list3_2,"\nlen3=",len(list3_2))

#得到不重复的CONCEPT_ID组成的list
print("list3_1=",list3_1,"\nlen3_1=",len(list3_1))
list8=list(set(list3_1))
list8.remove("\n")
list9=[]
for x in list8:
    x=int(x)
    list9.append(x)
list9.sort()
print("list9=",list9,"\nlen9=",len(list9))

#过滤多余的逗号
text2=",".join(list3_2)
list4=text2.split("\n")
list5=[]
for x in list4:
    x=x.strip(",")
    list5.append(x)
print("list5=",list5,"\nlen5=",len(list5))

#将每组COGID组成的字符串转换为list方便转换为集合后计算不重复项的个数
list6=[]
for x in list5:
    x=x.split(",")
    list6.append(x)
print("list6=",list6,"\nlen6=",len(list6))  

#得到每一个CONCEPT_ID下不重复COGID的个数组成的list
list7=[]
for x in list6:
    set1=set(x)
    y=len(set1)
    list7.append(y)
print("list7=",list7,"\nlen7=",len(list7))

list7_1=set(list7)
print("list7_1=",list7_1,"\nlen7_1=",len(list7_1))

#将每一个CONCEPT_ID和该CONCEPT_ID下不重复的COGID的个数一一对应
list10=list(zip(list9,list7))
print("list10=",list10,"\nlen10=",len(list10))

#检测不重复COGID的个数大于10的CONCEPT_ID
for (x,y) in list10:
    if y ==9:
        index1=list10.index((x,y))
        print("CONCEPT",x,"=",y,">10")
        list10[index1]=(x,0)
print("list10=",list10,"\nlen10=",len(list10)) 
        
              

