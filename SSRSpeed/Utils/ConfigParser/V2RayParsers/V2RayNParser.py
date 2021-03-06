#coding:utf-8

import logging
import json
logger = logging.getLogger("Sub")

import SSRSpeed.Utils.b64plus as b64plus

class ParserV2RayN(object):
	def __init__(self):
		self.__decodedConfigs = []

	def parseSubsConfig(self,rawLink):
		link = rawLink[8:]
		linkDecoded = b64plus.decode(link).decode("utf-8")
		try:
			_conf = json.loads(linkDecoded,encoding="utf-8")
		except json.JSONDecodeError:
			return None
		try:
			#logger.debug(_conf)
			cfgVersion = str(_conf.get("v","1"))
			server = _conf["add"]
			port = int(_conf["port"])
			_type = _conf.get("type","none") #Obfs type
			uuid = _conf["id"]
			aid = int(_conf["aid"])
			net = _conf["net"]
			group = "N/A"
			if (cfgVersion == "2"):
				host = _conf.get("host","") # http host,web socket host,h2 host,quic encrypt method
				path = _conf.get("path","") #Websocket path, http path, quic encrypt key
			#V2RayN Version 1 Share Link Support
			else:
				try:
					host = _conf.get("host",";").split(";")[0]
					path = _conf.get("host",";").split(";")[1]
				except IndexError:
					pass
			tls = _conf.get("tls","none") #TLS
			tlsHost = host
			security = _conf.get("security","auto")
			remarks = _conf.get("ps",server)
			logger.debug("Server : {},Port : {}, tls-host : {}, Path : {},Type : {},UUID : {},AlterId : {},Network : {},Host : {},TLS : {},Remarks : {},group={}".format(
				server,
				port,
				tlsHost,
				path,
				_type,
				uuid,
				aid,
				net,
				host,
				tls,
				remarks,
				group
			))
			_config = {
				"remarks":remarks,
				"server":server,
				"server_port":port,
				"id":uuid,
				"alterId":aid,
				"security":security,
				"type":_type,
				"path":path,
				"network":net,
				"tls-host":tlsHost,
				"host":host,
				"tls":tls
			}
			return _config
		except:
			logger.exception("Parse {} failed.(V2RayN Method)".format(rawLink))
			return None

	def parseGuiConfig(self,filename):
		with open(filename,"r",encoding="utf-8") as f:
			try:
				config = json.load(f)
			except:
				logger.exception("Not V2RayN Config.")
				f.close()
				return False
			f.close()
		subList = config.get("subItem",[])
		for item in config["vmess"]:
			_dict = {
				"server":item["address"],
				"server_port":item["port"],
				"id":item["id"],
				"alterId":item["alterId"],
				"security":item.get("security","auto"),
				"type":item.get("headerType","none"),
				"path":item.get("path",""),
				"network":item["network"],
				"host":item.get("requestHost",""),
				"tls":item.get("streamSecurity",""),
				"allowInsecure":item.get("allowInsecure",""),
				"subId":item.get("subid",""),
				"remarks":item.get("remarks",item["address"]),
				"group":"N/A"
			}
			subId = _dict["subId"]
			if (subId != ""):
				for sub in subList:
					if (subId == sub.get("id","")):
						_dict["group"] = sub.get("remarks","N/A")
			self.__decodedConfigs.append(_dict)
		return self.__decodedConfigs
	
