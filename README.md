# 新闻爬虫入库ES【Sina/Sohu/Netease】

> 2024E8018682045 沈亦婷

## 一、项目部署与启动

根目录下，执行以下命令启动相关服务：

```
docker compose up -d
```

## 二、爬虫运行

本项目包含多个爬虫，可分别运行不同来源的爬虫任务：

1. 运行搜狐爬虫：

```
python main.py --spider sohu
python main.py --spider netease
python main.py --spider sina
```

## 三、ES 数据操作

首先安装 `elasticdump`，官网地址 [https://www.npmjs.com/package/elasticdump]()

```
npm install elasticdump
```

### （一）数据导出

若要从 ES 中导出数据，可使用 `elasticdump` 工具执行以下命令：

```
elasticdump input=http://localhost:9200/news_index \
  --output=NewsSpider/data/news_index_mapping.json \
  --type=mapping
elasticdump input=http://localhost:9200/news_index \
  --output=NewsSpider/data/news_index.json \
  --type=data
```

此命令将把 `http://localhos:9200/news_index` 中的数据导出为 `news_index.json` 文件，并存储在 `/Users/polca/Downloads/` 目录下。

### （二）数据导入

要将数据导入到 ES 中，可使用以下命令：

```
elasticdump \
  --input= NewsSpider/data/news_index.json
  --output=http://{IP}:9200/news_index \
  --type=data 
```

确保 `news_index.json` 文件存在且路径正确，将数据库的IP替换为正确的IP地址（默认为localhost）



## 四、检索

### 倒排索引检索基础

* **理解倒排索引** ：倒排索引是 ES 实现快速检索的核心数据结构。它将文档中的每个关键词都映射到包含该关键词的文档列表。例如，有三个文档分别是 “我爱北京”“北京欢迎你”“欢迎来到北京”，那么 “北京” 这个词的倒排索引就会指向这三个文档，“欢迎” 会指向后两个文档 。
* **基本检索语法**
  * **简单查询** ：使用 `match`查询来进行基本的全文检索。例如，要查找包含 “北京” 的文档，可以这样写：

```json
{
  "query": {
    "match": {
      "content": "北京"
    }
  }
}
```

## 其他

**ES添加字段**

```
PUT /news_index/_mapping
{
  "properties": {
    "new_field1": {
      "type": "integer"
    },
    "new_field2": {
      "type": "integer"
    }
  }
}
```
