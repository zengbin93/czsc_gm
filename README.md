# czsc_gm

使用掘金量化终端对缠中说禅技术分析理论进行策略研究

* 掘金文档： [https://www.myquant.cn/docs/python/39?](https://www.myquant.cn/docs/python/39?)
* 企业微信群聊机器人文档：[https://work.weixin.qq.com/api/doc/90000/90136/91770](https://work.weixin.qq.com/api/doc/90000/90136/91770)

## 运行环境说明

* python >= 3.7
* czsc == 0.6.7

## 入口文件说明

执行前，需要在 `src/conf.py` 中设置一些参数

1. `run_gm_1min.py` - 按1分钟 on_bar 执行策略

## 回测结果说明

每次启动一次回测，都会在 `data_path` 目录下创建一个对应开始时间的文件夹，会存储一些相关的文件




