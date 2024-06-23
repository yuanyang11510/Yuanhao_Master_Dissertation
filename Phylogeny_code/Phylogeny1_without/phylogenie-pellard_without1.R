library(tidyverse)
library(phangorn)
library(ggtree)
library(tanggle)
library(TreeTools)

#1. Préparation des données
  #1.1. Import
    # url <- "https://raw.githubusercontent.com/yuanyang11510/Dissertation-Master-Codes/main/Without_borrowings(3214).tsv"
    # download.file(url, "BAI.tsv")
    # lx <- read_tsv("BAI.tsv", comment = "#") %>%
    lx = read_tsv ("Data/Without borrowings(3214).tsv", comment = "#") 

  #1.2. Conversion
    lx_m = lx %>%
      select(CONCEPT_ID, DOCULECT, COGID) %>%
      distinct() %>%
      pivot_wider(
        names_from = DOCULECT,
        values_from = CONCEPT_ID,
        values_fill = 0,
        values_fn = length
      ) %>%
      select(-COGID)

#A faire: Traitement des données marquantes    
        
    lx_phy <- phyDat(lx_m,
                     type = "USER",
                     levels = c(0, 1),
                     names = names(lx_m)
    )
    lx_phy
    
    write.phyDat(lx_phy, "Output/lx_phy_without.txt")
    
#2. Méthodes par distance
  #2.1. Calcul des distances  
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
    write.tree(lx_upgma, "Output/lx_upgma_without.nwk")
    plot(lx_upgma)
    
    upgma_tree <- ggtree(lx_upgma) +
      geom_tiplab() +
      xlim_tree(0.22) +
      theme_tree()
    upgma_tree
    
  #2.3. Neighbour-joining
    lx_nj <- NJ(lx_dist)
    lx_nj
    plot(lx_nj, "unrooted")
    plot(lx_nj, "tidy")
    
    nj_tree <- ggtree(lx_nj, layout = "daylight") +
      geom_tiplab2() +
      xlim(-.15, .25) +
      ylim(-.15, .25) +
      theme_tree()
    nj_tree

  #2.4. neighborNet
    lx_nn <- neighborNet(lx_dist)
    lx_nn
    plot(lx_nn)
    
    nn_nx <- ggsplitnet(lx_nn) +
      geom_tiplab2() +
      xlim(-.25, .15) +
      ylim(-.3, .2) +
      theme_tree()
    nn_nx

#3. Méthodes de parcimonie
  #3.1. Parcimonie générale (branch and bound)
    lx_bab <- bab(lx_phy)
    lx_bab
    
    lx_bab <- acctran(lx_bab, lx_phy)
    write.tree(lx_bab, "Output/lx_bab_without.nwk")
    
    ggtree(lx_bab[[1]], layout = "equal_angle") +
      geom_tiplab2() +
      xlim(-180, 200) + ylim(-150, 150) +
      theme_tree()
    
    ggtree(lx_bab[[2]], layout = "equal_angle") +
      geom_tiplab2() +
      xlim(-180, 200) + ylim(-150, 150) +
      theme_tree()
    
    ggtree(lx_bab[[3]], layout = "equal_angle") +
      geom_tiplab2() +
      xlim(-180, 200) + ylim(-150, 150) +
      theme_tree()
    
    ggtree(lx_bab[[4]], layout = "equal_angle") +
      geom_tiplab2() +
      xlim(-180, 200) + ylim(-150, 150) +
      theme_tree()

    #lx_bab[5-25]略
    
  #3.2. Parcimonie ratchet
    lx_pratchet <- pratchet(lx_phy)
    lx_pratchet <- acctran(lx_pratchet, lx_phy)
    lx_pratchet
    
    ggtree(lx_pratchet, layout = "equal_angle") +
      geom_tiplab2() +
      xlim(-150, 150) + ylim(-150, 250) +
      theme_tree()
    
#4. Evaluation
  #4.1. Evaluation de la robustesse (UPGMA, bootstrap)
  #此处是以2.2.中通过UPGMA得到的谱系树为例，运用bootstrap（自助法）来测试每棵谱系树的每条分支的稳定性
    lx_m <- PhyDatToMatrix(lx_phy)
    boot_upgma_hamming <- function(x) {
      upgma(dist.hamming(phyDat(x, type = "USER", levels = c(0, 1))))
    }
    n_bs <- 1000
    
    set.seed(123456)
    lx_upgma_bs <- boot.phylo(lx_upgma,
                              lx_m,
                              boot_upgma_hamming,
                              B = n_bs,
                              trees = TRUE,
                              quiet = TRUE)
    
    upgma_bs_scores <- prop.clades(lx_upgma, lx_upgma_bs$trees, rooted = TRUE)
    upgma_support <- c(rep(n_bs, length(lx_phy)), upgma_bs_scores)
    upgma_support_pct <- upgma_support / n_bs
  
    ggtree(lx_upgma) +
      geom_tiplab() +
      geom_nodelab(aes(label = upgma_support_pct), geom = "text", hjust = -.1) +
      xlim_tree(0.2) +
      theme_tree()

    upgma_support_pct[upgma_support_pct < .7] <- NA
    
    ggtree(lx_upgma) +
      geom_tiplab() +
      geom_nodelab(aes(label = upgma_support_pct), geom = "text", hjust = -.1) +
      xlim_tree(0.2) +
      theme_tree()

    #4.2. Résumer l'accord entre des résultats
    lx_bab_consensus <- consensus(lx_bab, p = 1)
    ggtree(lx_bab_consensus, layout = "equal_angle") +
      geom_tiplab2() +
      xlim(-10, 10) + ylim(-10, 10) +
      theme_tree()
    
    lx_bab_consensus_mj <- consensus(lx_bab, p = .5)
    ggtree(lx_bab_consensus_mj, layout = "equal_angle") +
      geom_tiplab2() +
      xlim(-10, 10) + ylim(-10, 10) +
      theme_tree()

    