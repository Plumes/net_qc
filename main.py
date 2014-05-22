#coding:utf-8

import os.path
import re
import tornado.httpserver
import tornado.web
import tornado.ioloop
import tornado.options
import torndb
import datetime
import json

from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="database host")
define("mysql_database", default="net_qc", help="database name")
define("mysql_user", default="root")
define("mysql_password", default="123456qwe")

def reverseEscape(raw_str):
    raw_str = raw_str.replace("&lt;","<")
    raw_str = raw_str.replace("&gt;",">")
    raw_str = raw_str.replace("&amp;","&")
    raw_str = raw_str.replace("&quot;","\"")
    raw_str = raw_str.replace("&#39;","\'")
    return (raw_str)

class Application(tornado.web.Application):
    """docstring for Application"""
    def __init__(self):
        handlers = [
            (r"/",IndexHandler),
            (r"/category",CategoryHandler),
            (r"/post",PostHandler),                                                                                                                                                                       
            (r"/login", LoginHandler),
            (r"/dashboard/", DashboardHandler),
            (r"/dashboard/settings", SettingsHandler),
            (r"/dashboard/manage/posts/(\w*)", PostsManagement),
            (r"/dashboard/manage/categories/(\w*)", CatsManagement),
            (r"/dashboard/manage/users/(\w*)", UsersManagement),
        ]
        settings = dict(
            cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            site_url="http://192.168.56.2:8080/",
            login_url="/login",
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
    def get_current_user(self):
        return self.get_secure_cookie("user")
    def getUnionCatagories(self):
        categories = self.db.query("SELECT * FROM category WHERE parentid=1 ORDER BY catid")
        for category in categories:
            child_cats = []
            child_cats = self.db.query("SELECT * FROM category WHERE parentid={0} ORDER BY catid".format(category["catid"]))
            category["child_cats"] = child_cats
        return (categories)

class LoginHandler(BaseHandler):
    def get(self):
        self.write('<html><body><form action="/login" method="post">'
                    'Name: <input type="text" name="name">'
                    'Password: <input type="password" name="pwd">'
                    '<input type="submit" value="Sign in">'
                    '</form></body></html>')

    def post(self):
        raw_name = self.get_argument("name")
        pwd =  self.db.query("SELECT pwd FROM users WHERE name={0}".format(raw_name))
        self.set_secure_cookie("user", self.get_argument("name"))
        self.redirect("/")

class IndexHandler(BaseHandler):
    """docstring for IndexHandler"""
    def get(self):
        if not self.current_user:
            self.current_user="none"
        name = tornado.escape.xhtml_escape(self.current_user)
        #self.write("Hello, " + name)
        cur = 0
        categories = self.getUnionCatagories()

        teachers = self.db.query ("SELECT * FROM teachers ORDER BY id")
        news = self.db.query ("SELECT entry_id, title, post_time FROM entries WHERE cat_id=2 ORDER BY post_time DESC LIMIT 0,10")
        links = self.db.query ("SELECT * FROM friends_link")
        self.render("index.html", categories=categories, teachers=teachers, news=news, links=links,cur=cur)
        #for c in categories:
        #print(len(categories))

class CategoryHandler(BaseHandler):
    def get(self):
        cid = int(self.get_argument('id'))
        categories = self.getUnionCatagories()

        hot_posts = self.db.query ("SELECT entry_id, title, post_time FROM entries WHERE cat_id=2 ORDER BY post_time DESC LIMIT 0,10")

        posts = self.db.query("SELECT entry_id, title, post_time, author, name FROM entries INNER JOIN  `users` ON entries.author = users.uid  WHERE cat_id={0} AND users.authority <2 AND users.authority >=0 ORDER BY post_time DESC LIMIT 0,10".format(cid))
        self.render("category.html", categories=categories, posts=posts, hot_posts=hot_posts, cid=cid)

class PostHandler(BaseHandler):
    def get(self):
        post_id = self.get_argument("id")
        post = self.db.query("SELECT * FROM entries WHERE entry_id={0}".format(post_id) )[0]
        author = self.db.query("SELECT name FROM users WHERE uid={0}".format(post["author"]))[0]
        categories = self.getUnionCatagories()
        #print(post["content"].encode("UTF-8"))
        post["content"] = reverseEscape(post["content"].encode("UTF-8"))
        hot_posts = self.db.query ("SELECT entry_id, title, post_time FROM entries WHERE cat_id=1 ORDER BY post_time DESC LIMIT 0,10")
        self.render("post.html",categories=categories, post=post, author=author["name"], hot_posts=hot_posts, cid=post["cat_id"] )

class DashboardHandler(BaseHandler):
    def privilegeCheck(self):
        privilege =  self.get_secure_cookie("privilege")
        if not privilege or int(privilege) > 1:
            self.redirect("/dashboard/error/")

    def getCatagories(self):
        categories = self.db.query("SELECT * FROM category WHERE parentid=1 ORDER BY catid")
        child_cats = {}
        for category in categories:
            tmp = []
            tmp = self.db.query("SELECT * FROM category WHERE parentid={0} ORDER BY catid".format(category["catid"]))
            child_cats[category["catid"]] = tmp
        return (categories,child_cats)

    def get(self):
        self.set_secure_cookie("user","admin")
        self.set_secure_cookie("privilege","0")
        self.privilegeCheck()

        uname = self.get_secure_cookie("user")
        self.render("dashboard/dashboard.html",user=uname)

class SettingsHandler(DashboardHandler):
    def get(self):
        self.privilegeCheck()

class PostsManagement(DashboardHandler):


    def get(self, oper):
        self.privilegeCheck()
        uname = self.get_secure_cookie("user")
        if oper=="new":
            categories,child_cats = self.getCatagories()
            self.render("dashboard/write_post.html",user=uname, categories=categories, child_cats=child_cats )
        elif oper=="modify":
            post_id=self.get_argument("id",default="0",strip=True)
            if int(post_id)>0:
                post = self.db.query("SELECT * FROM entries WHERE entry_id={0}".format(post_id) )[0]
                parentid = self.db.get("SELECT parentid FROM category WHERE catid={0}".format(post["cat_id"]))["parentid"]
                post["parentid"] = parentid
                post["content"] = reverseEscape(post["content"].encode("UTF-8"))
                categories,child_cats = self.getCatagories()
                self.render("dashboard/modify_post.html",post=post, user=uname, categories=categories, child_cats=child_cats)
        else:
            posts = self.db.query('''SELECT entry_id, title, post_time, author, name, catname
                                    FROM entries
                                    INNER JOIN  `users` ON entries.author = users.uid
                                    INNER JOIN  `category` ON entries.cat_id = category.catid
                                    WHERE users.authority <2
                                    AND users.authority >=0
                                    ORDER BY post_time DESC 
                                    LIMIT 0 , 10''')
            categories,child_cats = self.getCatagories()
            self.render("dashboard/show_posts.html",posts=posts, categories=categories, child_cats=child_cats, user=uname)

    def post(self, oper):
        self.privilegeCheck()
        uname = self.get_secure_cookie("user")
        uid = self.db.query("SELECT uid FROM users WHERE name=\"{0}\"".format(uname))[0]["uid"]
        if oper == "pull":
            # pull posts begin
            pid = self.get_argument("pid", default="0", strip=True)
            catid = self.get_argument("catid",default="0",strip=True)
            pagenum = int(self.get_argument("pagenum",default="0",strip=True))
            #parentid = self.db.query("SELECT parentid FROM category WHERE catid={0}".format(catid))
            if catid == "0":
                catid="catid"
            if pid=="0":
                pid="parentid"
            posts = []
            posts = self.db.query('''SELECT entry_id, title, post_time, author, name, catname 
                                    FROM entries 
                                    INNER JOIN  `users` ON entries.author = users.uid 
                                    INNER JOIN  `category` ON entries.cat_id = category.catid 
                                    WHERE category.parentid = {0} AND 
                                    entries.cat_id={1} AND 
                                    users.authority <2 AND 
                                    users.authority >=0 
                                    ORDER BY post_time DESC  
                                    LIMIT {2} , {3}'''.format(pid, catid, pagenum, pagenum+10))
            if len(posts) == 0:
                posts = self.db.query('''SELECT entry_id, title, post_time, author, name, catname 
                                    FROM entries 
                                    INNER JOIN  `users` ON entries.author = users.uid 
                                    INNER JOIN  `category` ON entries.cat_id = category.catid 
                                    WHERE category.parentid = {0} AND 
                                    entries.cat_id={1} AND 
                                    users.authority <2 AND 
                                    users.authority >=0 
                                    ORDER BY post_time DESC  
                                    LIMIT {2} , {3}'''.format(1, pid, pagenum, pagenum+10))
            for post in posts:
                post["post_time"] = post["post_time"].strftime("%Y年%m月%d日")
            if len(posts) > 0:
                status = 0
            else:
                status = 1
            self.write(json.dumps({"status":status,"posts":posts}))
            # pull posts end
        elif oper=="new":
            # new post begin
            title = self.get_argument("title").encode("UTF-8")
            content = tornado.escape.xhtml_escape(self.get_argument("content").encode("UTF-8"))
            catid = self.get_argument("catid",default="2",strip=True)
            self.db.execute('''INSERT INTO `entries`(`cat_id`, `title`, `content`, `author`, `post_time` ) 
                            VALUES ({0}, \"{1}\", \"{2}\", {3}, NOW() )'''.format(catid, title, content, uid))
            self.redirect("./")
            # new post end
        elif oper=="modify":
            # new post begin
            post_id=self.get_argument("post_id",default="0",strip=True)
            title = self.get_argument("title").encode("UTF-8")
            content = tornado.escape.xhtml_escape(self.get_argument("content").encode("UTF-8"))
            catid = self.get_argument("catid",default="2",strip=True)
            self.db.execute('''UPDATE `entries` SET `cat_id`={0}, `title`=\"{1}\", `content`=\"{2}\", `author`={3}, `post_time`=NOW() WHERE entry_id={4}'''.format(catid, title, content, uid, post_id))
            self.redirect("./")
            # new post end
            
        elif oper=="delete":
            post_id_list = self.get_arguments("post_id_list[]")
            for post_id in post_id_list:
                self.db.execute("DELETE FROM entries WHERE entry_id={0}".format(int(post_id)))
            #print (post_id_list)
            #self.write("del"+id)


class CatsManagement(DashboardHandler):
    def get(self, oper):
        self.privilegeCheck()
        categories,child_cats = self.getCatagories()
        self.render("dashboard/categories.html", categories=categories, child_cats=child_cats, user=self.current_user)
        
    def post(self,oper):
        self.privilegeCheck()
        if oper=="add":
            parentid = int(self.get_argument("parentid",default="0",strip=True))
            catname = tornado.escape.xhtml_escape(self.get_argument("catname").encode("UTF-8"))
            if parentid>0 and len(catname)>0:
                self.db.execute("INSERT INTO category (`parentid`,`catname`) VALUES ({0},\"{1}\")".format(parentid,catname))

        elif oper=="modify":
            catid = int(self.get_argument("catid",default="0",strip=True))
            parentid = int(self.get_argument("parentid",default="0",strip=True))
            catname = tornado.escape.xhtml_escape(self.get_argument("catname").encode("UTF-8"))
            if catid>1 and parentid>0 and len(catname)>0:
                pid = self.db.get("SELECT parentid FROM category WHERE catid={0}".format(catid))
                if pid=="1":
                    parentid = "parentid"
                self.db.execute("UPDATE category SET `parentid`={0}, `catname`=\"{1}\" WHERE catid={2}".format(parentid,catname,catid))

        elif oper=="delete":
            catid = int(self.get_argument("catid",default="0",strip=True))
            self.db.execute("DELETE FROM category WHERE catid={0}".format(catid))
            self.db.execute("DELETE FROM entries WHERE cat_id={0}".format(catid))



class UsersManagement(DashboardHandler):
    pass

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()