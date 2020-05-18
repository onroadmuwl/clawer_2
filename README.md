本项目爬取在淘宝中关键词为衬衫的所有商品，并进行数据分析<br>
==
1、catch.py<br>
--
淘宝网页和微博不同，采取的是json存储模式，需要先读取出json中的数据，然后写入到excel中，需要用到正则表达式，不需要xpath。<br>



2、connect.py<br>
--
淘宝存在反爬虫机制，在采取休眠的情况下，仍会出现滑块验证，不能一次全都获取到想要的数据，所以要把几次的数据写到一个excel中。<br>





3、deal_data.py<br>
--
把爬取到的不规范数据进行处理<br>




4、analyze.py<br>
--
用pyecharts和wordcloud对获取到的数据进行可视化分析<br>
