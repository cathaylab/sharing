setwd("C:/Users/hung/Documents/r")
library(compositions)

## 單一筆 data 的 z-order 值
ZorderEachdata <- function(data, bin_len = 3) {
  data_len <-  ncol(data)
  zbin <-  rep(0, data_len * bin_len)
  
  ## integer to binary
  for (i in 1:data_len) {
    bin <-  strsplit(sprintf(paste("%0", bin_len, "d", sep = ""), as.integer(binary(data[, i]))), "")[[1]]
    for (j in 1:bin_len) {
      zbin[i + j * data_len] <- as.integer(bin[j]) 
    }
  }
  
  ## binary to integer
  zvalue <- sum(2 ^ (length(zbin) - which(zbin == 1)))
  
  return(zvalue)
}


## 一個 dataset 中，每一筆資料的 z-order 值
ZorderDataset <- function(data) {
  ## normalization
  data_scale <- scale(data)
  
  ## convert -4 ~ 3 to 0 ~ 7
  data_scale[which(data_scale < -3)] <- -4
  data_scale[which(data_scale >= 3)] <- 3
  data_scale <- as.data.frame(floor(data_scale) + 4)
  
  z <- data.frame(zorder = rep(NA, nrow(data_scale)))
  for (i in 1:nrow(data_scale)) {
    z[i, 1] <- ZorderEachdata(data_scale[i, ])
  }
  
  return(z)
}


## 依 z-order 值進行抽樣
ZorderSampling <- function(data, zorder, cluster_num) {
  names(zorder) <- "zorder"
  
  ## data sorted by z-order value
  data_sort <- data[order(zorder$zorder), ]
  
  ## cluster_list will save sampling data
  cluster_list <- list()
  for (i in 1:cluster_num) {
    cluster_list[[i]] <-  data.frame()
  }
  
  data_len = 1:nrow(data)
  for (i in 1:cluster_num) {
    data_seq <- which(data_len %% cluster_num + 1 == i)
    cluster_list[[i %% cluster_num + 1]] <- data_sort[data_seq, ]
  }
  
  return(cluster_list)
}


ZorderPlot <- function(data1, data2) {
  col <- names(data1)
  
  png("output/output.png", units = "px", width = 1536, height = 1536)
  
  par(mfrow = c(2, ceiling(length(col) / 2)), mar = c(5, 4.8, 4, 2))
  
  for (i in 1:length(col)) {
    col_name = col[i]
    
    ulim <- max(cbind(data1[, col_name], data2[, col_name]))
    llim <- min(cbind(data1[, col_name], data2[, col_name]))
    
    ks <- ks.test(data1[, col_name], data2[, col_name])$p.value
    
    plot(ecdf(data1[, col_name]),
         verticals = TRUE, do.points = FALSE,
         xlim = c(llim, ulim),
         main = paste("p-value of k-s test : ", round(ks, 4), sep = ""),
         xlab = col_name, ylab = "Cumulative Distribution Function",
         lwd = 2.5, col = "royalblue3",
         cex.main = 2, cex.lab = 1.5, cex.axis = 1.5)
    
    par(new = TRUE)
    
    plot(ecdf(data2[, col_name]),
         verticals = TRUE, do.points = FALSE,
         xlim = c(llim, ulim),
         xaxt = "n", yaxt = "n",
         main = "", xlab = "", ylab = "",
         lwd = 2.5, col = "mediumvioletred",
         cex.lab = 1.5, cex.axis = 1.5)
  }
  
  dev.off()
}


## 以 iris data 實作
x <- iris[, 1:4]
y <- iris[, 5]

zorder <- ZorderDataset(x)
zsampling <- ZorderSampling(x, zorder, 2)
iris1 = zsampling[[1]]
iris2 = zsampling[[2]]
ZorderPlot(iris1, iris2)


set.seed(33250)
random_sample <- sample(seq(1, nrow(iris), 1), size = floor(nrow(iris) / 2), replace = FALSE)
iris.s1 <- iris[random_sample, 1:4]
iris.s2 <- iris[setdiff(seq(1, nrow(iris), 1), random_sample), 1:4]
ZorderPlot(iris.s1, iris.s2)



## 以 Teradata 實作
library(RODBC)
library(dplyr)
library(data.table)
conn <- odbcConnect("TERDATA_DB", uid = "nt49178", pwd = "WWWhelp0@")
data <- sqlQuery(conn, paste("select * from bacc_temp.nt19441_adj_apt201512"))
# CCD_CLA_CLM_001	信用卡總額度
# CUS_RWB_RWB_008	首個銀行帳戶帳齡
# CCD_CLA_CLU_001	當月額度使用率
# CUS_CHU_CHU_063	存款最近一年使用ATM次數(帳務性)
# ULN_CLA_USG_002	當月全體金融機構循環信用佔額度比率
# Y1_ALL_TXN_AMT	近一年行內外總簽帳金額
# WM_VIP_AVG_AMT	近三個月平均AUM
# AGE	年齡
# NET_PROFIT	近一年淨收益

x <- filter(data, !is.na(CCD_CLA_CLM_001) & !is.na(CUS_RWB_RWB_008) & !is.na(CCD_CLA_CLU_001) &
              !is.na(CUS_CHU_CHU_063) & !is.na(ULN_CLA_USG_002) & !is.na(Y1_ALL_TXN_AMT) &
              !is.na(WM_VIP_AVG_AMT) & !is.na(AGE) & !is.na(NET_PROFIT)) %>% 
  select(CCD_CLA_CLM_001, CUS_RWB_RWB_008, CCD_CLA_CLU_001, CUS_CHU_CHU_063,
         ULN_CLA_USG_002, Y1_ALL_TXN_AMT, WM_VIP_AVG_AMT, AGE, NET_PROFIT)

x <- fread("data/abt_data.txt", header = TRUE, data.table = FALSE)

Sys.time()
zorder <- ZorderDataset(x)
Sys.time()
zsampling <- ZorderSampling(x, zorder, 2)
Sys.time()

td1 <- zsampling[[1]]
td2 <- zsampling[[2]]
ZorderPlot(td1, td2)

set.seed(810844)
random_sample <- sample(seq(1, nrow(x), 1), size = floor(nrow(x) / 2), replace = FALSE)
td1 <- x[random_sample, ]
td2 <- x[setdiff(seq(1, nrow(x), 1), random_sample), ]
ZorderPlot(td1, td2)

