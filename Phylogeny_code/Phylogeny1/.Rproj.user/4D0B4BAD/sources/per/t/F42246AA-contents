#Phylolinguistique avec R (fabriqué par Thomas Pellard, site : https://tpellard.github.io/phylolinguistique/)
library(tidyverse)
library(phangorn)
library(ggtree)
library(tanggle)
library(TreeTools)

#1. Préparation des données
  #1.1. Import
    url <- "https://raw.githubusercontent.com/digling/edictor/master/data/BAI.tsv"
    download.file(url, "Data/BAI.tsv")
    lx <- read_tsv("Data/BAI.tsv", comment = "#") %>%#载入tsv文件
      select(-MORPHEMES)#因为MORPHEMES一列没有作用，所以直接删去（注意MORPHEME前面的负号）
    
    lx <- lx %>%
      mutate(DOCULECT = case_when(
        DOCULECT == "Gongxing" ~ "Magenta",
        DOCULECT == "Jinman" ~ "Cyan",
        DOCULECT == "Mazhelong" ~ "Jaune",
        DOCULECT == "Dashi" ~ "Vert",
        DOCULECT == "Zhoucheng" ~ "Violet",
        DOCULECT == "Jinxing" ~ "Orange",
        DOCULECT == "Tuolo" ~ "Rouge",
        DOCULECT == "Enqi" ~ "Bleu",
        DOCULECT == "Ega" ~ "Indigo",
      ))#将具体语言名替换成颜色名

  #1.2. Conversion
    lx_m <- lx %>%
      select(CONCEPT, DOCULECT, COGIDS) %>%#选择CONCEPT（似乎等同于CONCEPTID），DOCULECT和COGIDS三列
      distinct() %>%#删去相同内容的行（即同一个语言内部同源的不同形式，比如方言）
      pivot_wider(
        names_from = DOCULECT,
        values_from = CONCEPT,
        values_fill = 0,
        values_fn = length
      ) %>%#将DOCULECT一列变成抬头行（待研究pivot_wider命令），将同源词标记为1，非同源词标记为0
      select(-COGIDS)#删去COGIDS行；最后得到一个抬头行是所有的语言，接下来每一行是一组同源词标记0或1的矩阵

#A faire: Traitement des données marquantes    
        
    lx_phy <- phyDat(lx_m,
                     type = "USER",
                     levels = c(0, 1),
                     names = names(lx_m)
    )
    lx_phy#phyDat的功能待研究；可以得知有9列（语言），205行（同源形式COGID），其中不重复的有74列（同一个COGID/COGNAT SET下的同源模式）；待研究该命令中各项参数的意义
    
    write.phyDat(lx_phy, "Output/lx_phy.txt")#将上述信息保存在txt文件中；可以在""内的名称前加上路径，不加则默认保存在R文件所在的文件夹中
    #这个lx_phy很重要，是接下来获得汉明距离矩阵以及实施简约法的基础
    
#2. Méthodes par distance
  #2.1. Calcul des distances  
    lx_dist <- dist.hamming(lx_phy)#计算九种语言相互间的汉明距离（hamming distance）
    
    lx_dist_m <- as.matrix(lx_dist)#将这些距离表示为矩阵
    lx_dist_m[upper.tri(lx_dist_m)] <- NA#将矩阵上半部分的内容替换为NA（缺失值missing value,"Not Available"的缩写）
    options(knitr.kable.NA = "")#待研究knitr.kable命令
    knitr::kable(lx_dist_m, digits = 2)#待研究knitr::kable命令；将矩阵下半部分的距离保留两位小数
    
    lx_sim_m <- (1 - as.matrix(lx_dist)) * 100#由于两种语言间的汉明距离越低，表示两种语言越相似，因此可以通过上述公式将汉明距离转换成更直观的相似度系数
    lx_sim_m[upper.tri(lx_sim_m)] <- NA
    options(knitr.kable.NA = "")
    knitr::kable(lx_sim_m, digits = 2)
    
  #2.2. UPGMA
    lx_upgma <- upgma(lx_dist)
    lx_upgma#基于汉明距离通过UPGMA得到一棵有根且“超度量”（ultramétrique，何义？）的谱系树（唯一）
    write.tree(lx_upgma, "Output/lx_upgma.nwk")#nwk文件可以通过iTOL网站打开
    plot(lx_upgma)
    
    upgma_tree <- ggtree(lx_upgma) +
      geom_tiplab() +
      xlim_tree(0.14) +
      theme_tree()#调整谱系树的位置和大小方便查看（待研究这一命令中各个参数的意义）
    upgma_tree#在Plots中查看该课谱系树
    
  #2.3. Neighbour-joining
    lx_nj <- NJ(lx_dist)
    lx_nj#基于汉明距离通过neighbour-joining（邻接法）得到一棵无根且非超度量的谱系树（唯一）
    plot(lx_nj, "unrooted")
    plot(lx_nj, "tidy")#置根用于暂时直观地表现语言之间的关系（但这个结果往往是不准确的）
    
    nj_tree <- ggtree(lx_nj, layout = "daylight") +#daylight似乎是用来表示无根树的，待研究
      geom_tiplab2() +
      xlim(-.2, .09) +
      ylim(-.17, .12) +
      theme_tree()
    nj_tree

  #2.4. neighborNet
    lx_nn <- neighborNet(lx_dist)
    lx_nn#基于汉明距离通过neighbouring-net得到一张体现数据间冲突的网络（唯一）
    plot(lx_nn)
    
    nn_nx <- ggsplitnet(lx_nn) +
      geom_tiplab2() +
      xlim(-.15, .13) +
      ylim(-.16, .1) +
      theme_tree()
    nn_nx#不知为何此处得到的结果和教程上有略微差异，报错信息显示“Removed 3 rows containing missing values (`geom_segment()`)”

#3. Méthodes de parcimonie
  #3.1. Parcimonie générale (branch and bound)
    lx_bab <- bab(lx_phy)#基于lx_phy（待研究是什么性质）通过branch and bound（分支界定法）生成无根的谱系树（不唯一）；在分类单元数量在十余个时，适用该方法
    lx_bab#共生成四个同样简约的谱系树
    
    lx_bab <- acctran(lx_bab, lx_phy)#计算每棵谱系树中分支的“长度”（取最大值）
    write.tree(lx_bab, "Output/lx_bab.nwk")
    
    ggtree(lx_bab[[1]], layout = "daylight") +#[1]可以替换成[2/3/4]对应生成的四个谱系树
      geom_tiplab2() +
      xlim(-25, 45) + ylim(-30, 60) +
      theme_tree()#这一棵谱系树显示不全，似乎和xlim以及ylim当中的系数有关，如何确定这些系数，待研究
    
    ggtree(lx_bab[[2]], layout = "daylight") +
      geom_tiplab2() +
      xlim(-25, 45) + ylim(-30, 60) +
      theme_tree()
    
    ggtree(lx_bab[[3]], layout = "daylight") +
      geom_tiplab2() +
      xlim(-25, 45) + ylim(-30, 60) +
      theme_tree()
    
    ggtree(lx_bab[[4]], layout = "daylight") +
      geom_tiplab2() +
      xlim(-25, 45) + ylim(-30, 60) +
      theme_tree()

  #3.2. Parcimonie ratchet
    lx_pratchet <- pratchet(lx_phy)#基于lx_phy通过Parcimonie Ratchet(属于méthode heuristique启发法的一种)得到一棵无根的谱系树（唯一）；在分类单元数量在十余个以上时，适用该方法
    lx_pratchet <- acctran(lx_pratchet, lx_phy)
    lx_pratchet
    
    ggtree(lx_pratchet, layout = "daylight") +
      geom_tiplab2() +
      xlim(-70, 30) + ylim(-35, 45) +
      theme_tree()

#A faire : Parcimonie de Camin-Sokal et de Dollo
    
#4. Evaluation
  #4.1. Evaluation de la robustesse (UPGMA, bootstrap)
  #此处是以2.2.中通过UPGMA得到的谱系树为例，运用bootstrap（自助法）来测试每棵谱系树的每条分支的稳定性
    lx_m <- PhyDatToMatrix(lx_phy)#PhyDatToMatrix是为了重新得到数据的矩阵，但不知作用为何，待研究
    boot_upgma_hamming <- function(x) {
      upgma(dist.hamming(phyDat(x, type = "USER", levels = c(0, 1))))
    }#定义一个函数boot_upgma_hamming，将每次抽样的数据都转换成一个通过UPGMA得到的谱系树
    n_bs <- 1000#定义进行1000次取样
    
    set.seed(123456)#set.seed是为了固定"graine aléatoire"，确保结果的可复现性（reproductibilité），待研究
    lx_upgma_bs <- boot.phylo(lx_upgma,
                              lx_m,
                              boot_upgma_hamming,
                              B = n_bs,
                              trees = TRUE,
                              quiet = TRUE)#待研究该命令中每个参数的意义
    
    upgma_bs_scores <- prop.clades(lx_upgma, lx_upgma_bs$trees, rooted = TRUE)#符号$表示后者在前者当中
    upgma_support <- c(rep(n_bs, length(lx_phy)), upgma_bs_scores)
    upgma_support_pct <- upgma_support / n_bs#最后得到的是在1000次抽样中，依据每次抽样数据得到的1000棵谱系树中，与基于全部数据的UPGMA得到的谱系树的某个分支的位置相一致的数量
    #但关于以上三行代码的具体细节，待研究
  
    ggtree(lx_upgma) +
      geom_tiplab() +
      geom_nodelab(aes(label = upgma_support_pct), geom = "text", hjust = -.1) +#将上述通过bootstrap得到的谱系树中每个分支与基于全部数据的得到的谱系树对应分支的符合比例加到谱系树的分支上
      xlim_tree(0.14) +
      theme_tree()#但该命令中各个参数的意义，待研究

    upgma_support_pct[upgma_support_pct < .7] <- NA#将谱系树中符合比例低于0.7分支舍去，只显示符合比例高于0.7的分支
    
    ggtree(lx_upgma) +
      geom_tiplab() +
      geom_nodelab(aes(label = upgma_support_pct), geom = "text", hjust = -.1) +
      xlim_tree(0.14) +
      theme_tree()

    #4.2. Résumer l'accord entre des résultats (consensus tree)
    lx_bab_consensus <- consensus(lx_bab, p = 1)
    ggtree(lx_bab_consensus, layout = "daylight") +
      geom_tiplab2() +
      xlim(-4.75, 3.85) + ylim(-4.25, 4.75) +
      theme_tree()#得到一棵“严格一致树”(strict consensus tree, arbre consensus strict)，使其满足各分支符合所有可能的谱系树的情况
    
    lx_bab_consensus_mj <- consensus(lx_bab, p = .5)
    ggtree(lx_bab_consensus_mj, layout = "daylight") +
      geom_tiplab2() +
      xlim(-6, 5) + ylim(-5, 5.25) +
      theme_tree()#得到一棵“多数规则一致树”(majority-rule consensus tree, arbre consensus majoritaire)，使其满足各分支符合二分之一的谱系树的情况
    
#A faire: Score de parcimonie, CI, RI, etc.

    