import jqdatasdk as jq
from .utils import clean_up_otc_netvalues, update_local_net_values

def generate_report():
    
    clean_up_otc_netvalues()
    update_local_net_values()