from com.crawler.hbase.ContentHBaseDao import ContentHBaseDaoImp
from thrift.transport import TTransport, TSocket
from thrift.protocol import TBinaryProtocol
from hbase import Hbase

# 
# hbase = ContentHBaseDaoImp()
# 
# hbase.saveContentModel(None)

transport = TSocket.TSocket("192.168.2.128", 9090);

transport = TTransport.TBufferedTransport(transport)

protocol = TBinaryProtocol.TBinaryProtocol(transport);

client = Hbase.Client(protocol)

transport.open()    