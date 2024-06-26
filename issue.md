很多同学在使用中因为没有仔细看教程，所以会出现各种问题。



这里列出一些常见的问题，大家可以参考参考。



## 1. IndexError: list index out of range



![image-20240626104118017](https://flydean-1301049335.cos.ap-guangzhou.myqcloud.com/img/202406261041060.png)

这里的原因很可能是阿里云语音合成极速版没有开通商业版本， 点击升级为商用版本即可。

![image-20240626104231191](https://flydean-1301049335.cos.ap-guangzhou.myqcloud.com/img/202406261042860.png)



![image-20240626104158441](https://flydean-1301049335.cos.ap-guangzhou.myqcloud.com/img/202406261042930.png)


## 2. No such filter

在ffmpeg合成视频的时候出现下面错误：

```
[AVFilterGraph @ 000001f7486a8b40] No such filter: ''
Error initializing complex filters.
Invalid argument
```

查看你的ffmpeg版本，需要升级到6.0以上。

