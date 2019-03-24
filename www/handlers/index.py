# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import logging
import tornado.web

from handlers.base import BaseHandler
sys.path.append('lib')
import ast
import json
import time
import urllib2

class IndexHandler(BaseHandler):
    def get(self):
        q = self.get_argument('q', '')
        self.render('index.html', q=q)

class HCheckHandler(BaseHandler):
    def get(self):
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        templates_dir = 'templates'
        hdn_filename = '_hcheck.hdn'
        err_filename = 'error.html'
        try : fid = open(templates_dir + "/" + hdn_filename, 'r')
        except :
            self.set_status(404)
            self.render(err_filename)
        else :
            fid.close()
            self.render(hdn_filename)

class LNGHandler(BaseHandler):
    def get_request_ip(self):
        client_ip = self.request.headers.get("X-Forwarded-For")
        client_ip = self.request.remote_ip
        if not client_ip :
            client_ip = self.request.remote_ip
        return client_ip

    def get(self) :
        # check ip
        #client_ip = self.get_request_ip()
        #if self.localhost_ip != client_ip:
        #    self.write((dict(success=True, status=500, output='', client_ip=client_ip, localhost_ip=self.localhost_ip)))

        #else:
        start_time = time.time()
        
        mode  = self.get_argument('mode', '')
        callback = self.get_argument('callback', '')
        debug = {}
        debug['callback'] = callback

        debug = {}
        rst = {}
        if mode == 'debug' : rst['debug'] = debug

        try :
            # get params
            params = { k: self.get_argument(k) for k in self.request.arguments }
            #self.log.info(json.dumps(params,ensure_ascii=False,encoding="utf-8"))
            template = ''
            key_value = {}
            for k,v in params.items():
                key_value[k] = v
            if key_value['query']:
                query = key_value['query']
            else:
                query="1"
            out = self.lng.search_lotto_dic(query)
        except Exception, e :
            rst['status'] = 500
            rst['msg'] = 'answerGenerator() fail, ' + str(e)
            rst['output'] = []
        else :
            rst['status'] = 200
            rst['output'] = out
 
        if mode == 'debug' :
            duration_time = time.time() - start_time
            debug['exectime'] = duration_time

        try :
            ret = json.dumps(rst,ensure_ascii=False,encoding="utf-8")
        except :
            msg = "json.dumps() fail for query %s" % (query)
            self.log.debug(msg + "\n")
            err = {}
            err['status'] = 500
            err['msg'] = msg
            ret = json.dumps(err)

        if mode == 'debug' :
            self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')

        if callback.strip() :
            self.set_header('Content-Type', 'application/javascript; charset=utf-8')
            ret = 'if (typeof %s === "function") %s(%s);' % (callback, callback, ret)
        else :
            self.set_header('Content-Type', 'application/json; charset=utf-8')

        self.write(ret)
        self.finish()

    def post(self):
        self.get()

