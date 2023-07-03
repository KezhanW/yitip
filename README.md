# daily_reminder
给女朋友做的微信天气推送

教程链接

https://www.coolapk.com/feed/38579891?shareKey=NGI3ZGZlZTM4MDBjNjMwMzdlM2M~&shareUid=3198334&shareFrom=com.coolapk.app_4.10



网址1   http://mp.weixin.qq.com/debug/cgi-bin/sandboxinfo?action=showinfo&t=sandbox/index
网址2   https://id.qweather.com/


模板内容如下：

```
{{greetings.DATA}}
{{date.DATA}} 
今天是我们恋爱的第{{love_day.DATA}}天
你的城市：{{region.DATA}} 
今天天气：白天 : {{textDay.DATA}}   夜间 : {{textNight.DATA}} 
今天气温：{{temp.DATA}} 
贵人星座：{{NobleConstellation.DATA}}
爱情指数：{{loveIndex.DATA}}  工作指数：{{workIndex.DATA}}
今天的你：{{overviewToday.DATA}}
土味情话：{{saylove.DATA}}
毒鸡汤：{{ChickenSoup.DATA}}
```

模板内容如下：

{{date.DATA}} 

地区：{{region.DATA}} 

天气：{{weather.DATA}} 

气温：{{temp.DATA}} 

风向：{{wind_dir.DATA}} 

今天是我们恋爱的第{{love_day.DATA}}天 

{{birthday1.DATA}} 
{{birthday2.DATA}}

{{note_en.DATA}} 
{{note_ch.DATA}}


天气key生成教程
![image](https://raw.githubusercontent.com/limoest/daily_reminder/main/%E5%92%8C%E9%A3%8E%E5%A4%A9%E6%B0%94key%E7%94%9F%E6%88%90.png)


可以去天行数据申请各种各样的接口用来推送  
![image](https://raw.githubusercontent.com/limoest/daily_reminder/main/others/Snipaste_2022-08-24_12-13-19.png)
![image](https://raw.githubusercontent.com/limoest/daily_reminder/main/others/Snipaste.png)



有别的建议欢迎留言
