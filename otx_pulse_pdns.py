from recon.core.module import BaseModule

class Module(BaseModule):

    meta = {
        'name': 'OTX Pulse Enumerator',
        'author': 'j nazario (@jnazario)',
        'description': 'Leverages the OTX Pulse API to enumerate other virtual hosts sharing the same IP address. Updates the \'hosts\' and \'domains\' table with the results.',
        'query': 'SELECT DISTINCT host FROM hosts WHERE host IS NOT NULL',
    }

    def module_run(self, hosts):
        for host in hosts:
            self.heading(host, level=0)
            url = 'https://otx.alienvault.com/api/v1/indicators/hostname/{0}/passive_dns'.format(host)
            resp = self.request(url)
            jsonobj = resp.json
            for address in [x['address'] for x in jsonobj['passive_dns']]:
                self.add_hosts(host, address)
                self.output('\'%s\' successfully found.' % (address))
