import re


class HostUtils(object):

    @classmethod
    def host_selectors(self, all_selectors, host):
        if host is None:
            return None

        host = host.replace("www.", "")    

        if host in all_selectors:
            selectors = all_selectors[host]
            if type(selectors) is dict:
                selectors = all_selectors[selectors['reference']]
            return selectors

        # for regex_string in all_selectors['regexs_references']:
        #     match_data = re.compile(regex_string).search(host)
        #     if match_data:
        #         reference_host = all_selectors['regexs_references'][regex_string]['reference']
        #         return all_selectors[reference_host]
