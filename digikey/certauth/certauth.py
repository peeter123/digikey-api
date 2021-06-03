import logging
import os

from io import BytesIO

from OpenSSL import crypto
from OpenSSL.SSL import FILETYPE_PEM

import random

import ipaddress
import tldextract

from argparse import ArgumentParser

from collections import OrderedDict

import threading

# =================================================================
# Valid for 3 years from now
# Max validity is 39 months:
# https://casecurity.org/2015/02/19/ssl-certificate-validity-periods-limited-to-39-months-starting-in-april/
CERT_NOT_AFTER = 3 * 365 * 24 * 60 * 60

CERTS_DIR = './ca/certs/'

CERT_NAME = 'certauth sample CA'

DEF_HASH_FUNC = 'sha256'

ROOT_CA = '!!root_ca'


# =================================================================
class CertificateAuthority(object):
    """
    Utility class for signing individual certificate
    with a root cert.

    Static generate_ca_root() method for creating the root cert

    All certs saved on filesystem. Individual certs are stored
    in specified certs_dir and reused if previously created.
    """

    def __init__(self, ca_name,
                 ca_file_cache,
                 cert_cache=None,
                 cert_not_before=0,
                 cert_not_after=CERT_NOT_AFTER,
                 overwrite=False):

        if isinstance(ca_file_cache, str):
            self.ca_file_cache = RootCACache(ca_file_cache)
        else:
            self.ca_file_cache = ca_file_cache

        if isinstance(cert_cache, str):
            self.cert_cache = FileCache(cert_cache)
        elif isinstance(cert_cache, int):
            self.cert_cache = LRUCache(max_size=cert_cache)
        elif cert_cache is None:
            self.cert_cache = LRUCache(max_size=100)
        else:
            self.cert_cache = cert_cache

        self.ca_name = ca_name

        self.cert_not_before = cert_not_before
        self.cert_not_after = cert_not_after

        res = self.load_root_ca_cert(overwrite=overwrite)
        self.ca_cert, self.ca_key = res

    def load_root_ca_cert(self, overwrite=False):
        cert_str = None

        if not overwrite:
            cert_str = self.ca_file_cache.get(ROOT_CA)

        # if cached, just read pem
        if cert_str:
            cert, key = self.read_pem(BytesIO(cert_str))

        else:
            cert, key = self.generate_ca_root(self.ca_name)

            # Write cert + key
            buff = BytesIO()
            self.write_pem(buff, cert, key)
            cert_str = buff.getvalue()

            # store cert in cache
            self.ca_file_cache[ROOT_CA] = cert_str

        return cert, key

    def is_host_ip(self, host):
        try:
            # if py2.7, need to decode to unicode str
            if hasattr(host, 'decode'):  #pragma: no cover
                host = host.decode('ascii')

            ipaddress.ip_address(host)
            return True
        except (ValueError, UnicodeDecodeError) as e:
            return False

    def get_wildcard_domain(self, host):
        host_parts = host.split('.', 1)
        if len(host_parts) < 2 or '.' not in host_parts[1]:
            return host

        ext = tldextract.extract(host)

        # allow using parent domain if:
        # 1) no suffix (unknown tld)
        # 2) the parent domain contains 'domain.suffix', not just .suffix
        if not ext.suffix or ext.domain + '.' + ext.suffix in host_parts[1]:
            return host_parts[1]

        return host

    def load_cert(self, host, overwrite=False,
                              wildcard=False,
                              wildcard_use_parent=False,
                              include_cache_key=False):

        is_ip = self.is_host_ip(host)

        if is_ip:
            wildcard = False

        if wildcard and wildcard_use_parent:
            host = self.get_wildcard_domain(host)

        cert_str = None

        if not overwrite:
            cert_str = self.cert_cache.get(host)

        # if cached, just read pem
        if cert_str:
            cert, key = self.read_pem(BytesIO(cert_str))

        else:
            # if not cached, generate new root or host cert
            cert, key = self.generate_host_cert(host,
                                                self.ca_cert,
                                                self.ca_key,
                                                wildcard,
                                                is_ip=is_ip)

            # Write cert + key
            buff = BytesIO()
            self.write_pem(buff, cert, key)
            cert_str = buff.getvalue()

            # store cert in cache
            self.cert_cache[host] = cert_str

        if not include_cache_key:
            return cert, key

        else:
            cache_key = host
            if hasattr(self.cert_cache, 'key_for_host'):
                cache_key = self.cert_cache.key_for_host(host)

            return cert, key, cache_key

    def cert_for_host(self, host, overwrite=False,
                                  wildcard=False):

        res = self.load_cert(host, overwrite=overwrite,
                                   wildcard=wildcard,
                                   wildcard_use_parent=False,
                                   include_cache_key=True)

        return res[2]



    def get_wildcard_cert(self, cert_host, overwrite=False):
        res = self.load_cert(cert_host, overwrite=overwrite,
                                        wildcard=True,
                                        wildcard_use_parent=True,
                                        include_cache_key=True)

        return res[2]

    def get_root_PKCS12(self):
        p12 = crypto.PKCS12()
        p12.set_certificate(self.ca_cert)
        p12.set_privatekey(self.ca_key)
        return p12.export()

    def get_root_pem(self):
        return self.ca_file_cache.get(ROOT_CA)

    def get_root_pem_filename(self):
        return self.ca_file_cache.ca_file

    def _make_cert(self, certname):
        cert = crypto.X509()
        cert.set_serial_number(random.randint(0, 2 ** 64 - 1))
        cert.get_subject().CN = certname

        cert.set_version(2)
        cert.gmtime_adj_notBefore(self.cert_not_before)
        cert.gmtime_adj_notAfter(self.cert_not_after)
        return cert

    def generate_ca_root(self, ca_name, hash_func=DEF_HASH_FUNC):
        # Generate key
        key = crypto.PKey()
        key.generate_key(crypto.TYPE_RSA, 2048)

        # Generate cert
        cert = self._make_cert(ca_name)

        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(key)
        cert.add_extensions([
            crypto.X509Extension(b"basicConstraints",
                                 True,
                                 b"CA:TRUE, pathlen:0"),

            crypto.X509Extension(b"keyUsage",
                                 True,
                                 b"keyCertSign, cRLSign"),

            crypto.X509Extension(b"subjectKeyIdentifier",
                                 False,
                                 b"hash",
                                 subject=cert),
            ])
        cert.sign(key, hash_func)

        return cert, key

    def generate_host_cert(self, host, root_cert, root_key,
                           wildcard=False,
                           hash_func=DEF_HASH_FUNC,
                           is_ip=False):

        host = host.encode('utf-8')

        # Generate key
        key = crypto.PKey()
        key.generate_key(crypto.TYPE_RSA, 2048)

        # Generate CSR
        req = crypto.X509Req()
        req.get_subject().CN = host
        req.set_pubkey(key)
        req.sign(key, hash_func)

        # Generate Cert
        cert = self._make_cert(host)

        cert.set_issuer(root_cert.get_subject())
        cert.set_pubkey(req.get_pubkey())

        primary = b'DNS:' + host

        if wildcard:
            alt_hosts = primary + b', DNS:*.' + host

        elif is_ip:
            alt_hosts = b'IP:' + host + b', ' + primary

        else:
            alt_hosts = primary

        cert.add_extensions([
            crypto.X509Extension(b'subjectAltName',
                                 False,
                                 alt_hosts)])

        cert.sign(root_key, hash_func)
        return cert, key

    def write_pem(self, buff, cert, key):
        buff.write(crypto.dump_privatekey(FILETYPE_PEM, key))
        buff.write(crypto.dump_certificate(FILETYPE_PEM, cert))

    def read_pem(self, buff):
        cert = crypto.load_certificate(FILETYPE_PEM, buff.read())
        buff.seek(0)
        key = crypto.load_privatekey(FILETYPE_PEM, buff.read())
        return cert, key


# =================================================================
class FileCache(object):
    def __init__(self, certs_dir):
        self._lock = threading.Lock()
        self.certs_dir = certs_dir
        self.modified = False

        if self.certs_dir and not os.path.exists(self.certs_dir):
            os.makedirs(self.certs_dir)

    def key_for_host(self, host):
        host = host.replace(':', '-')
        return os.path.join(self.certs_dir, host) + '.pem'

    def __setitem__(self, host, cert_string):
        filename = self.key_for_host(host)
        with self._lock:
            with open(filename, 'wb') as fh:
                fh.write(cert_string)
                self.modified = True

    def get(self, host):
        filename = self.key_for_host(host)
        try:
            with open(filename, 'rb') as fh:
                return fh.read()
        except:
            return b''


# =================================================================
class RootCACache(FileCache):
    def __init__(self, ca_file):
        self.ca_file = ca_file
        ca_dir = os.path.dirname(ca_file) or '.'
        super(RootCACache, self).__init__(ca_dir)

    def key_for_host(self, host=None):
        return self.ca_file


# =================================================================
class LRUCache(OrderedDict):
    def __init__(self, max_size):
        super(LRUCache, self).__init__()
        self.max_size = max_size

    def __setitem__(self, host, cert_string):
        super(LRUCache, self).__setitem__(host, cert_string)
        if len(self) > self.max_size:
            self.popitem(last=False)


# =================================================================
def main(args=None):
    parser = ArgumentParser(description='Certificate Authority Cert Maker Tools')

    parser.add_argument('root_ca_cert',
                        help='Path to existing or new root CA file')

    parser.add_argument('-c', '--certname', action='store', default=CERT_NAME,
                        help='Name for root certificate')

    parser.add_argument('-n', '--hostname',
                        help='Hostname certificate to create')

    parser.add_argument('-d', '--certs-dir', default=CERTS_DIR,
                        help='Directory for host certificates')

    parser.add_argument('-f', '--force', action='store_true',
                        help='Overwrite certificates if they already exist')

    parser.add_argument('-w', '--wildcard_cert', action='store_true',
                        help='add wildcard SAN to host: *.<host>, <host>')

    r = parser.parse_args(args=args)

    certs_dir = r.certs_dir
    wildcard = r.wildcard_cert

    root_cert = r.root_ca_cert
    hostname = r.hostname

    if not hostname:
        overwrite = r.force
    else:
        overwrite = False

    cert_cache = FileCache(r.certs_dir)
    ca_file_cache = RootCACache(root_cert)

    ca = CertificateAuthority(ca_name=r.certname,
                              ca_file_cache=ca_file_cache,
                              cert_cache=cert_cache,
                              overwrite=overwrite)

    # Just creating the root cert
    if not hostname:
        if ca_file_cache.modified:
            print('Created new root cert: "' + root_cert + '"')
            return 0
        else:
            print('Root cert "' + root_cert +
                  '" already exists,' + ' use -f to overwrite')
            return 1

    # Sign a certificate for a given host
    overwrite = r.force
    ca.load_cert(hostname, overwrite=overwrite,
                           wildcard=wildcard,
                           wildcard_use_parent=False)

    if cert_cache.modified:
        print('Created new cert "' + hostname +
              '" signed by root cert ' +
              root_cert)
        return 0

    else:
        print('Cert for "' + hostname + '" already exists,' +
              ' use -f to overwrite')
        return 1


if __name__ == "__main__":  #pragma: no cover
    main()
