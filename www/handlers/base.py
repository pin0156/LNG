# -*- coding: utf-8 -*-
import tornado.web
import logging

class BaseHandler(tornado.web.RequestHandler):
    @property
    def log(self):
        return self.application.log
    @property
    def lng(self):
        return self.application.lng
    @property
    def localhost_ip(self):
        return self.application.localhost_ip
