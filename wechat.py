import tornado.web
import tornado.options
import tornado.ioloop
import tornado.httpserver
import hashlib
import xmltodict
import time

WECHAT_TOKEN = "lxhsec"
tornado.options.define("port", default=8000,type=int, help="") 

class Wechat_handler(tornado.web.RequestHandler):
	def prepare(self):
		signature = self.get_argument("signature")
		timestamp = self.get_argument("timestamp")
		nonce = self.get_argument("nonce")  
		tmp = [WECHAT_TOKEN, timestamp, nonce]
		tmp.sort()
		tmp = "".join(tmp)
		sigsha1 = hashlib.sha1(tmp).hexdigest()
		if signature != sigsha1:
			self.write("error")
	def get(self):
		echostr = self.get_argument("echostr")
		self.write(echostr)

	def post(self):
		"""
<xml>
	<ToUserName><![CDATA[toUser]]></ToUserName>
	<FromUserName><![CDATA[fromUser]]></FromUserName> 
	<CreateTime>1348831860</CreateTime>
	<MsgType><![CDATA[text]]></MsgType>
	<Content><![CDATA[this is a test]]></Content>
	<MsgId>1234567890123456</MsgId>
 </xml>
		"""
		xml_data = self.request.body
		dict_data = xmltodict.parse(xml_data)
		data_type = dict_data['xml']['MsgType']
		if data_type == 'text':
			"""text"""
			content = dict_data['xml']['Content']
			rep_data = {
				"xml": {
					"ToUserName" : dict_data['xml']['FromUserName'],
					"FromUserName" : dict_data['xml']['ToUserName'],
					"CreateTime" : int(time.time()),
					"MsgType" : "text",
					"Content" : content,
				}
			}
			self.write(xmltodict.unparse(rep_data))
		else:
			rep_data = {
				"xml": {
					"ToUserName" : dict_data['xml']['FromUserName'],
					"FromUserName" : dict_data['xml']['ToUserName'],
					"CreateTime" : int(time.time()),
					"MsgType" : "text",
					"Content" : "I love you",
				}
			}





def main():
	tornado.options.parse_command_line()
	app = tornado.web.Application([
		(r"/wechat8000", Wechat_handler),


		])
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(tornado.options.options.port)
	tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
	main()
