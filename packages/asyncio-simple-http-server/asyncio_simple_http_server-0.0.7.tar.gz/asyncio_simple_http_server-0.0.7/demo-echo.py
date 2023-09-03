from asyncio_simple_http_server import HttpServer, HttpResponseException, HttpRequest, HttpResponse, HttpHeaders, uri_mapping, uri_variable_mapping, uri_pattern_mapping
import logging.handlers
import logging
import asyncio
import os

logger = logging.getLogger('demo')

class MyHandler:
    @uri_pattern_mapping('/(.*)', method=('GET', 'POST'))
    def foo(self, request: HttpRequest):
        logger.debug('request: %s', request)
        logger.debug('HTTP-REQ METHOD: %s', request.method)
        logger.debug('HTTP-REQ PATH: %s', request.path)
        logger.debug('HTTP-REQ QUERY: %s', request.query_params)
        for k, v in request.headers.items():
          logger.debug('HTTP-REQ HEADER: %s: %s', k, v)
        logger.debug('HTTP-REQ BODY: %s', request.body)
        return {}

async def main():
    http_server = HttpServer()
    http_server.add_handler(MyHandler())
    if False:
      http_server.add_default_response_headers({
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': '*'
      })

    await http_server.start('127.0.0.1', 58888)
    print(f'Serving on {http_server.bind_address_description()}')

    await http_server.serve_forever()

if __name__ == '__main__':
    log_path = '/home/ubuntu/demo-http/http.log'
    if not os.path.exists(os.path.dirname(log_path)):
      os.makedirs(os.path.dirname(log_path))

    log_format = '%(asctime)-15s %(levelname)s %(name)-8s %(filename)s %(funcName)s():%(lineno)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=log_format)
    root_logger = logging.getLogger('')
    handler = logging.handlers.RotatingFileHandler(filename=log_path, maxBytes=(512 << 20), backupCount=16)
    handler.setFormatter(logging.Formatter(log_format))
    handler.setLevel(logging.DEBUG)
    root_logger.addHandler(handler)

    asyncio.run(main())
