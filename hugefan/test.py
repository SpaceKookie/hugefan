class DataHandler:
	class __DataHandler:	
		def __init__(self, meta):
			self.meta = meta
	instance = None	
	def __init__(self, meta):
		if not DataHandler.instance: 
			DataHandler.instance = DataHandler.__DataHandler(meta)
		else:
			DataHandler.instance.val = meta
	def __getattr__(self, name):
		return getattr(self.instance, name)



dh = DataHandler(None)