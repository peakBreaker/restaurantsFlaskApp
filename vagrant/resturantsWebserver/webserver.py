from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from model.model import list_resturants, insert_resturant, editname_resturant, delete_resturant
import cgi

class webserverHandler(BaseHTTPRequestHandler):
    def gotpage(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        return

    def do_GET(self):
        if self.path.endswith("/resturants"):
            print "Got request for resturants"
            self.gotpage()

            output = ""
            output = open("views/resturants.html", "r")
            body = ""
            for r in list_resturants():
                body += """<div>Resturant: {}</div> <a href='/resturant/{id}/edit'>
                        Edit</a><br><a href='/resturant/{id}/delete'>Delete</a>
                        """.format(r.name, id=r.id)
            print body
            output = (output.read().format(body))
            self.wfile.write(output)
            print output
            return
        elif self.path.endswith("resturants/new"):
            self.gotpage()
            output = open("views/newresturant.html", "r")
            self.wfile.write(output.read())
        elif self.path.endswith("/edit"):
            self.gotpage()
            resturantID = self.path.split("/")[-2]
            output = open("views/editresturant.html", "r")
            output = output.read().format(id=str(resturantID))
            self.wfile.write(output)
        elif self.path.endswith("/delete"):
            self.gotpage()
            resturantID = self.path.split("/")[-2]
            output = open("views/deleteresturant.html", "r")
            output = output.read().format(id=str(resturantID))
            self.wfile.write(output)
        else:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/resturants/new"):
                print "got post request!"
                self.send_response(302)
                self.send_header('content-type', 'text/html')
                self.end_headers()
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type')
                )
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    name = fields.get('name')[0]
                    address = fields.get('address')[0]
                    city = fields.get('city')[0]
                    state = fields.get('state')[0]
                    zipCode = fields.get('zipCode')[0]
                output = open("views/submitted.html", "r")
                insert_resturant(name, address, city, state, zipCode)
                self.wfile.write(output.read())
            elif self.path.endswith("/resturants/edit"):
                print "got post request!"
                self.send_response(302)
                self.send_header('content-type', 'text/html')
                self.end_headers()
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type')
                )
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    id = fields.get('id')[0]
                    name = fields.get('name')[0]
                output = open("views/submitted.html", "r")
                editname_resturant(id, name)
                self.wfile.write(output.read())
            elif self.path.endswith("/resturants/delete"):
                print "got post request!"
                self.send_response(302)
                self.send_header('content-type', 'text/html')
                self.end_headers()
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type')
                )
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    id = fields.get('id')[0]
                output = open("views/submitted.html", "r")
                delete_resturant(id)
                self.wfile.write(output.read())
        except Exception as e:
            print e

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print "Serving application on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print "Shutting down webserver..."
        server.socket.close()

if __name__ == '__main__':
    main()
