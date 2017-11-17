import tornado.httpserver
import tornado.web
import asyncio
import asyncio_redis
from tornado.platform.asyncio import AsyncIOMainLoop
import motor.motor_asyncio
r = None
class CounterHandler(tornado.web.RequestHandler):
	async def get(self):
		global r
		count = await r.incr('count')
		self.write('The count is ' + str(count))
class ResetHandler(tornado.web.RequestHandler):
	async def get(self):
		global r
		finalcount = await r.get('count')
		await db.counts.insert_one({'count':finalcount})
		self.write('Final count is ' + finalcount)
		await r.set('count','0')

async def InitRedis():
	global r
	print("InitRedis begin")
	r = await asyncio_redis.Pool.create(host='localhost',port=6379,poolsize=10)
	print("InitRedis end")

if __name__ == '__main__':
	mongodb = motor.motor_asyncio.AsyncIOMotorClient('localhost',27017)
	db = mongodb.geetest_python
	counts = db.counts
	app = tornado.web.Application(handlers=[
		(r"/counter",CounterHandler),
		(r"/reset",ResetHandler)
		])
	
	AsyncIOMainLoop().install()
	loop = asyncio.get_event_loop()
	loop.run_until_complete(InitRedis())
	httpserver = tornado.httpserver.HTTPServer(app)
	httpserver.listen(8001)
	print("httpserver is running!")
	loop.run_forever()