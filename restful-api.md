[TOC]



# 异常检测

## k-means算法

##### 检测参数
```
 net bytes_recv , net bytes_sent
```
##### slack command 
```
 dog km yyyy-mm-dd HH:MM:SS
```
##### request

```
http://172.20.10.2:8089/km/<float:test_time>
```

##### response
```
检测出的异常点个数，异常点时间，以及图形名称
```


## 孤立森林算法

##### 检测参数
```
net bytes_recv , net bytes_sent
```

##### slack command

```
dog if yyyy-mm-dd HH:MM:SS
```


##### request
```

http://172.20.10.2:8089/forest/<float:test_time>
```
##### response
```
检测出的异常点个数，异常点时间，以及图形名称
```


# 图形化

##### slack command
```
dog photo yyyy-mm-dd HH:MM:SS
```
##### request
```
http://172.20.10.2:8089/image/<float:test_time>
```
##### response
```
有关cpu‘usage_idle’的图片
```
# 数据信息

##### slack command
```
dog cpu
```
##### request
```
http://172.20.10.2:8089/cpu
```
##### response
```
有关cpu的数据信息
```

