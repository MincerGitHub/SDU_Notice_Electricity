# 第一个把coroutine添加为task的方法：await
# asyncio.run()把main()包装成了第一个task加入到了event loop中
#
# 用async def定义的函数被调用后返回一个corouine而不是自身return的返回值
#
# 当你await一个coroutine的时候：
# 本质就只是调用了一个生成器，对协程没有帮助
#
#
# 当你await一个task时：
# 告诉event loop我这个task要完成，我把控制权交还给event loop；
# 并且在控制权回来时从这个task里提取所需要的返回值
# 会yield出去（告诉event loop我这个task现在干不了了在等待中，应该让别人占资源去）
# 当event loop再次安排他运行时，他会返回这个coroutine里面真正的返回值，拿出来保存起来
# （但没有‘x = await get_txt(url)’的x=的话就不会再return了）
#
#
# 而当你await一个future（gather()的返回值类型）时：
# （若future里装的是coroutines，首先一并包装成很多task）；告诉event loop这个future里的tasks都要完成，并把控制权交还给event loop
#
#
#
#
#
# await coroutine --> 像调用生成器一样调用coroutine，等待直到拿到范围值（可能为空），不交还控制权，导致并不能实现异步
# await task --> 阻塞程序，并将控制权交还event_loop
# create_task --> 提供了一种将单个coroutine包装成task的方法，注册到event_loop，不交还控制权
# gather 【coroutine】 --> 提供了一种将多个coroutint包装成task并注册到event_loop的方法，’应该‘是要交还控制权用来执行【coroutine】包装成的【task】
# gather 【task】--> 将多个task进行await（注册到event_loop并等待），阻塞直到所有task完成，’应该‘是要交还控制权用来执行【task】





import asyncio


async def get_txt(url):
    await asyncio.sleep(1)
    return len(url)


async def main():
    task1 = asyncio.create_task(get_txt('https://www.baidu.com'))
    task2 = asyncio.create_task(get_txt('https://www.sogou.com'))

    ret1 = await task1
    ret2 = await task2

    print(ret1)
    print(ret2)


asyncio.run(main())