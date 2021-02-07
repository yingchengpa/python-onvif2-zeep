from onvif2.client import ONVIFService, ONVIFCamera, SERVICES
from onvif2.exceptions import ONVIFError, ERR_ONVIF_UNKNOWN, \
        ERR_ONVIF_PROTOCOL, ERR_ONVIF_WSDL, ERR_ONVIF_BUILD
#from onvif2 import cli

__all__ = ( 'ONVIFService', 'ONVIFCamera', 'ONVIFError',
            'ERR_ONVIF_UNKNOWN', 'ERR_ONVIF_PROTOCOL',
            'ERR_ONVIF_WSDL', 'ERR_ONVIF_BUILD',
            'SERVICES'#, 'cli'
           )
