#赋予词partial COGID（暂时不考虑无字音节C）
with open ("C:/Users/11510/Desktop/Partial COGIDS(word saillant).txt","w",encoding="utf-8") as f7:
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
            char_COGID=lst3.index(character)+1#这是不精确的，因为存在同形不同源或者同源不同形的问题
            f7.write(str(char_COGID))