import sys
import os
import logging
import pickle

from bottle import Bottle, run, urljoin, HTTPResponse, request

# agent pickle file path
pickle_path = '.bidders'

# set up logging
logging.basicConfig(filename='bidder_gateway.log',
        format='%(asctime)-15s %(levelname)s %(message)s', 
        level=logging.DEBUG)
logger = logging.getLogger('bidder_gateway')

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

    # save the executable name
    bidders[name]['bidder_name'] = request.query['bidder_name']
    bidders[name]['executable'] = request.query['executable']  
    # save the params    
    bidders[name]['params'] = {
         k:v for k,v in request.query.iteritems() 
            if k not in ('bidder_name', 'executable') 
    }
    
    logger.info('bringing up bidder %s=%s' % (name, bidders[name]))

    #TODO : execute the bidder instance
    #TODO : save the pid for the new bidder
    bidders[name]['pid']  = 8888
   
    # the key stored by the agent configuration service
    # is a concatenation of the bidder name passed and the
    # pid for for process 
    bidders[name]['agent_conf_name'] = \
        '%s_%s' % (bidders[name]['bidder_name'], bidders[name]['pid'])
    logger.info('bidder %s got pid %d' % (name, bidders[name]['pid']))
    
    # great, let's pickle the data
    try :    
        f = open(os.path.join(pickle_path, str(bidders[name]['pid'])), 'w')    
        pickle.dump(bidders[name], f)
        f.close()
    except :
        result['resultCode'] = 2
        result['resultDescription'] = 'unable to pickle configuration'

    return result
    

if __name__ == '__main__' :
    logger.warning('starting up server')
    run(app, host='localhost', port=8080, reloader=True)
    sys.exit(0)
