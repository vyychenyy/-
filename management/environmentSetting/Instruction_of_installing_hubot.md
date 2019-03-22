# 本地运行Hubot

### 安装Hubot
Hubot是基于node.js技术体系，使用CoffeeScript语言开发的开源chatbot。
要安装Hubot，需要先上node.js官网下载js，我们使用的版本是v11.12.0。
安装好node.js后，npm也会自动安装上，我们要使用npm来安装Hubot生成器。

`npm install -g yo generator-hubot`

之后可以再任意的文件夹生成自己的Hubot，只要输入`yo hubot`即可。
生成时要注意，为了之后能够连接Slack，需要在adapter一栏打上slack，这样Hubot就安装完毕了。

### 启动并调试Hubot
在命令行输入下面的指令，就可以执行Hubot了

`bin\hubot.cmd`

注意这是windows环境下，如果是linux，使用普通的斜杠即可。当你看到  

```
yourHubotName> 
```

这就表示你成功执行你的Hubot了，这里yourHubotName是在生成Hubot时给它取的名字。
Hubot有一些它自带的基础命令，比如输入yourHubotName ping，它会回你pong

```
yourHubotName> youHubotName ping
yourHubotName> PONG
```

### 开发自定义机器人脚本
Hubot的项目结构
- bin/ Hubot运行脚本
- node_modules/ 引用的包文件
- scripts/ 存放自定义脚本
- external-scripts.json 引用的外部脚本
- package.json 项目全局配置信息

我们的自定义脚本既可以使用CoffeeScript，也可以使用纯JavaScript来编写。
详细的说明可参考以下链接  
[https://hubot.github.com/docs/scripting/][1]

# 连接Hubot和Slack
要连接Hubot和Slack，首先要把Slack的adapter集成进来，输入以下命令

`npm install hubot-slack --save`

然后每次连接前，都需要把Hubot的API Token设好

`set HUBOT_SLACK_TOKEN=xoxb-576609764288-580486290854-Pv8ovA0LcIZwTzlqNXXHVe6v`

Slack的Hubot API Token是不变的，所以每次都输入这个命令即可。

启动Hubot时，要声明使用的adaper是Slack

`bin\hubot.cmd -a slack`

这样启动后，就已经连接上Hubot了，之后可以在Slack跟我们的Hubot聊天啦

[1]: https://hubot.github.com/docs/scripting/
