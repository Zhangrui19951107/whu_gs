class site(object):
	name = ''
	crawlername = ''
	limit = 0.0
	v = 0.0
	weight = 0
	whethermass = 0
	inuse = 0

	def __init__(self,name,crawlername,limit,weight,inuse):
		self.name = name
		self.limit = limit
		self.weight = weight
		self.crawlername = crawlername
		self.inuse = inuse


	def pr(self):
		print "name:"
		print self.name
		print "crawlername:"
		print self.crawlername
		print "limit:"
		print self.limit
		print "v:"
		print self.v
		print "weight:"
		print self.weight
		print "inuse:"
		print self.inuse
