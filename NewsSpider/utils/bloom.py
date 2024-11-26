from hashlib import md5
from elasticsearch import Elasticsearch

class SimpleHash(object):
    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed

    def hash(self, value):
        ret = 0
        for i in range(len(value)):
            ret += self.seed * ret + ord(value[i])
        return (self.cap - 1) & ret


from elasticsearch import Elasticsearch, NotFoundError
from hashlib import md5

class BloomFilter(object):
    def __init__(self, host='localhost', port=9200, index_name='bloom_filter', key='NewsSpider'):
        # 初始化 Elasticsearch 客户端
        self.es = Elasticsearch([{'host': host, 'port': port, 'scheme': 'http'}])
        self.index_name = index_name
        self.key = key
    
    def contains(self, str_input):
        """检查 Elasticsearch 中是否已经包含给定的字符串"""
        if not str_input:
            return False
        
        # 使用 MD5 进行哈希
        m5 = md5()
        m5.update(str_input.encode('utf-8'))
        str_input_hash = m5.hexdigest()  # 计算 MD5 哈希值
        
        # 直接使用 MD5 哈希值作为文档 ID
        doc_id = str_input_hash
        
        # 检查 Elasticsearch 中是否存在该文档
        try:
            res = self.es.get(index=self.index_name, id=doc_id)
            return res['found']  # 如果找到文档，则返回 True
        except NotFoundError:
            # 文档不存在的情况
            return False
        except Exception as e:
            # 处理其他异常情况
            print(f"Error occurred while checking document in Elasticsearch: {e}")
            return False

    def insert(self, str_input):
        """将字符串插入 Elasticsearch 索引，标记为已存在"""
        m5 = md5()
        m5.update(str_input.encode('utf-8'))
        str_input_hash = m5.hexdigest()
        
        # 直接使用 MD5 哈希值作为文档 ID
        doc_id = str_input_hash
        
        # 构造文档内容
        doc = {
            'hash': str_input_hash,
            'original_input': str_input
        }
        
        # 插入文档到 Elasticsearch
        try:
            self.es.index(index=self.index_name, id=doc_id, body=doc)
            print(f"Document inserted with ID: {doc_id}")
        except Exception as e:
            print(f"Failed to insert into Elasticsearch: {e}")

if __name__ == '__main__':
    bf = BloomFilter()
    if bf.contains('http://www.baidu.co'):   # 判断字符串是否存在
        print('exists!')
    else:
        print('not exists!')
        bf.insert('http://www.baidu.co')