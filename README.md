# ZanORobot
将自己的赞噢校园集市帖子回复接入GPT（伪记忆性对话）
# Requirements
> openai
> 
> requests
# Usage
要先有一个API KEY，推荐**V3小店的转发api**[(无人头)](https://api.v3.cm/)....[(有人头)](https://api.v3.cm/register?aff=Nmpy)

抓cookie：

推荐**Fidder**

cookie的结构（值已经做了混淆）：
> 'user_token': 'ckddWc1padVVZbFJOaXptRlo0T2WxnOU9HbW1UbUlSJqb0U9'
> 
> 'Hm_lvt_44d055a19f3943caa808501f424e662e': '1791732053,1221732325,1921732454,1021812878'
> 
> 'HMACCOUNT': '1AB4385D280CC087'
> 
> 'Hm_lpvt_44d055a19f3943caa808501f424e662e': '1921732454'
> 
> 'SERVERID': 'e90691305575d026b90b6e62872e5858|1921732454|1921732454'

- **user_token**是网站给你的，测试下来，user_token虽然每次登录都是新的，但是旧的不会随着过期。
- **Hm_lvt_xxx** 和 **Hm_lpvt_xxx**这两个是百度广告联盟的cookie，xxx为百分广告联盟给分配的id，固定不变。
- **HMACCOUNT** 也是百度广告联盟分配的，固定不变。
- **SERVERID** 不确定是谁的，可能是网站的。
- --------分割线--------
- **Hm_lpvt_44d055a19f3943caa808501f424e662e**的值为当前时间的时间戳（单位秒）。
- **Hm_lvt_44d055a19f3943caa808501f424e662e**的值为四个时间戳，其最后一个时间戳应当与**SERVERID**中最后一个时间戳相同。
上面的当做介绍吧，下面是怎么用。

抓取一次cookie后，每次发起请求时将当前的时间戳赋值给**Hm_lpvt_44d055a19f3943caa808501f424e662e**即可。

修改**Robt**中**YOUR_API_KEY**和**Spider**中**cookies**即可。

**Spider**中**get_comment_list**方法需要接收帖子的id。

**Spider**中**get_headers**方法需要修改**X-Sc-Alias**的值，应当为你的学校英文缩写，具体看抓包内容。
