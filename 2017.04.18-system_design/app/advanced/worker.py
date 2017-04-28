import json

from kafka import KafkaConsumer
from kafka import KafkaProducer


class Worker(object):
    def __init__(self, topic, hosts="127.0.0.1:9092", group="testing", zookeeper_hosts="127.0.0.1:2181"):
        self.topic = topic
        self.consumer = KafkaConsumer(topic, bootstrap_servers=hosts)
        self.producer = KafkaProducer(bootstrap_servers=hosts)
        
        self.init()
    
    def init(self):
        pass
    
    def get_classname(self):
        return type(self).__name__.replace("Worker", "").lower()
    
    def run(self):
        for message in self.consumer:
            request = json.loads(message.value)
            
            self.post_process(request, self.process(request))
            
    def process(self, request):
        raise NotImplementedError

    def worker_process(self, request, ret, next_worker):
        request.setdefault("events", [])
        request["events"].append(ret)
            
        self.producer.send(next_worker, json.dumps(request))
        print "pass the request to the next worker - {}".format(next_worker)
        
    def post_process(self, request, ret):
        if ret:
            workers = request.get("workers", "")
            if len(workers) == 0:
                workers = [request.get("final_output", "console")]

            if isinstance(workers, (str, unicode)):
                workers = workers.split("|")
                
            next_worker = workers.pop()

            request["workers"] = "|".join(workers)
            if "worker" in next_worker:
                self.worker_process(request, ret, next_worker)
            elif "console" in next_worker:
                events = request.get("events", [])
                events.append(ret)
                for r in events:
                    print r
            elif "mongo" in next_worker:
                results = {}
                if "events" not in request:
                    results = {"customer_id": request["customer_id"],
                               "by": self.topic.replace("worker", "mongo"),
                               "ret": ret}
                else:
                    request["events"].append(ret)
                    results = {"customer_id": request["customer_id"],
                               "by": self.topic.replace("worker", "mongo"),
                               "ret": {"events": request["events"]}}
                
                self.producer.send("worker.mongo", json.dumps(results))
                
                print "send request to kafka({}) with {}".format("worker.mongo", results)
        else:
            pass
        

class CollectionWorker(Worker):
    def init(self):
        super(CollectionWorker, self).init()
        
        self.pool = {}
                
    def init_requirements(self, requirements):
        self.requirements = requirements
        
    def init_db(self):
        pass
    
    def insert(self, record):
        pass
        
    def process(self, request):        
        customer_id = request["customer_id"]
        ret = request["ret"]
        
        by = request["by"]
        del request["by"]
        
        self.pool.setdefault(customer_id, {}).setdefault("requirements", self.requirements[:])
        if customer_id in self.pool:
            self.pool[customer_id].update(ret)
            self.pool[customer_id]["requirements"].remove(by)
            
            if len(self.pool[customer_id]["requirements"]) == 0:
                del self.pool[customer_id]["requirements"]
                self.pool[customer_id]["customer_id"] = customer_id
                
                self.insert(self.pool[customer_id])
                del self.pool[customer_id]
                
                print "insert {} into mongodb".format(ret)