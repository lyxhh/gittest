import tornado.web
import tornado.options
import tornado.ioloop
import tornado.httpserver
import hashlib

WECHAT_TOKEN = "lxhsec"
tornado.options.define("port", default=8000,type=int, help="") 

class Wechat_handle(tornado.web.RequestHandler):
	def get(self):
		signature = self.get_argument("signature")
		timestamp = self.get_argument("timestamp")
		nonce = self.get_argument("nonce")  
		echostr = self.get_argument("echostr")
		tmp = [WECHAT_TOKEN, timestamp, nonce]
		tmp.sort()
		tmp = "".join(tmp)
		sigsha1 = hashlib.sha1(tmp).hexdigest()
		if signature == sigsha1:
			self.write(echostr)

		else:
			self.write("error")





def main():
	app = tornado.web.Application([
		(r"/wechat8000", Wechat_handler),


		])
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(tornado.options.options.port)
	tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
	main()