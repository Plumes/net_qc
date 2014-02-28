#coding:utf-8

import os.path
import re
import tornado.httpserver
import tornado.web
import tornado.ioloop
import tornado.options
import torndb
import datetime

from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="database host")
define("mysql_database", default="net_qc", help="database name")
define("mysql_user", default="root")
define("mysql_password", default="123456qwe")

class Application(tornado.web.Application):
	"""docstring for Application"""
	def __init__(self):
		handlers = [
			(r"/",IndexHandler),
			(r"/category",CategoryHandler),
			(r"/post",PostHandler)
		]
		settings = dict(
			orgnization = "哈尔滨工业大学(威海)计算机网络教研室",
			site_name = "哈尔滨工业大学(威海)——计算机网络",
			course_name="计算机网络",
			course_intro="网络技术是支撑当今信息时代的核心技术之一，学习、研究和掌握计算机网络技术成为新时代青年的时尚追求。计算机网络的研究对象是计算机网络的体系结构，研究的主要内容是以TCP/IP体系为核心的各层的协议的基本概念、原理和方法，包括物理层、数据链路层、介质访问子层、网络层、传输层和应用层等内容。",
			template_path = os.path.join(os.path.dirname(__file__),"templates"),
			static_path = os.path.join(os.path.dirname(__file__),"static"),
		)
		tornado.web.Application.__init__(self, handlers, **settings)
		
		self.db = torndb.Connection(
			host = options.mysql_host, database = options.mysql_database,
			user = options.mysql_user, password = options.mysql_password
			)

class BaseHandler(tornado.web.RequestHandler):
 	@property
 	def db(self):
 		return self.application.db

class IndexHandler(BaseHandler):
	"""docstring for IndexHandler"""
	def get(self):
		cur = 0
		categories = self.db.query("SELECT * FROM category WHERE parentid=0 AND catid>0 ORDER BY catid")
		teachers = self.db.query ("SELECT * FROM teachers ORDER BY id")
		news = self.db.query ("SELECT entry_id, title, post_time FROM entries WHERE parent_id=0 AND cat_id=0 ORDER BY post_time DESC LIMIT 0,10")
		links = self.db.query ("SELECT * FROM friends_link")
		self.render("index.html", categories=categories, teachers=teachers, news=news, links=links,cur=cur)
		#for c in categories:
		#print(len(categories))

class CategoryHandler(BaseHandler):
	def get(self):
		cur = 0
		pid = self.get_argument('p')
		cur = int(pid)
		cid = int(self.get_argument('id'))
		if cid<1:
			cid=1

		categories = self.db.query("SELECT * FROM category WHERE parentid=0 AND catid>0 ORDER BY catid")
		cat_list = self.db.query("SELECT * FROM category WHERE parentid={0} AND catid>0 ORDER BY catid".format(pid))
		posts = self.db.query("SELECT entry_id, title, post_time, author, name FROM entries INNER JOIN  `users` ON entries.author = users.uid  WHERE parent_id={0} AND cat_id={1} AND users.authority <2 AND users.authority >=0 ORDER BY post_time DESC LIMIT 0,10".format(pid,cid))
		self.render("category.html", categories=categories, cat_list=cat_list, posts=posts, cur=cur, cid=cid)

class PostHandler(BaseHandler):
    def get(self):
        post_id = self.get_argument("id")
        post = self.db.query("SELECT * FROM entries WHERE entry_id={0}".format(post_id) )[0]
        author = self.db.query("SELECT name FROM users WHERE uid={0}".format(post["author"]))[0]
        categories = self.db.query("SELECT * FROM category WHERE parentid=0 AND catid>0 ORDER BY catid")
        #print (post)
        cat_list = self.db.query("SELECT * FROM category WHERE parentid={0} AND catid>0 ORDER BY catid".format( post["parent_id"] ))
        self.render("post.html",categories=categories, cat_list=cat_list, post=post, author=author["name"], cur=post["parent_id"], cid=post["cat_id"] )

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
	main()