from http.server import HTTPServer, BaseHTTPRequestHandler

import update_poem
import asyncio
import nltk
nltk.download('averaged_perceptron_tagger')
			  
class MyHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		
		with open('templates/index.html', 'r') as f:
			content = f.read()
		#print(content)
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()
		self.wfile.write(bytes(content, 'utf8'))

		
		asyncio.run(update_poem.update())
	
		

httpd = HTTPServer(('', 8000), MyHandler)
httpd.serve_forever()
