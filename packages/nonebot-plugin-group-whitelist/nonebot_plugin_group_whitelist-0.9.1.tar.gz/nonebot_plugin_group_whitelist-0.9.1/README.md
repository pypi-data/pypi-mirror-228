## nonebot_plugin_group_whitelist
适用于 [Nonebot2](https://github.com/nonebot/nonebot2) 的群聊白名单插件


### 安装
- 使用 nb-cli
```
nb plugin install nonebot_plugin_group_whitelist
```
 - 使用pip
```
pip install nonebot_plugin_group_whitelist
```

### 使用
以下命令需要配置命令前缀与命令分隔符，默认为”/“和”.“<br>
可以参考[命令前缀](https://nb2.baka.icu/docs/next/appendices/config#command-start-%E5%92%8C-command-separator)
自行配置
```
/whitelist.add <群号> 添加白名单
/whitelist.remove <移除白名单> 添加白名单
/whitelist.lookup 列出白名单
```