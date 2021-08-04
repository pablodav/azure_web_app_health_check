#!python3
# https://nagios-plugins.org/doc/guidelines.html

# Import required libs
from .plugin_check import curlCheck
from .azure_web_app_health_check import AzureAppHealthChecks
import argparse
import sys


# Return codes expected by Nagios
OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3

# Return message
message = {
    'status': OK,
    'summary': 'Example summary',
    'perfdata': 'label1=0;;;; '  # 'label'=value[UOM];[warn];[crit];[min];[max] 
}

# For multiple perdata, ensure to add space after each perfdata
# message['perfdata'] = 'label1=x;;;; '
# message['perfdata'] += 'label2=x;;;; '

# Function to parse arguments
def parse_args(args):
    """
    Information extracted from: https://mkaz.com/2014/07/26/python-argparse-cookbook/
     https://docs.python.org/3/library/argparse.html
    :return: parse.parse_args(args) object
    You can use obj.option, example:
    options = parse_args(args)
    options.user # to read username
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, 
                                     description='nagios plugin to check some url using curl and some other code')

    parser.add_argument('-u', '--url', dest='url', nargs='?', default=None, const=None,
                        help='url to check \n')
    parser.add_argument('-k', '--key', dest='key', nargs='?', default=None, const=None,
                        help='key to access to azure app \n')                    
    parser.add_argument('-e', '--extra_args', dest='extra_args', nargs='?', default='', const=None,
                            help='extra args to add to curl, see curl manpage  \n')
    
    if not args:
        raise SystemExit(parser.print_help())

    return parser.parse_args(args)

# Function to execute cli commands
def cli_execution(options):
    """
    : param: options: arguments from parse.parse_args(args) (see parse_args function)
    """
    
    #Create azure health object    
    azure_healt_obj = AzureAppHealthChecks(url=options.url, key=options.key)

    def collect_data():        
        retrcode, msgdata = azure_healt_obj.check_status_data()
        return retrcode, msgdata
    
    def check(retrcode):
        if retrcode >= 2:
            status = CRITICAL
            message['summary'] = 'CRITICAL: '            
        elif retrcode == 1:
            status = WARNING
            message['summary'] = 'WARNING: '
        else:
            status = OK
            message['summary'] = 'OK: '
        return status
        
   
    # Check logic starts here
    data = collect_data()
    message['status'] = check(data[0])
    # Add summary       
    message['summary'] += data[1]
    # Add perfdata
    # total = len(data)
    #message['perfdata'] = curlnagiosobj.format_perfdata()    
    # Print the message
    # Print the message
    
    print("{summary}".format(
        summary=message.get('summary')
    ))
    # Exit with status code
    raise SystemExit(message['status'])

# Argument parser
# https://docs.python.org/3.5/library/argparse.html

def main():
    """
    Main function
    """
    # Get options with argparse
    options = parse_args(sys.argv[1:])
    # Execute program functions passing the options collected
    cli_execution(options)


if __name__ == "__main__":
    main()
