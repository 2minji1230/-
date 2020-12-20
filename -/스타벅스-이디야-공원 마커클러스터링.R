library(readxl)
library(dplyr)
library(readxl)
library(leaflet)
library(leaflet.extras)
library(stringr)

setwd('D:/MyGit/Data-Analysis/스타벅스 분석')

# 데이터 불러오기
starbucks <- read_excel('(종합)Starbucks_Stores.xlsx')
ediya <- read_excel('(종합)Ediya_Stores.xlsx', sheet = 'Sheet2')
parks <- read.csv('전국도시공원정보표준데이터.csv')

# 전처리
parks <- parks %>% 
    filter(위도 > 28) %>% 
    filter(경도 < 136)


# 이름, 위경도만 추출
star_temp <- starbucks %>% select('name', 'lat', 'long', 'service', 'loc&fac')
ediya_temp <- ediya %>% select('상호명', '지점명', '경도', '위도')
parks_temp <- parks %>% select('공원명', '위도', '경도')

# 아이콘 생성
star_icon <- makeIcon(iconUrl = 'starbucks.png',
                      iconWidth = 50,
                      iconHeight = 50)

ediya_icon <- makeIcon(iconUrl = 'ediya.gif',
                       iconWidth = 50,
                       iconHeight = 50)

park_icon <- makeIcon(iconUrl = 'parks.jpg',
                      iconWidth = 50,
                      iconHeight = 50)

# 시각화
## 형변환
star_temp$lat <- as.numeric(star_temp$lat)
star_temp$long <- as.numeric(star_temp$long)
ediya_temp$경도 <- as.numeric(ediya_temp$경도)
ediya_temp$위도 <- as.numeric(ediya_temp$위도)
parks_temp$위도 <- as.numeric(parks_temp$위도)
parks_temp$경도 <- as.numeric(parks_temp$경도)

## 정보를 나타내기 위한 변수조인
star_temp$info <- str_c(star_temp$name, star_temp$service, star_temp$`loc&fac`, sep = " <br> ")

# 시각화
map <- leaflet() %>% 
    addTiles() %>% 
    addMarkers(lat = star_temp$lat, lng = star_temp$long,
               clusterOptions = markerClusterOptions(),
               popup = star_temp$info,
               icon = star_icon) %>% 
    addMarkers(lat = ediya_temp$위도, lng = ediya_temp$경도,
               clusterOptions = markerClusterOptions(),
               popup = str_c(ediya_temp$상호명, ediya_temp$지점명, sep = " "),
               icon = ediya_icon) %>% 
    addMarkers(lat = parks_temp$위도, lng = parks_temp$경도,
               clusterOptions = markerClusterOptions(),
               popup = parks_temp$공원명,
               icon = park_icon) %>% 
    addDrawToolbar(editOptions = editToolbarOptions(selectedPathOptions = 
                                                        selectedPathOptions()))
map
