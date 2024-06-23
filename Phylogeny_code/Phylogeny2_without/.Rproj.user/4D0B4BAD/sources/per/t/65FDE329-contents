#Phylolinguistique avec R (fabriqué par Thomas Pellard, site : https://tpellard.github.io/phylolinguistique/)
library(tidyverse)
library(phangorn)
library(ggtree)
library(tanggle)
library(TreeTools)
library(ggthemes)

#1. Préparation des données
  #1.1. Import
  url <- "https://raw.githubusercontent.com/yuanyang11510/Dissertation-Master-Codes/main/Without_borrowings(3214).tsv"
  download.file(url, "Data/Without_borrowings(3214).tsv")
  lx_orig <- read_tsv("Data/Without_borrowings(3214).tsv", comment = "#")
  lx <- lx_orig %>%
  select(CONCEPT_ID, DOCULECT, COGID) %>% 
  distinct()
    
  # 1.2. Conversion
  # 1.2.1. Etats multiples
  lx_multi <- lx %>%
    group_by(CONCEPT_ID) %>%
    mutate(COGID = as.factor(COGID) %>% as.numeric()) %>%
    group_by(DOCULECT, CONCEPT_ID) %>%
    summarise(COGID = paste0(COGID, collapse = "")) %>%
    ungroup() %>%
    mutate(COGID = ifelse(str_detect(COGID, "..+"), paste0("{", COGID, "}"), COGID)) %>%
    pivot_wider(
      names_from = CONCEPT_ID,
      values_from = COGID,
      values_fill = "?",
    )%>%
    arrange(DOCULECT)
  
  lx_phy_multi <- lx_multi %>%
    column_to_rownames("DOCULECT") %>%
    as.matrix() %>%
    MatrixToPhyDat()
  
  write.phyDat(lx_phy_multi, "Output/lx_phy_multi_without.nex", format = "nexus")
  
  #1.2.2. Etats binaires
  lx_bin <- lx %>%
    rowid_to_column() %>%
    pivot_wider(
      names_from = DOCULECT,
      values_from = rowid,
      values_fill = 0,
      values_fn = length
    ) %>%
    pivot_longer(cols = !(CONCEPT_ID | COGID), names_to = "DOCULECT", values_to = "VALUE") %>%
    mutate(VALUE = as.character(VALUE)) %>%
    group_by(CONCEPT_ID, DOCULECT) %>%
    mutate(VALUE = ifelse(sum(VALUE != "0") == 0, "?", VALUE)) %>%
    ungroup() %>%
    mutate(id = paste0(CONCEPT_ID, "_", COGID)) %>%
    select(DOCULECT, id, VALUE) %>%
    pivot_wider(
      names_from = id,
      values_from = VALUE
    )%>%
    arrange(DOCULECT)
  
  lx_phy_bin <- lx_bin %>%
    column_to_rownames("DOCULECT") %>%
    as.matrix() %>%
    MatrixToPhyDat()
  lx_phy_bin
  
  lx_phy_multi
  write.phyDat(lx_phy_bin, "Output/lx_phy_bin_without.nex", format = "nexus")
    
#2. Méthodes par distance
  #2.1. Calcul des distances 
  lx_phy <- ReadAsPhyDat("Output/lx_phy_multi_without.nex")
  lx_dist <- dist.hamming(lx_phy)
  
  lx_dist_m <- as.matrix(lx_dist)
  # lx_dist_m[upper.tri(lx_dist_m)] <- NA
  options(knitr.kable.NA = "")
  knitr::kable(lx_dist_m, digits = 2)
  
  lx_sim_m <- (1 - as.matrix(lx_dist)) * 100
  # lx_sim_m[upper.tri(lx_sim_m)] <- NA
  options(knitr.kable.NA = "")
  knitr::kable(lx_sim_m, digits = 2)
    
  #2.2. UPGMA
  lx_upgma <- upgma(lx_dist)
  lx_upgma
  
  write.tree(lx_upgma, "Output/lx_upgma_without.tree")
  plot(lx_upgma)
  
  upgma_tree <- ggtree(lx_upgma) +
    geom_tiplab() +
    xlim_tree(.2) +
    theme_tree()
  upgma_tree
  
  #2.3. Neighbour-joining
  lx_nj <- NJ(lx_dist)
  lx_nj
  
  plot(lx_nj, "unrooted")
  nj_tree <- ggtree(lx_nj, layout = "daylight") +
    geom_tiplab2() +
    xlim(-.25, .3) +
    ylim(-.2, .35) +
    theme_tree()
  nj_tree
  
  # plot(lx_nj, "tidy")
  # nj_tree <- ggtree(lx_nj) +
  #   geom_tiplab () +
  #   xlim_tree(.4) +
  #   theme_tree()
  # nj_tree
  
  #2.4. neighborNet
  lx_nn <- neighborNet(lx_dist)
  lx_nn
  plot(lx_nn)
  nn_nx <- ggsplitnet(lx_nn) +
    geom_tiplab2() +
    xlim(-.4, .2) +
    ylim(-.16, .1) +
    theme_tree()
  nn_nx
    
#3. Méthodes de maximum de parcimonie
  #3.1. Parcimonie générale (branch and bound)
  lx_phy <- ReadAsPhyDat("Output/lx_phy_multi_without.nex")
  lx_bab <- bab(lx_phy)
  lx_bab
  
  lx_bab <- acctran(lx_bab, lx_phy)
  write.tree(lx_bab, "Output/lx_bab_without.nwk")
  
  ggtree(lx_bab[[1]], layout = "equal_angle") +
    geom_tiplab2() +
    xlim(-180, 200) + ylim(-150, 150) +
    theme_tree()  

  #3.2. Parcimonie ratchet
  lx_mp_r <- pratchet(lx_phy)
                      #, trace = 0, minit = 1000, k = 100, method = "sankoff", all = TRUE)
  lx_mp_r
  
  plot(lx_mp_r, "unrooted")
  ggtree(lx_mp_r, layout = "equal_angle") +
    geom_tiplab2() +
    xlim(-30, 30) +
    ylim(-20, 20) +
    theme_tree()
  
  lx_mp_bl <- acctran(lx_mp_r, lx_phy)
  lx_mp_bl
  plot(lx_mp_bl, "unrooted")
  ggtree(lx_mp_bl, layout = "equal_angle") +
    geom_tiplab2() +
    xlim(-150, 80) +
    ylim(-100, 50) +
    theme_tree()
  
  # lx_mp_mid = midpoint(lx_mp_bl)
  # lx_mp_mid
  # plot(lx_mp_mid)
  # ggtree(lx_mp_mid) +
  #   geom_tiplab() +
  #   xlim_tree(100) +
  #   # ylim(-100, 70) +
  #   theme_tree()
  
  lx_mp_out <- RootTree(lx_mp_r, "Xiamen") %>%
    acctran(lx_phy)
  lx_mp_out
  plot(lx_mp_out)
  ggtree(lx_mp_out) +
    geom_tiplab() +
    xlim(NA, 160) +
    ylim(NA, 20) +
    theme_tree()
  
  write.tree(lx_mp_r, "Output/lx_mp_r_without.tree")
  write_rds(lx_mp_r, "Output/lx_mp_r_without.rds")
  write.tree(lx_mp_out, "Output/lx_mp_out_without.tree")
  write_rds(lx_mp_out, "Output/lx_mp_out_without.rds")
  
  #3.3. Mesures d'homoplasie et de cohérence
  #3.3.1. Consistency index (CI), indice de cohérence
  m <- phangorn:::lowerBound(lx_phy)[attr(lx_phy, "index")]
  s <- sankoff(lx_mp_r, lx_phy, site = "site")[attr(lx_phy, "index")]
  h <- s - m
  h
  H <- sum(h)
  H
  which(h > 0)
  sankoff(lx_mp_r, lx_phy)
  sum(s)

  ci <- CI(lx_mp_r, lx_phy, sitewise = TRUE)
  ci
  CI(lx_mp_r, lx_phy)
  sum(m)/sum(s)
  
  #3.3.2. Rescaled consistency index (RCI), indice de cohérence à l'échelle
  g <- phangorn:::upperBound(lx_phy)[attr(lx_phy, "index")]
  g
  rci <- RI(lx_mp_r, lx_phy, sitewise = TRUE) * CI(lx_mp_r, lx_phy, sitewise = TRUE)
  rci
  CI(lx_mp_r, lx_phy) * RI(lx_mp_r, lx_phy)

  d <- h/(g - m)
  d
  D <- sum(h)/(sum(g) - sum(m))
  D

  ri <- RI(lx_mp_r, lx_phy, sitewise = TRUE)
  ri
  RI <- RI(lx_mp_r, lx_phy)
  RI
  1 - D

  #3.3.3.比较UPGMA和MP(Ratchet)两棵树的S/H/CI/RCI/RI/D
  lx_upgma <- read.tree("Output/lx_upgma_without.tree")
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
  write_tsv(comp_tb, "Output/comp_tb_without.tsv")
    
#4. Evaluation
  #4.1. Evaluation de la stabilité des clades
  #4.1.1.以2.2.中通过UPGMA得到的谱系树为例，运用bootstrap（自助法）来测试每棵谱系树的每条分支的稳定性
  lx_phy <- ReadAsPhyDat("Output/lx_phy_multi_without.nex")
  lx_upgma <- read.tree("Output/lx_upgma_without.tree")
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
  lx_mp_out <- read_rds("Output/lx_mp_out_without.rds")
  plotBS(lx_mp_out)
  plotBS(lx_mp_out, p = .7)
  
  #4.2. Résumer l'accord entre des résultats (consensus tree)
  #以3.1.中通过MP(Branch and band)得到的一系列谱系树为例，生成一致树
  lx_bab_consensus <- consensus(lx_bab, p = 1)
  ggtree(lx_bab_consensus, layout = "daylight") +
    geom_tiplab2() +
    xlim(-10, 10) + ylim(-10, 10) +
    theme_tree()
  
  lx_bab_consensus_mj <- consensus(lx_bab, p = .5)
  ggtree(lx_bab_consensus_mj, layout = "daylight") +
    geom_tiplab2() +
    xlim(-8, 15) + ylim(-15, 10) +
    theme_tree()
  

    