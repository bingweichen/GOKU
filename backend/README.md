#后端数据库设计模式

业务逻辑分为 route/service/database 三层结构

service 层使用 Add/Get/Modify/Remove

方法默认使用primary key进行搜索

database 层使用 Create/Read/Update/Delete


# 业务分层逻辑
object转json 放在service层


# restful api
GET 获取
PUT 新增

# 后端
- route

1. store (code, test)
2. school (code, test)
3. user （code, test)
- service
- model

## service
- store 线下商铺
- school 学校
- user 用户

- e_bike model 电动车型号
- e_bike 电动车
- appointment 预约订单



### user service
- register
- login
- add
- get
- modify
- remove
### school service
- add
- get
- modify
- remove
### store service
- add
- get
- modify
- remove
### e_bike model service
- add
- get
- modify
- remove
### e_bike service
- add
- get
- modify
- remove
### appointment service
- add
- get
- modify
- remove


## requirement
flask
peewee
PyMySQL
flask_cors
flask_jwt_extended
