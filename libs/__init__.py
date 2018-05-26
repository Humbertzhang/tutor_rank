from . import ccnu
import redis
import pickle

r = redis.StrictRedis(host = "localhost", port = 6379, db = 0)
universities_list = pickle.load(r.get("universities"))
universities_auth = {
    "华中师范大学": ccnu.Ccnu
}

