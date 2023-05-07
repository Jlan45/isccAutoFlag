# isccAutoFlag
没什么，就是想做个自动提交flag的东西
## 食用教程

1、先去下载cqhttp并自行配置，接受和发送消息的地方改成这样

```
  - http: # HTTP 通信设置
      host: 0.0.0.0 # 服务端监听地址
      port: 5700      # 服务端监听端口
      timeout: 5      # 反向 HTTP 超时时间, 单位秒，<5 时将被忽略
      long-polling:   # 长轮询拓展
        enabled: false       # 是否开启
        max-queue-size: 2000 # 消息队列大小，0 表示不限制队列大小，谨慎使用
      middlewares:
        <<: *default # 引用默认中间件
      post:           # 反向HTTP POST地址列表
      #- url: ''                # 地址
      #  secret: ''             # 密钥
	  #  max-retries: 3         # 最大重试，0 时禁用
      #  retries-interval: 1500 # 重试时间，单位毫秒，0 时立即
      - url: http://127.0.0.1:5701/ # 地址
        secret: ''                  # 密钥
        max-retries: 0             # 最大重试，0 时禁用
      #  retries-interval: 1000      # 重试时间，单位毫秒，0 时立即

```

2、运行main.py，缺依赖的话自己装

3、会自动接受类似于

```
题目名 ISCC{xxxx}
```
如果有疑似flag的字符串会自动私聊发送主账号并给出群聊号和发送人号

并找到对应的题目进行提交，会提醒config.py中的QQ对应题目的提交成功情况

随意二开，仅供分享，不承担使用者任何使用后果
