#Phylolinguistique avec R (fabriqué par Thomas Pellard, site : https://tpellard.github.io/phylolinguistique/)
library(tidyverse)
library(phangorn)
library(ggtree)
library(tanggle)
library(TreeTools)
library(ggthemes)

#1. Préparation des données
  #1.1. Import
    url <- "https://raw.githubusercontent.com/digling/edictor/master/data/BAI.tsv"
    download.file(url, "Data/BAI.tsv")
    lx_orig <- read_tsv("Data/BAI.tsv", comment = "#")
    lx <- lx_orig %>%
    select(CONCEPTID, DOCULECT, COGIDS) %>% 
    distinct()
      
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
      ))

  # 1.2. Conversion
    # 1.2.1. Etats multiples#多元性状模式，实际是以每个CONCEPT作为一个CHARACTER，以每个CONCEPT下面的COGID作为CHARACTER的不同状态（0~9，如果超过10个状态可以用字母表示）
    lx_multi <- lx %>%
      group_by(CONCEPTID) %>%
      mutate(COGIDS = as.factor(COGIDS) %>% as.numeric()) %>%
      group_by(DOCULECT, CONCEPTID) %>%
    
      summarise(COGIDS = paste0(COGIDS, collapse = "")) %>%
      ungroup() %>%
      mutate(COGIDS = ifelse(str_detect(COGIDS, "..+"), paste0("{", COGIDS, "}"), COGIDS)) %>%
      pivot_wider(
        names_from = CONCEPTID,
        values_from = COGIDS,
        values_fill = "?",
      )%>%
    arrange(DOCULECT)
    
    lx_phy_multi <- lx_multi %>%
      column_to_rownames("DOCULECT") %>%
      as.matrix() %>%
      MatrixToPhyDat()
  
    write.phyDat(lx_phy_multi, "Output/lx_phy_multi.nex", format = "nexus")
    
    #1.2.2. Etats binaires#二元性状模式，实际是以每个COGID作为一个CHARACTER，以每门语言的每个COGID的存在与否作为CHARACTER的状态（1，存在/0，不存在）
    lx_bin <- lx %>%
      rowid_to_column() %>%
      pivot_wider(
        names_from = DOCULECT,
        values_from = rowid,
        values_fill = 0,
        values_fn = length
      ) %>%
      pivot_longer(cols = !(CONCEPTID | COGIDS), names_to = "DOCULECT", values_to = "VALUE") %>%
      mutate(VALUE = as.character(VALUE)) %>%
      group_by(CONCEPTID, DOCULECT) %>%
      mutate(VALUE = ifelse(sum(VALUE != "0") == 0, "?", VALUE)) %>%
      ungroup() %>%
      mutate(id = paste0(CONCEPTID, "_", COGIDS)) %>%
      select(DOCULECT, id, VALUE) %>%
      pivot_wider(
        names_from = id,
        values_from = VALUE
      )
    
    lx_phy_bin <- lx_bin %>%
      column_to_rownames("DOCULECT") %>%
      as.matrix() %>%
      MatrixToPhyDat()
    lx_phy_bin
        
    write.phyDat(lx_phy_bin, "Output/lx_phy_bin.nex", format = "nexus")
    
#2. Méthodes par distance
  #2.1. Calcul des distances 
    lx_phy <- ReadAsPhyDat("Output/lx_phy_multi.nex")#多元模式比起二元模式可以降低那些【拥有太多COGID的CONCEPT】导致的偏误
    lx_dist <- dist.hamming(lx_phy)
    
    lx_dist_m <- as.matrix(lx_dist)
    lx_dist_m[upper.tri(lx_dist_m)] <- NA
    options(knitr.kable.NA = "")
    knitr::kable(lx_dist_m, digits = 2)
    
    lx_sim_m <- (1 - as.matrix(lx_dist)) * 100
    lx_sim_m[upper.tri(lx_sim_m)] <- NA
    options(knitr.kable.NA = "")
    knitr::kable(lx_sim_m, digits = 2)
    
  #2.2. UPGMA
    lx_upgma <- upgma(lx_dist)
    lx_upgma
    
    write.tree(lx_upgma, "Output/lx_upgma.tree")
    plot(lx_upgma)
    
  #2.3. Neighbour-joining
    lx_nj <- NJ(lx_dist)
    lx_nj
    plot(lx_nj, "unrooted")
    plot(lx_nj, "tidy")

  #2.4. neighborNet
    lx_nn <- neighborNet(lx_dist)
    lx_nn
    plot(lx_nn)

#3. Méthodes de maximum de parcimonie
  #3.1. Parcimonie ratchet
    lx_phy <- ReadAsPhyDat("Output/lx_phy_multi.nex")
    lx_mp <- pratchet(lx_phy, trace = 0, minit = 1000, k = 100, method = "sankoff", all = TRUE)
    lx_mp
    plot(lx_mp, "unrooted")

    lx_mp_bl <- acctran(lx_mp, lx_phy)
    lx_mp_bl
    plot(lx_mp_bl, "unrooted")
    plot(midpoint(lx_mp_bl))#在两个分歧最大的分支之间置根，这种方法假定演化的速率是恒定的，因此拓扑结构是平衡的
    
    lx_mp_r <- RootTree(lx_mp, "Violet") %>% #假定"Violet"为外类群之后置根，这种方法必须先确定一个外类群
      acctran(lx_phy)
    plot(lx_mp_r)
    
    write.tree(lx_mp_r, "Output/lx_mp.tree")
    write_rds(lx_mp_r, "Output/lx_mp.rds")
    
  #3.2. Mesures d'homoplasie et de cohérence
    #3.2.1. Consistency index (CI), indice de cohérence
    m <- phangorn:::lowerBound(lx_phy)[attr(lx_phy, "index")]#得到每个character假定的最小变化数
    s <- sankoff(lx_mp_r, lx_phy, site = "site")[attr(lx_phy, "index")]#得到每个character实际的变化数
    h <- s - m
    h#得到每个character的homoplasy的个数
    H <- sum(h)
    H#homoplasy的总数
    which(h > 0)#检测哪些character上发生了homoplasy
    sankoff(lx_mp_r, lx_phy)
    sum(s)#得到整棵树所有character的实际变化数（树长）
    
    ci <- CI(lx_mp_r, lx_phy, sitewise = TRUE)
    ci#得到每个character(此处即110个CONCEPT)的ci
    CI(lx_mp_r, lx_phy)#得到整棵树的CI
    sum(m)/sum(s)
    #CI值越小，表明homoplasy越多，当CI值为1时最大，表明不存在homoplasy
    
    #3.2.2. Rescaled consistency index (RCI), indice de cohérence à l'échelle
    #CI的局限性之一：CI实际的范围往往没有0-1那末大
    #CI的局限性之二：autapomorphy的CI是1（仅在一个分类单元(此处即DOCULECT)上改变了一次），会影响CI的有效性，比如在某些CONCEPT下，只有一个DOCULECT的COGID和其他DOCULECT的COGID不同
    #CI的局限性之三：分类单元越多，CI值往往越小，即假定出现更多的homoplasy
    #见《植物系统学》21-22
    g <- phangorn:::upperBound(lx_phy)[attr(lx_phy, "index")]
    g#得到每个character假定的最大变化数
    rci <- RI(lx_mp_r, lx_phy, sitewise = TRUE) * CI(lx_mp_r, lx_phy, sitewise = TRUE)
    rci#得到每个character的rci
    CI(lx_mp_r, lx_phy) * RI(lx_mp_r, lx_phy)#得到整棵树的RCI
    
    d <- h/(g - m)
    d#得到每个character的distortion coefficient, coefficient de distortation
    D <- sum(h)/(sum(g) - sum(m))
    D#得到整棵树的distortation coefficient
    
    ri <- RI(lx_mp_r, lx_phy, sitewise = TRUE)
    ri#得到每个character的ri(retention index), indice de rétention
    RI <- RI(lx_mp_r, lx_phy)
    RI#得到整棵树的RI
    1 - D#RI和D相加等于一
    
    #3.2.3.比较UPGMA和MP(Ratchet)两棵树的S/H/CI/RCI/RI/D
    lx_upgma <- read.tree("Output/lx_upgma.tree")
    tr <- c(lx_mp_r, lx_upgma)
    nms <- c("MP", "UPGMA")
    comp_tb <- map(seq_along(tr), function(i){
      m_x <- phangorn:::lowerBound(lx_phy)[attr(lx_phy, "index")]
      s_x <- sankoff(tr[[i]], lx_phy, site = "site")[attr(lx_phy, "index")]
      h_x <- s_x - m_x
      CI_x <- CI(tr[[i]], lx_phy)
      RI_x <- RI(tr[[i]], lx_phy)
      df <- tribble(
        ~var, ~value,
        "S", sum(s_x),
        "H", sum(h_x),
        "CI", CI_x,
        "RCI", CI_x * RI_x,
        "RI", RI_x,
        "D", 1 - RI_x
      )
      colnames(df)[2] <- nms[i]
      df
    }) %>% 
      reduce(left_join)
    write_tsv(comp_tb, "Output/comp_tb.tsv")
    #一般来说，MP相比起UPGMA会有更大的CI/RI/RCI和更小的D
    
#4. Evaluation
  #4.1. Evaluation de la stabilité des clades
    #4.1.1.以2.2.中通过UPGMA得到的谱系树为例，运用bootstrap（自助法）来测试每棵谱系树的每条分支的稳定性
      lx_phy <- ReadAsPhyDat("Output/lx_phy_multi.nex")
      lx_upgma <- read.tree("Output/lx_upgma.tree")
      lx_m <- PhyDatToMatrix(lx_phy)
      
      boot_upgma_hamming <- function(x) {
        upgma(Hamming(MatrixToPhyDat(x)))
      }
      n_bs <- 1000
      
      set.seed(123456)
      lx_upgma_bs <- boot.phylo(lx_upgma,
                                lx_m,
                                boot_upgma_hamming,
                                B = n_bs,
                                trees = TRUE,
                                quiet = TRUE
      )
      
      upgma_bs_scores <- prop.clades(lx_upgma, lx_upgma_bs$trees, rooted = TRUE)
      upgma_support_pct <- upgma_bs_scores / n_bs
      lx_upgma$node.label <- upgma_support_pct
      plot(lx_upgma, show.node.label = TRUE)
      
      upgma_support_pct[upgma_support_pct < .7] <- NA
      lx_upgma$node.label <- upgma_support_pct
      plot(lx_upgma, show.node.label = TRUE)
      
      plotBS(lx_upgma, lx_upgma_bs$trees)#另一种更简单的方法，结果会有些许差异
      plotBS(lx_upgma, lx_upgma_bs$trees, p = 70)
  
      #4.1.2.以3.1.中通过MP(Ratchet)得到的谱系树为例，运用bootstrap（自助法）来测试每棵谱系树的每条分支的稳定性
      lx_mp <- read_rds("Output/lx_mp.rds")
      plotBS(lx_mp, p = .7)
    
    #4.2. Résumer l'accord entre des résultats (consensus tree)
    trees <- map(1:3, ~ rtree(n = 9))#为了便于举例，随机生成一些树
    trees <- as.multiPhylo(c(trees[1], trees[1], trees[1], trees, trees))
    tree_sc <- consensus(trees, p = 1)
    plot(tree_sc)#arbre consensus strict
    
    tree_mc <- consensus(trees, p = .5)
    plot(tree_mc)#arbre consensus majoritaire
    
    #4.3. Mesures du degré d'aborescence
    #检验数据能够表示为树状结构的可能性
      #4.3.1. Score δ (用于衡量一系列数据之间的冲突程度)
      #此处衡量的对象是DOCULECT之间的距离
      lx_delta <- lx_phy %>% 
        Hamming() %>% 
        delta.plot()
      lx_delta#得到所有DOCULECT四元组的δ值的直方图，以及每个DOCULECT的δ值的平均值
      
      lx_delta$delta.bar#得到每个DOCULECT的δ值的平均值
      mean(lx_delta$delta.bar)#得到所有DOCULECT的δ值的平均值
      
      #定义新函数用于输出所有的δ值/所有的δ值的平均值/所有的δ值的标准差
      delta.score2 <- function(x, arg = "mean", f = phangorn:::delta.quartet) {
        dist.dna <- as.matrix(x)
        all.quartets <- t(combn(attributes(x)$Labels, 4))
        delta.values <- apply(
          all.quartets[, ], 1, f,
          dist.dna
        )
        if (!arg %in% c("all", "mean", "sd")) {
          stop("return options are: all, mean, or sd")
        }
        if (arg == "all") {
          return(delta.values)
        }
        if (arg == "mean") {
          return(mean(delta.values))
        }
        if (arg == "sd") {
          return(sd(delta.values))
        }
      }
      
      lx_dist <- Hamming(lx_phy)
      delta.score2(lx_dist, "all")#得到所有DOCULECT四元组的δ值
      delta.score2(lx_dist, "mean")#得到所有DOCULECT四元组的δ值的平均值
      delta.score2(lx_dist, "all") %>% mean()
      
      #得到所有DOCULECT四元组的δ值的分布图象
      delta.score2(lx_dist, "all") %>%
        enframe() %>%
        ggplot(aes(x = value)) +
        geom_density(fill = few_pal("Medium")(2)[1], color = few_pal("Dark")(2)[1]) +
        xlab("δ") +
        theme_minimal()
      
      #4.3.2. Score de résidus Q
      #定义新函数用于计算Q值
      qresid.score <- function(quartet, dist.dna) {
        m1 <- dist.dna[quartet[1], quartet[2]] + dist.dna[
          quartet[3],
          quartet[4]
        ]
        m2 <- dist.dna[quartet[1], quartet[3]] + dist.dna[
          quartet[2],
          quartet[4]
        ]
        m3 <- dist.dna[quartet[1], quartet[4]] + dist.dna[
          quartet[2],
          quartet[3]
        ]
        m <- sort(c(m1, m2, m3), decreasing = TRUE)
        ret <- (m[1] - m[2])^2
        return(ret)
      }
      lx_dist2 <- lx_dist/mean(lx_dist)
      delta.score2(lx_dist2, "mean", f = qresid.score)#得到所有DOCULECT四元组的Q值的平均值
      
      #得到所有DOCULECT四元组的Q值的分布图象
      delta.score2(lx_dist2, "all", f = qresid.score) %>%
        enframe() %>%
        ggplot(aes(x = value)) +
        geom_density(fill = few_pal("Medium")(2)[1], color = few_pal("Dark")(2)[1]) +
        xlab("Q-residual") +
        theme_minimal()
      
      #比较δ值和Q值
      ds <- delta.score2(lx_dist, "all")
      qr <- delta.score2(lx_dist2, "all", f = qresid.score)
      tibble(ds, qr) %>%
        ggplot(aes(x = ds, y = qr)) +
        geom_vline(xintercept = mean(ds), linewidth = .4) +
        geom_hline(yintercept = mean(qr), linewidth = .4) +
        geom_point(color = few_pal("Dark")(2)[2], fill = few_pal("Dark")(2)[2], pch = 21, alpha = .5, size = 4) +
        xlab("δ") +
        ylab("Q-residual") +
        theme_minimal()
      
      #比较每个DOCULECT的δ值和Q值
      dsqr_bytaxon <- t(combn(names(lx_phy), 4)) %>%
        as_tibble() %>%
        mutate(ds, qr) %>%
        pivot_longer(cols = 1:4, names_to = NULL, values_to = "taxon")
      dsqr_bytaxon_mean <- dsqr_bytaxon %>%
        group_by(taxon) %>%
        summarise(across(ds:qr, mean)) %>%
        arrange(ds, qr)
      
      #比较每个DOCULECT的δ值-Q值图象和所有DOCULECT的δ值-Q值图象
      dsqr_bytaxon %>%
        ggplot(aes(x = ds, y = qr, color = taxon, fill = taxon)) +
        geom_vline(data = dsqr_bytaxon_mean, aes(xintercept = ds, color = taxon), linewidth = .4) +
        geom_hline(data = dsqr_bytaxon_mean, aes(yintercept = qr, color = taxon), linewidth = .4) +
        geom_vline(xintercept = mean(ds), linewidth = .4, linetype = "dashed") +
        geom_hline(yintercept = mean(qr), linewidth = .4, linetype = "dashed") +
        geom_point(pch = 21, alpha = .5, size = 2) +
        xlab("δ") +
        ylab("Q-residual") +
        facet_wrap(~taxon) +
        scale_color_ptol() +
        scale_fill_ptol() +
        theme_minimal() +
        theme(legend.position = "none")
      