'''
Validator
'''
import re, os
import logging
from tidylib import tidy_fragment
logger = logging.getLogger('strings')

SKIP_HTML_VALIDATION = False
if os.environ.get('SKIP_HTML_VALIDATION'):
    SKIP_HTML_VALIDATION = os.environ.get('SKIP_HTML_VALIDATION') \
    in ['true', '1', 'yes', 'Yes', 'YES', 'True', 'TRUE']

'''
DOC: Precompile regular expression for search, replace
'''
# regular expression for white space
REG_WHITESPACE = re.compile(r'\s+')
# regular expression for html escaped characters
REG_HTML_ESCAPED_AMP = re.compile('&amp;')
REG_HTML_ESCAPED_GRT = re.compile('&gt;')
REG_HTML_ESCAPED_LST = re.compile('&lt;')
# regular expression for carriage return
REG_CARRIAGE_RETURN = re.compile('[\r\n]')

def validate_texts(item):
    '''
    Provide fail/success with parsed
    '''
    fail = []
    success = []
    for key in item:
        if key == 'key':
            continue
        # logger.info('Parsing {}'.format(key))
        parsed = is_valid_text(item[key])
        if parsed['isValid']:
            success.append({'field': key, 'imported':item[key], 'parsed':parsed})
        else:
            fail.append({'field': key, 'imported': item[key], 'parsed': parsed})
    return {'fail': fail, 'success': success}

def is_valid_text(text):
    '''
    1. is this valid HTML fragment?
    '''
    results = {
        'origin': text,
        'parsed': text,
        'isValid': True,
        'errorMessage': None,
    }
    '''
    DOC: Option to skip HTML VALIDATION
    '''
    if SKIP_HTML_VALIDATION:
        return results
    if REG_CARRIAGE_RETURN.search(text) is not None:
        results['errorMessage'] = 'Translation should not contains new line character.'
        results['isValid'] = False
        return results
    # convert to html using tidy
    results['parsed'], error = tidy_fragment(text, {
        'indent': 0,
        'break-before-br': False,
        'uppercase-attributes': False,
        'show-warnings': False,
        'output-html': False
    })
    # logger.info('Parsed data: "%s"' % parsed)
    if error:
        results['isValid'] = False
        return results
    cleaned_parsed = results['parsed'].lower()
    cleaned_text = results['origin'].lower()
    cleaned_text = REG_WHITESPACE.sub('', cleaned_text)
    cleaned_parsed = REG_WHITESPACE.sub('', cleaned_parsed)
    # revert escaped characters
    cleaned_parsed = REG_HTML_ESCAPED_AMP.sub('&', cleaned_parsed)
    cleaned_parsed = REG_HTML_ESCAPED_GRT.sub('>', cleaned_parsed)
    cleaned_parsed = REG_HTML_ESCAPED_LST.sub('<', cleaned_parsed)
    # compare
    logger.debug('Origin data: "%s"' % text)
    logger.debug('Parsed data: "%s"' % results['parsed'])
    if cleaned_parsed != cleaned_text:
        results['errorMessage'] = 'Parsed String is not same as original'
        results['isValid'] = False
        return results
    return results

def validateHTMLFragment(fragment):
    if fragment == '':
        return '', 'Empty String'
    result = is_valid_text(fragment)
    if result.get('isValid'):
        return result.get('parsed'), None
    return result.get('parsed'), "%s - %s" % (result.get('errorMessage'), result.get('parsed'))
