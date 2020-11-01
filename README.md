# web-UI 自动化测试示例

---

## 框架设计

- pytest
- selenium
- POM 模型

---

## 目录结构

    common                 ——公共类
    Page                   ——基类
    PageElements           ——页面元素类
    PageObject             ——页面对象类
    TestCase               ——测试用例
    conf.py                ——各种固定配置
    conftest.py            ——pytest胶水文件
    pytest.ini             ——pytest配置文件

---

## 运行

- `cd 项目目录`

* MacOS 系统或 Linux 系统

- 在命令行输入`sh run_mac.sh`即可运行

* Windows 系统

- 在命令行输入`run_mac.bat`即可运行


# allure参数说明


- allure --alluredir

- allure generate
    - -c 生成报告前删除上一次生成的报告
    - -o 指定生成的报告目录
- allure open

1、pytest --collect-only    查看pytest收集到的用例
2、pytest test_case/        执行test_case目录下的测试用例
3、pytest -s -v             控制台显示详细的用例执行情况
4、pytest --alluredir=Output/allure_reports   将测试报告生成到指定的目录
5、pytest --reruns 2 --reruns-delay 5         失败的用例可以重新运行2次，第一次和第二次的间隔时间为5秒钟。
6、pytest -m mark_practice   运行打标记的用例
7、pytest --help   查看pytest中全部的标记选项

1、@pytest.mark.parametrize()   传递参数化数据

打标记：mark功能
   对用例打标记，运行的时候，只运行打标记的用例。
   300个回归用例。-- 打标记50个，作为冒烟测试。

   1、得先注册标记名
      pytest.ini
      [pytest]
      markers=
         标签名:说明
         标签名
         标签名

   2、给测试用例/测试类打标记
      @pytest.mark.已注册的标记名

      在测试类里，使用以下申明（测试类下，所有用例都被打上该标签）：
      class TestClass(object):
          pytestmark = pytest.mark.已注册标签名
          pytestmark = [pytest.mark.标签1, pytest.mark.标签2]  # 多标签模式

      在模块文件里，同理（py文件下，所有测试函数和测试类里的测试函数，都有该标签）：
      import pytest
      pytestmark = pytest.mark.webtest
      pytestmark = [pytest.mark.标签1, pytest.mark.标签2]  # 多标签模式

   3、运行时设置只运行标记的用例
      pytest命令行：-m 标记名
      在收集到的所有用例当中，只运行有标记名的用例。
	  
	 前置后置：
   unittest:
          setup/teardown
          setup当中得到的变量，怎么传递给测试用例的：self.XXX = value
          setupClass,tearDownClass
          setupClass当中得到的变量，怎么传递给测试用例的：cls.XXX = value

fixture:

    先定义再调用、共享。

    定义：
    1、函数实现的，函数名称不固定。 --- 如何知道它是前置后置？
       @pytest.fixture
       def fix():
        pass

    2、前置操作和后置操作，写在一个函数里。 -- 怎么区分哪些是前置代码？后置代码？
       @pytest.fixture
       def fix():
        前置代码
        yeild  # 分隔线
        后置代码

    3、4个作用域。测试函数(function)、测试类(class)、测试模块文件(module)、测试会话(session)
        @pytest.fixture(scope=function(默认值)/class/module/session)
           def fix():
            前置代码
            yeild  # 分隔线
            后置代码

    4、不跟测试类/测试函数放在一起。   ---如果说有测试类要用的话，怎么办？需要的时候再调用。


    5、前置操作得到的一些数据，如何传递给测试用例？
      yeild 返回值

      在测试用例当中：以fixture函数名作为用例参数。用例参数接收返回值。
      测试函数的参数：1、fixture   2、参数化



    5、共享机制：conftest.py
       conftest.py   定义fixture,可以定义多个。



调用：
  用例/类 主动调用 fixtures.

  哪儿需要哪儿调：

  @pytest.mark.usefixtures("fixture的函数名称")
  测试类/测试函数

  如果fixture有返回值，
  那么，将它作为测试函数的参数时，则可以不用使用： @pytest.mark.usefixtures("fixture的函数名称")




conftest.py共享

1、所在目录下全面共享
2、支持嵌套

"""
1、放的都是fixture
2、fixtures可以对外共享。
3、共享的范围：
   当前conftest.py所在目录下的(含子孙目录)，所有用例共享
4、conftest.py，是可以创建多个，在不同的包下。可以层级创建的。
5、优先级：就近原则！！
    发现fiXture: 用例自己的模块 -》用例所在目录下的conftest.py -》目录的父级目录下的conftest.py

6、嵌套方式：
   6.1 什么时候嵌套？  一个fixture，想完全使用另外一个fixture,并在人家的基础上新增一些代码。
   6.2 怎么嵌套？
       @pytest.fixture
        def fix1():
            pass

        @pytest.fixture
        def fix2(fix1):
            # 新增的代码
            pass
   6.3 嵌套后的执行顺序？
       fix1 的前置
       fix2 的前置
       fix2 的后置
       fix1 的后置

   6.4 可以任意fixture级别嵌套吗？
       fix1 >= fix2的级别


数据驱动实现：
@pytest.mark.parametrized()

在测试用例的前面加上：
@pytest.mark.parametrize("参数名",列表数据)
参数名：用来接收每一项数据，并作为测试用例的参数。
列表数据：一组测试数据。

@pytest.mark.parametrize("参数1,参数2",[(数据1，数据2),(数据1，数据2)])

示例:
   @pytest.mark.parametrize("a,b,c",[(1,3,4),(10,35,45),(22.22,22.22,44.44)])
   def test_add(a,b,c):
        res = a + b
        assert res == c


组合参数化：多组参数，依次组合。
使用多个@pytest.mark.parametrize

示例：用例有4个：0,2/0,3/1,2/1,3  迪卡尔积
@pytest.mark.parametrize("x", [0, 1])
@pytest.mark.parametrize("y", [2, 3])
def test_foo(x, y):
    pass







打标记：mark功能
   对用例打标记，运行的时候，只运行打标记的用例。
   300个回归用例。-- 打标记50个，作为冒烟测试。

   1、得先注册标记名
      pytest.ini
      [pytest]
      markers=
         标签名:说明(只能是英文)
         标签名
         标签名

   2、给测试用例/测试类打标记
      @pytest.mark.已注册的标记名

   3、运行时设置只运行标记的用例
      pytest命令行：-m 标记名
      在收集到的所有用例当中，只运行有标记名的用例。

1、放的都是fixture
2、fixtures可以对外共享。
3、共享的范围：
   当前conftest.py所在目录下的(含子孙目录)，所有用例共享
4、conftest.py，是可以创建多个，在不同的包下。可以层级创建的。
5、优先级：就近原则！！
    发现fiXture: 用例自己的模块 -》用例所在目录下的conftest.py -》目录的父级目录下的conftest.py

6、嵌套方式：
   6.1 什么时候嵌套？  一个fixture，想完全使用另外一个fixture,并在人家的基础上新增一些代码。
   6.2 怎么嵌套？
       @pytest.fixture
        def fix1():
            pass

        @pytest.fixture
        def fix2(fix1):
            # 新增的代码
            pass
   6.3 嵌套后的执行顺序？
       fix1 的前置
       fix2 的前置
       fix2 的后置
       fix1 的后置

   6.4 可以任意fixture级别嵌套吗？
       fix1 >= fix2的级别


day2包下面的conftest.py
	  
1、在cmd命令行当中，执行：allure serve Output/allure_reports （测试结果文件目录 ）
	  

1、基于Pytest框架的自动化测试开发：
   https://mp.weixin.qq.com/s?__biz=MzI4MjcwNTU1MQ==&mid=2247483856&idx=1&sn=937841e57c77c3686ce2644367aa5248&chksm=eb94aa30dce32326b1e46efe63a1146d4d492b754d684135cf3026b26a30d5cb214ac3443a75&token=1584017789&lang=zh_CN#rd
2、pytest+allure+jenkins - 持续集成平台生成allure报告:
   https://www.cnblogs.com/Simple-Small/p/11512337.html
3、pytest文章：
   https://www.cnblogs.com/Simple-Small/tag/pytest/
4、allure命令行工具下载地址：
   https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/
5、pytest+allure+jenkins - 持续集成平台生成allure报告
   https://www.cnblogs.com/Simple-Small/p/11512337.html
   
 