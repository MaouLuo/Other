# RFC 2822 - style email validation for Python
# (c) 2012 Syrus Akbary <me@syrusakbary.com>
# Extended from (c) 2011 Noel Bush <noel@aitools.org>
# for support of mx and user check
# This code is made available to you under the GNU LGPL v3.
#
# This module provides a single method, valid_email_address(),
# which returns True or False to indicate whether a given address
# is valid according to the 'addr-spec' part of the specification
# given in RFC 2822.  Ideally, we would like to find this
# in some other library, already thoroughly tested and well-
# maintained.  The standard Python library email.utils
# contains a parse_addr() function, but it is not sufficient
# to detect many malformed addresses.
#
# This implementation aims to be faithful to the RFC, with the
# exception of a circular definition (see comments below), and
# with the omission of the pattern components marked as "obsolete".

# pip insatall validate_email
# pip insatall py3dns

import re
import smtplib
import logging
import socket
import sys

import cloudmersive_validate_api_client
from cloudmersive_validate_api_client.rest import ApiException

try:
    raw_input
except NameError:
    def raw_input(prompt=''):
        return input(prompt)

try:
    import DNS
    ServerError = DNS.ServerError
    DNS.DiscoverNameServers()
except (ImportError, AttributeError):
    DNS = None

    class ServerError(Exception):
        pass

# All we are really doing is comparing the input string to one
# gigantic regular expression.  But building that regexp, and
# ensuring its correctness, is made much easier by assembling it
# from the "tokens" defined by the RFC.  Each of these tokens is
# tested in the accompanying unit test file.
#
# The section of RFC 2822 from which each pattern component is
# derived is given in an accompanying comment.
#
# (To make things simple, every string below is given as 'raw',
# even when it's not strictly necessary.  This way we don't forget
# when it is necessary.)
#
WSP = r'[ \t]'                                       # see 2.2.2. Structured Header Field Bodies
CRLF = r'(?:\r\n)'                                   # see 2.2.3. Long Header Fields
NO_WS_CTL = r'\x01-\x08\x0b\x0c\x0f-\x1f\x7f'        # see 3.2.1. Primitive Tokens
QUOTED_PAIR = r'(?:\\.)'                             # see 3.2.2. Quoted characters
FWS = r'(?:(?:' + WSP + r'*' + CRLF + r')?' + \
      WSP + r'+)'                                    # see 3.2.3. Folding white space and comments
CTEXT = r'[' + NO_WS_CTL + \
        r'\x21-\x27\x2a-\x5b\x5d-\x7e]'              # see 3.2.3
CCONTENT = r'(?:' + CTEXT + r'|' + \
           QUOTED_PAIR + r')'                        # see 3.2.3 (NB: The RFC includes COMMENT here
# as well, but that would be circular.)
COMMENT = r'\((?:' + FWS + r'?' + CCONTENT + \
          r')*' + FWS + r'?\)'                       # see 3.2.3
CFWS = r'(?:' + FWS + r'?' + COMMENT + ')*(?:' + \
       FWS + '?' + COMMENT + '|' + FWS + ')'         # see 3.2.3
ATEXT = r'[\w!#$%&\'\*\+\-/=\?\^`\{\|\}~]'           # see 3.2.4. Atom
ATOM = CFWS + r'?' + ATEXT + r'+' + CFWS + r'?'      # see 3.2.4
DOT_ATOM_TEXT = ATEXT + r'+(?:\.' + ATEXT + r'+)*'   # see 3.2.4
DOT_ATOM = CFWS + r'?' + DOT_ATOM_TEXT + CFWS + r'?' # see 3.2.4
QTEXT = r'[' + NO_WS_CTL + \
        r'\x21\x23-\x5b\x5d-\x7e]'                   # see 3.2.5. Quoted strings
QCONTENT = r'(?:' + QTEXT + r'|' + \
           QUOTED_PAIR + r')'                        # see 3.2.5
QUOTED_STRING = CFWS + r'?' + r'"(?:' + FWS + \
                r'?' + QCONTENT + r')*' + FWS + \
                r'?' + r'"' + CFWS + r'?'
LOCAL_PART = r'(?:' + DOT_ATOM + r'|' + \
             QUOTED_STRING + r')'                    # see 3.4.1. Addr-spec specification
DTEXT = r'[' + NO_WS_CTL + r'\x21-\x5a\x5e-\x7e]'    # see 3.4.1
DCONTENT = r'(?:' + DTEXT + r'|' + \
           QUOTED_PAIR + r')'                        # see 3.4.1
DOMAIN_LITERAL = CFWS + r'?' + r'\[' + \
                 r'(?:' + FWS + r'?' + DCONTENT + \
                 r')*' + FWS + r'?\]' + CFWS + r'?'  # see 3.4.1
DOMAIN = r'(?:' + DOT_ATOM + r'|' + \
         DOMAIN_LITERAL + r')'                       # see 3.4.1
ADDR_SPEC = LOCAL_PART + r'@' + DOMAIN               # see 3.4.1

# A valid address will match exactly the 3.4.1 addr-spec.
VALID_ADDRESS_REGEXP = '^' + ADDR_SPEC + '$'

MX_DNS_CACHE = {}
MX_CHECK_CACHE = {}


def get_mx_ip(hostname):
    if hostname not in MX_DNS_CACHE:
        try:
            MX_DNS_CACHE[hostname] = DNS.mxlookup(hostname)
        except ServerError as e:
            if e.rcode == 3:  # NXDOMAIN (Non-Existent Domain)
                MX_DNS_CACHE[hostname] = None
            else:
                raise

    return MX_DNS_CACHE[hostname]


def validate_email(email, check_mx=False, verify=False, debug=False, smtp_timeout=10):
    """Indicate whether the given string is a valid email address
    according to the 'addr-spec' portion of RFC 2822 (see section
    3.4.1).  Parts of the spec that are marked obsolete are *not*
    included in this test, and certain arcane constructions that
    depend on circular definitions in the spec may not pass, but in
    general this should correctly identify any email address likely
    to be in use as of 2011."""
    if debug:
        logger = logging.getLogger('validate_email')
        logger.setLevel(logging.DEBUG)
    else:
        logger = None

    try:
        assert re.match(VALID_ADDRESS_REGEXP, email) is not None
        check_mx |= verify
        if check_mx:
            if not DNS:
                raise Exception('For check the mx records or check if the email exists you must '
                                'have installed pyDNS python package')
            hostname = email[email.find('@') + 1:]
            mx_hosts = get_mx_ip(hostname)
            if mx_hosts is None:
                return False
            for mx in mx_hosts:
                try:
                    if not verify and mx[1] in MX_CHECK_CACHE:
                        return MX_CHECK_CACHE[mx[1]]
                    smtp = smtplib.SMTP(timeout=smtp_timeout)
                    smtp.connect(mx[1])
                    MX_CHECK_CACHE[mx[1]] = True
                    if not verify:
                        try:
                            smtp.quit()
                        except smtplib.SMTPServerDisconnected:
                            pass
                        return True
                    status, _ = smtp.helo()
                    if status != 250:
                        smtp.quit()
                        if debug:
                            logger.debug(u'%s answer: %s - %s', mx[1], status, _)
                        continue
                    smtp.mail('')
                    status, _ = smtp.rcpt(email)
                    if status == 250:
                        smtp.quit()
                        return True
                    if debug:
                        logger.debug(u'%s answer: %s - %s', mx[1], status, _)
                    smtp.quit()
                except smtplib.SMTPServerDisconnected:  # Server not permits verify user
                    if debug:
                        logger.debug(u'%s disconected.', mx[1])
                except smtplib.SMTPConnectError:
                    if debug:
                        logger.debug(u'Unable to connect to %s.', mx[1])
            return None
    except AssertionError:
        return False
    except (ServerError, socket.error) as e:
        if debug:
            logger.debug('ServerError or socket.error exception raised (%s).', e)
        return None
    return True

def progress(percent,width=50):
    '''进度打印功能'''
    if percent >= 100:
        percent=100
  
    show_str=('[%%-%ds]' %width) %(int(width * percent/100)*"#") #字符串拼接的嵌套使用
    print('\r%s %d%%' %(show_str,percent))

def progress_run(MaxNum):
    data_size = MaxNum #定义传输的数据，实际应用中这个值改一下就可以了
    recv_size=0
    while recv_size < data_size:
        #time.sleep(0.1) #模拟数据的传输延迟
        recv_size+=1 #每次收1024
      
        recv_per=int(100*recv_size/data_size) #接收的比例
        progress(recv_per,width=30) #调用进度条函数，进度条的宽度默认设置为30

def single_validate(email):
    #while True:
        #email = raw_input('Enter email for validation: ')
    logging.basicConfig()
    result = validate_email(email, True, True, debug=False, smtp_timeout=1)
    if result:
        #print("{0} Valid.".format(email))
        resu = 'Valid'
    elif result is None:
        #print("{0} Not sure.".format(email))
        resu = 'Not sure'
    else:
        #print("{0} Invalid.".format(email))
        resu = 'Invalid'

    return {email:resu}

    '''
    dic = {'a':1, 'b':12, 'c':11, 'd':21}

	for k,v in dic.items():
		print('key:{0}, v:{1}'.format(k,v)) 
		'''

def cloudmersive_init():
    # Configure API key authorization: Apikey
    configuration = cloudmersive_validate_api_client.Configuration()
    configuration.api_key['Apikey'] = 'a7fa4e04-df08-4b69-a5f1-fcd1dbc34b88'
    # Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
    # configuration.api_key_prefix['Apikey'] = 'Bearer'

    # create an instance of the API class
    api_instance = cloudmersive_validate_api_client.EmailApi(cloudmersive_validate_api_client.ApiClient(configuration))
    #email = 'lhough@arizonatile.com' # str | Email address to validate, e.g. \"support@cloudmersive.com\".    The input is a string so be sure to enclose it in double-quotes.

    return api_instance


def cloudmersive_api(email, api_instance):
    try:
        # Fully validate an email address
        api_response = api_instance.email_full_validation(email)
        # api_response = api_instance.email_address_get_servers(email)
        #print(api_response.valid_address)
        return {email:api_response.valid_address}

    except ApiException as e:
        print("Exception when calling EmailApi->email_full_validation: %s\n" % e)


def r_ex(path):
	df = pd.read_excel(path)
	emails = []
	for v in df.loc[:,'email']:
		emails.append(v)
	#df.shape[0]或len(df)显示总行数，df.shape[1]显示总列数
	return emails 


def w_ex(emails, valid):
	df = pd.DataFrame({'email':emails, 'valid':valid})
	df.to_excel('validited.xlsx')
	return True


def main(path):    
    emails_c = {}
    addr = []
    val = []
    emails_o = r_ex(path)
    print('已读取所有邮箱')
    #print(sys.getsizeof(emails_o))
    #return
    
    starttime = time.time()
    data_size = len(emails_o)
    recv_size=0
    api_instance = cloudmersive_init()

    try:
        for e in emails_o:
        	#email_c = single_validate(e)        
            email_c = cloudmersive_api(e, api_instance)
            emails_c.update(email_c)
            recv_size+=1 #每次收1024
            recv_per=int(100*recv_size/data_size) #接收的比例
            progress(recv_per,width=30) #调用进度条函数，进度条的宽度默认设置为30
            time.sleep(10)
    
    finally:	    
        endtime = time.time()
        print('校验完成，耗时：%.2s s，开始生成文件' % (endtime-starttime))

        for k,v in emails_c.items():
            addr.append(k)
            val.append(v)

        #print('addr:{0}'.format(addr))
        #print('val:{0}'.format(val))

        w_ex(addr, val)
        print('已生成文件：validited.xlsx')

    return



if __name__ == "__main__":
    import time
    import pandas as pd

    path = input('input your excel path:')
    main(path)
    


# import sys

# sys.modules[__name__],sys.modules['validate_email_module'] = validate_email,sys.modules[__name__]
# from validate_email_module import *
