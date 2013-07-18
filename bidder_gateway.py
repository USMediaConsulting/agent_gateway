import sys
from bottle import Bottle, run, urljoin, HTTPResponse, request

# create the bottle app so we don't use the global one
app = Bottle()
# initialize bidder map
bidders = {}

@app.get('/test_redirect')
def do_redirection():
    location = urljoin('http://127.0.0.1:9985', '/v1/accounts/nemi')
    raise HTTPResponse("", status=302, Location=location)

@app.post('/v1/agents/<name>/start')
def start_bidder(name):
    """
        Starts up a bidder using as the instance parameters
        the arguments passed in the query string 
    """ 
    print 'starting up bidder %s' % name
    result = {
            'resultCode'        :   0,
            'resultDescription' :   'ok'
    }

    if name in bidders :
        result['result_code'] = 1
        result['resultDescription'] = 'bidder already started'    
        return result
    else :
        bidders[name] = {}

    #TODO : execute the bidder instance
    #TODO : save the pid for the new bidder
    bidders[name]['pid']  = 8888
    bidders[name]['bidder_name'] = request.query['bidder_name']  
    bidders[name]['params'] = {
         k:v for k,v in request.query.iteritems() if k != 'bidder_name' 
    }
    bidders[name]['agent_conf_name'] = \
        '%s_%s' % (bidders[name]['bidder_name'], bidders[name]['pid'])

    return result
    

if __name__ == '__main__' :
    print '---- BIDDER GATEWAY ----'
    run(app, host='localhost', port=8080, reloader=True)
    sys.exit(0)
