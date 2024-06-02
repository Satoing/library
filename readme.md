# UESTC 图书馆研修室预约

> 每天6点半抢图书馆研修室。

自行配置selenium环境。main.py中需要填写的信息：

```python
uname = '' # 统一身份登录
pword = ''

# room1和room2是最想要的两个，如果已经被约了就依次执行wants
room1 = 'A-S320'
room2 = 'A-S321'
wants = ['A-S321', 'A-S320', 'A-S324', 'A-S325', 'A-S341', 'A-S342', 'A-S343', 'A-S344']
start = '800'
end = '2130' #图书馆改版后最多只能约4个小时，算一下起始时间
```