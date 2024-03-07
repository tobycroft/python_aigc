# TuuzPythonWeb

TuuzPythonWeb基于Flask，四层架构，数据库基于EasyPythonOrm

框架结构参考Thinkphp，极大降低上手难度，TPW的设计理念是简单好理解，为了不写文档，

采用静态路由安全性好，性能也够用就是

输入器支持简单操作以及链式操作

# 新手用户

# 数据库ORM支持

内置

# TPW目录说明

- app
    - 这是所有的代码逻辑控制面
- common
    - 这是所有本项目里面（移植项目）里面会用到的控制面
- config
    - 设定面
- extend
    - 插件控制面
- route
    - 路由控制面
- tuuz
    - 核心Utils
        - [计算+转换器模块](https://github.com/tobycroft/Calc)
        - 待补充……

# TPW的四段路由说明

~~~
{{host}}/文件夹名称v1/下层文件夹index/下层controller中的文件名称index/文件中的方法名称index
~~~

- 我强烈推荐使用四段路由，四段路由可以将你的动作进行有效的切分
- 四段路由在Thinkphp的默认三段的基础上，加入了版本属性
- 虽然你可以使用版本控制或者注入来完成新接口的切换，但是这并不适用于复制型的项目
- 使用四段地址，可以让你从"前端"对接中解放出来，如果你愿意你可以让你的项目有多个版本共存
- 前端合作中需要使用什么功能，直接翻之前的接口文档对接即可，这是TPW选择使用四段路由的重要原因！

当然如果你相对OldSchool，你也可以将所有的Controller路由放到Onroute中

## TPW的route用法说明

- OnRoute是路由的入口，有且只有一个Onroute.py，在Onroute中，我们需要定义版本以及下级（版本）路由的入口
- v1文件夹同app文件夹中的v1，目的是将所有属于v1这个router的下的路由全部集合
- 在v1文件夹下，你可以定义多个route，请使用xxxRouter结尾，这个习惯有利于ide区别controller和router，命名不会影响功能，但是会影响日后接手人员的心情
- 编写方法可以参考示例

### TPW的route目录构建逻辑

- route
    - OnRoute.py

## TPW的app用法说明

- 写法以及构建方法可参考示例
- 这里强调下，当你写了一个controller之后，你需要将这个controller的名称写入到对应的router中方可使用
- TPW推荐使用MAC方式开发
- 传统框架只能使用MVC方式，复杂业务中数据库的单例很难实现，这是因为原版的MysqlDriver对NestedTransaction支持很差
- 本框架使用Gorose-Pro，支持NestedTransaction等操作，你可以放心大胆的使用MAC架构进行解耦！
- 如果有必要，你可以在MAC的基础上加入Util或者Logic，做成（伪）四层的形式

### TPW的app目录构建逻辑

- app
    - v1
        - index
            - action
            - controller
                - index.py
            - model
                - IndexModel.py
        - user
            - action
            - controller
                - user.py
            - model
                - UserModel.py
                - UserInfoModel.py
    - v2
        - index
            - action
            - controller
                - index.py
            - model
                - IndexModel.py
        - balance
            - action
            - controller
                - index.py
            - model
                - BalanceModel.py
    - cron
        - invest.py
        - timeinvest.py

### TPW的其他说明

接口性能：

- 在本地数据库的情况下，平均（列表x20/单条数据)，平均效率在6ms-30ms左右
- 在RDS数据库情况下，平均（列表x20/单条数据)，平均效率在1ms-10ms左右

## TPW输出说明

- 你可以使用Gin的默认输出
- Code:错误码可以与前端自定
- Data:如果传输nil，最终json中的data字段会变成"[]"
- Echo:这里只能传string

```
RET.Success(c, 0, nil, "验证成功")
RET.Fail(c, 400, nil, "验证失败")
```
