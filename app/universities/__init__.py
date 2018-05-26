from . import ccnu, wust


universities_list = ["CCNU", "WUST"]

universities_engname = {
    "CCNU": "ccnu",
    "WUST": "wust"
}

universities_auth = {
    "CCNU": ccnu.Ccnu,
    "WUST": wust.Wust
}

universities_verify = {
    "WUST": wust.Wust.verify
}
