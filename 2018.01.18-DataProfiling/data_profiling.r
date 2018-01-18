setwd("C:/Users/hung/Downloads/kaggle")

library(data.table)
library(dplyr)
library(ggplot2)

# load data
members <- fread("members.csv", header = TRUE, data.table = FALSE)
sampsub <- fread("sample_submission.csv", header = TRUE)
songetr <- fread("song_extra_info.csv", header = TRUE, encoding = "UTF-8")
songs <- fread("songs.csv", header = TRUE, encoding = "UTF-8")
train <- fread("train.csv", header = TRUE)
test <- fread("test.csv", header = TRUE)

colnames(train)[1] <- c("user_id")
colnames(members)[c(1, 3, 6)] <- c("user_id", "age", "registration_date")

# ggplot setting
readable_labs <- theme(axis.text = element_text(size = 12),
                       axis.title = element_text(size = 14),
                       plot.title = element_text(hjust = 0.5))

# 資料筆數檢視
dim(members)

# 主鍵唯一性分析
pk <- group_by(train, user_id, song_id) %>% 
        summarise(cnt = n()) %>% 
        filter(cnt > 1)
pk

# 欄位型態轉換
str(members)
members <- transform(members,
                     city = as.character(city),
                     registered_via = as.character(registered_via),
                     registration_date = as.Date(as.character(registration_date), format = "%Y%m%d"), 
                     expiration_date = as.Date(as.character(expiration_date), format = "%Y%m%d"))

# 值域分析
summary(members$age)

# 異常值偵測
length(members[which(members$age == 0), "age"])
summary(members[which(members$age > 0 & members$age <= 100), "age"])

# 類別分析
group_by(members, city) %>% 
  summarise(cnt = n())

# 資料分布
tmp_age <- group_by(members, age) %>% 
             summarise(cnt = n()) %>% 
             arrange(desc(cnt))

tmp_age %>% ggplot(aes_string("age", "cnt")) + 
              geom_col(fill = "goldenrod2") + 
              labs(x = "Age", y = "Frequency") +
              xlim(0, 100) +
              ylim(0, 1000) +
              readable_labs


tmp_city <- group_by(members, city) %>% 
              summarise(cnt = n()) %>% 
              arrange(desc(cnt))

tmp_city %>% ggplot(aes_string("city", "cnt")) + 
               geom_col(fill = "goldenrod2") + 
               labs(x = "City", y = "Frequency") +
               xlim(0, 25) +
               ylim(0, 20000) +
               readable_labs

# 相關性分析
tmp_tab <- group_by(train, source_system_tab) %>% 
             summarize(cnt = n(),
                       avg = mean(target)) %>% 
             arrange(desc(avg)) 
  
tmp_tab %>% ggplot(aes_string("source_system_tab",
                              "avg")) + 
              geom_col(aes(fill = cnt)) +
              scale_fill_gradient(low = "turquoise",
                                  high = "violet") +
              coord_flip() +
              labs(x = "", y = "mean_target") +
              readable_labs


tmp_song <-  group_by(train, song_id) %>% 
               summarize(occurence = n(),
                         mean_target = mean(target)) %>% 
               group_by(occurence) %>% 
               summarize(no_of_items = n(),
                         avg_target = mean(mean_target)) %>% 
               arrange(desc(avg_target))

tmp_song %>% ggplot(aes(occurence, avg_target)) +
               geom_line(color = "turquoise") +
               geom_smooth(color = "turquoise") +
               labs(x = "Song Occurence", y = "Target") + 
               readable_labs
