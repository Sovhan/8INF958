# coding : utf-8
import xmlrpclib

p = xmlrpclib.ServerProxy("http://localhost:4118")
p.launchapp("libreoffice", ["--calc"])
