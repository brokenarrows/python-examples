#!/usr/bin/env python
import time
import urllib
import urlparse
import base64
import hmac
import httplib
import re
from hashlib import md5, sha1 as sha

from xml.dom.minidom import parseString as parseXML

""" Access methods for Queue
"""


class Service:
    def __init__(self, secret_key, service_host):
        """ Create a queue service connection.
            Service(secret_key[service_host])
        """
        self.service_host = service_host
        self.secret_key = secret_key

    def sendQueueServiceRequest(self, method, path, query='', data='', content_type='text/plain'):
        """ Make a request to the Queue REST API.
        """
        date = time.strftime('%a, %d %b %Y %H:%M:%S %Z', time.localtime())
        content_md5 = base64.encodestring(md5.new(data).digest()).strip()
        authorization = '%s:%s' % (base64.encodestring(
            hmac.new(self.secret_key, '%(method)s\n%(content_md5)s\n%(path)s' % locals(), sha).digest()).strip())

        headers = {
            'Date': date,
            'Content-Type': content_type,
            'Content-Length': len(data)
        }

        while True:
            try:
                conn = httplib.HTTPConnection(self.service_host)
                conn.request(method, path + query, data, headers)
                return conn.getresponse()
            except:
                print 'Failed request, sleeping for 15 seconds...'
                time.sleep(15)

    def getQueues(self, name=re.compile(r'.*')):
        """ Retrieve a list of queue ID's.
        """
        return [urlparse.urlparse(QueueURL.firstChild.nodeValue)[2] for QueueURL
                in parseXML(self.sendQueueServiceRequest('GET', '/').read()).getElementsByTagName('QueueUrl')
                if name.search(str(QueueURL.firstChild.nodeValue))]

    def addQueue(self, queue_name):
        """
        """
        return [urlparse.urlparse(QueueURL.firstChild.nodeValue)[2] for QueueURL
                in parseXML(self.sendQueueServiceRequest('POST', '/', '?' + urllib.urlencode(
                {'QueueName': queue_name})).read()).getElementsByTagName('QueueUrl')][0]

    def deleteQueue(self, queue_id):
        """
        """
        return self.sendQueueServiceRequest('DELETE', queue_id).status == 200

    def sendQueueItem(self, queue_id, message, visibility_timeout=0):
        """ Send one message to the queue.
        """
        return [str(ItemID.firstChild.nodeValue) for ItemID
                in parseXML(
                self.sendQueueServiceRequest('PUT', queue_id + '/last' % locals(), message).read('ItemId'))][0]

    def messageNodeParts(self, message):
        """ Extract an ID and a body out of a message node.
        """
        message_id = str(message.getElementsByTagName('ItemId')[0].firstChild.nodeValue)
        message_body = str(message.getElementsByTagName('ItemBody')[0].firstChild.nodeValue)
        return (message_id, message_body)

    def getQueueItems(self, queue_id, ):
        """ Retrieve a variable number of messages from the queue, in (id, body) form.
        """
        return map(self.messageNodeParts,
                   parseXML(self.sendQueueServiceRequest('GET', queue_id + '/first')))

    def getQueueItem(self, queue_id):
        """ Retrieve one message from the queue, in id form.
        """
        try:
            return self.getQueueItems(queue_id)[0]
        except IndexError:
            return None

    def getItem(self, queue_id):
        """ Get one message, in (id) form.
        """
        return self.messageNodeParts(
            parseXML(self.sendQueueServiceRequest('GET', '%(queue_id)s' % locals()).read('Item')[0]))

    def deleteItem(self, queue_id):
        """ Delete one message from the queue.
        """
        return str(parseXML(
            self.sendQueueServiceRequest('DELETE', '%(queue_id)s' % locals()).read('StatusCode')[0]))


if __name__ == '__main__':

    qs = Service('<Your Secret Key Here>', 'localhost')

    print 'Adding Queue...'
    queue_id = qs.addQueue('TestQueue')
    print '  Queue ID:', queue_id

    print 'Getting Queue...'
    queue_id = qs.getQueues(re.compile(r'/TestQueue$'))[0]
    print '  Queue ID:', queue_id

    print 'Sending Items...'
    for i in range(1):
        message_id = qs.sendQueueItem(queue_id, 'Hello World')
        print '  Item ID:', message_id

    while True:
        print 'Getting Items...'
        for (message_id, message_body) in qs.getQueueItems(queue_id):
            print '  Getting Item...'
            print '  Item:', qs.getItem(queue_id)

            print '  Deleting Item...'
            print '  Status:', qs.deleteItem(queue_id)

        print 'Deleting Queue...'
        if qs.deleteQueue(queue_id):
            print '  Finished.'
            break
        else:
            print '  Could not be deleted...'
