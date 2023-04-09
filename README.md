# API [Demo](https://www.betit.online/)

# MySQL entity-relationship diagram
![](/app/image/SQLChart.png "Magic Gardens")

# Redis Cloud key value structure

|      Key                |     Value               |    Value               |
|:-----------------------:|:-----------------------:|:----------------------:|
| realtime:dashboard      |        JSON{...}        |realtime data for [dashboard](https://bet-it-frontend.vercel.app/dashboard)  |
| realtime:crypto         |        JSON{...}        |realtime data for [crypto](https://bet-it-frontend.vercel.app/crypto)        |
| realtime:crypto_symbol  |        JSON{...}        | data for crypto symbol                       |
| realtime:crypto_top7    |        JSON{...}        |realtime data for [top7 search on Coingeko](https://bet-it-frontend.vercel.app/crypto)|
| realtime:TW_realtime    |        JSON{...}        |realtime data for [TW Stock](https://bet-it-frontend.vercel.app/twStock)                         |
| realtime:US_daily       |        JSON{...}        |realtime data for [US Stock](https://bet-it-frontend.vercel.app/usStock)                        |