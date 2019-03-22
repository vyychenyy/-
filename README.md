# README
---
# 环境依赖
node.js v11.12.0

---
# 目录结构
|-- frontend
|-- backend
|-- management

之后应该会在一级目录添上数据库，所以之后不要把数据库加进backend

---
# Kanban
### Project
- 现在暂时分了Front-end，Back-end和Management
- 因为现在全部用的默认看板，所以只有To do，In progress和Done，注意每次In progess的issue最多三件，如果完成有困难的话，在issue添加help wanted标签，然后找团队里其他成员一起解决
- issue在done后应该把issue状态改成close
- 大家一起检查过done状态的issue，确认无误后可以把issue从project delete掉，否则应该reopen

### Issue
- 在issue栏目点击new issue可以创建新issue
- 需要在issue的题目说明ddl，在右边选择labels、projects和milestones，之后该issue会自动加入对应project的To do

### Label说明
- negotiation	全体工作
- management	文档管理以及项目管理工作
- help wanted	需要帮助
- frontend		前端工作（用户与hubot交互）
- backend		后端工作（云平台数据分析）
