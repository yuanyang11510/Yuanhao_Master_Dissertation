#将CHARACTER和COGID按照空格和换行符分割成最小单元（各5909个）
with open ("C:/Users/11510/Desktop/CHARACTER.txt","r",encoding="utf-8") as f1:
    text1=f1.read()
#print(text1)
list1=text1.split()
print("list1=",list1,"\nlen1=",len(list1))

with open ("C:/Users/11510/Desktop/COGID.txt","r",encoding="utf-8") as f2:
    text2=f2.read()
#print(text2)
list2=text2.split()
print("list2=",list2,"\nlen2=",len(list2))

#将CHARACTER和COGID的最小单元一一对应
list3=list(zip(list1,list2))
print("list3=",list3,"\nlen3=",len(list3))

#合并同类项得到不重复的CHARACTER-COGID对应元组构成的list
list4=[]
for x in list3:
    if x in list4:
        pass
    else:
        list4.append(x)
print("list4=",list4,"\nlen4=",len(list4))

#输出CHARACTER-COGID对应元组的频数
with open ("C:/Users/11510/Desktop/检查CHARACTER-COGID对应.txt","w",encoding="utf-8") as f3:
    f3.write("CHARACTER	COGID	FREQUENCY\n")
    for (x,y) in list4:
        f3.write(str(x)+"	"+str(y)+"	"+str(list3.count((x,y)))+"\n")