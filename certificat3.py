# -*- encoding: utf-8 -*-
# requires a recent enough python with idna support in socket
# pyopenssl, cryptography and idna

from OpenSSL import SSL
import cryptography
from cryptography import x509
from cryptography.x509.oid import NameOID
import idna
import concurrent.futures

from socket import socket
from collections import namedtuple

HostInfo = namedtuple(field_names='cert hostname peername', typename='HostInfo')

HOSTS = [
    ('damjan.softver.org.mk', 443),
    ('expired.badssl.com', 443),
    ('wrong.host.badssl.com', 443),
    ('echange.asp-public.fr', 443),
]


def verify_cert(cert, hostname):
    # verify notAfter/notBefore, CA trusted, servername/sni/hostname
    cert.has_expired()
    # service_identity.pyopenssl.verify_hostname(client_ssl, hostname)
    # issuer


def get_certificate(hostname, port):
    hostname_idna = idna.encode(hostname)
    sock = socket()

    sock.connect((hostname, port))
    peername = sock.getpeername()
    ctx = SSL.Context(SSL.SSLv23_METHOD)  # most compatible
    ctx.check_hostname = False
    ctx.verify_mode = SSL.VERIFY_NONE

    sock_ssl = SSL.Connection(ctx, sock)
    sock_ssl.set_connect_state()
    sock_ssl.set_tlsext_host_name(hostname_idna)
    sock_ssl.do_handshake()
    cert = sock_ssl.get_peer_certificate()
    crypto_cert = cert.to_cryptography()
    sock_ssl.close()
    sock.close()

    return HostInfo(cert=crypto_cert, peername=peername, hostname=hostname)


def get_alt_names(cert):
    try:
        ext = cert.extensions.get_extension_for_class(x509.SubjectAlternativeName)
        return ext.value.get_values_for_type(x509.DNSName)
    except x509.ExtensionNotFound:
        return None


def get_common_name(cert):
    try:
        names = cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)
        return names[0].value
    except x509.ExtensionNotFound:
        return None


def get_issuer(cert):
    try:
        names = cert.issuer.get_attributes_for_oid(NameOID.COMMON_NAME)
        return names[0].value
    except x509.ExtensionNotFound:
        return None


def print_extensions(extensions):
    space = " " * 3
    for certificat in extensions:
        print(space, f"- {str(certificat.critical):5}", end=", ")

        print(space, f"{certificat.oid._name:30}", end=" = ")
        print(space, certificat.oid.dotted_string)

        if hasattr(certificat.value, "__iter__"):
            for cert in certificat.value:

                if type(cert) is cryptography.hazmat.bindings._rust.ObjectIdentifier:
                    if hasattr(cert, "dotted_string"):
                        print(space, "    * dotted_string:", cert.dotted_string)

                elif type(cert) is cryptography.x509.extensions.DistributionPoint:
                    if hasattr(cert, "full_name"):
                        print(space, "    * full_name: ", end="")
                        for name in cert.full_name:
                            print(name.value, end=", ")
                        print()

                elif type(cert) is cryptography.x509.extensions.AccessDescription:            
                    if hasattr(cert, "access_location"):
                        print(space, "    * access_location:", cert.access_location.value)
                    if hasattr(cert, "access_method"):
                        print(space, "    * access_method:", cert.access_method._name, "=", cert.access_method.dotted_string)

                elif type(cert) is cryptography.x509.general_name.DNSName:
                    if hasattr(cert, "value"):
                        print(space, "    * value:", cert.value)

                elif type(cert) is cryptography.x509.extensions.PolicyInformation:
                    if hasattr(cert, "policy_identifier"):
                        print(space, "    * policy_identifier:", cert.policy_identifier._name, "=", cert.policy_identifier.dotted_string)
                    if hasattr(cert, "policy_qualifiers"):
                        print(space, "    * policy_qualifiers:", cert.policy_qualifiers)

                elif type(cert) is cryptography.hazmat.bindings._rust.x509.Sct:
                    print(space, "   [", cert.signature_algorithm, end=", ")
                    print(cert.signature_hash_algorithm.name, "]")
                    if hasattr(cert, "entry_type"):
                        print(space, "    * entry_type:", cert.entry_type)
                    if hasattr(cert, "extension_bytes"):
                        print(space, "    * extension_bytes:", cert.extension_bytes)
                    if hasattr(cert, "log_id"):
                        print(space, "    * log_id:", cert.log_id)
                    if hasattr(cert, "timestamp"):
                        print(space, "    * timestamp:", cert.timestamp)
                    if hasattr(cert, "version"):
                        print(space, "    * version:", cert.version)
                else:
                    raise TypeError("type de certificat inconnu:", type(cert))

        else:
            print(space, "    * value:", certificat.value)
            print(space, "    * oid:", certificat.oid._name, "=", certificat.oid.dotted_string)

    print()


def print_basic_info(hostinfo):
    s = '''> {hostname} ... {peername}
    commonName: {commonname}
    SAN: {SAN}
    issuer: {issuer}
    notBefore: {notbefore}
    notAfter:  {notafter}
    Extensions:'''.format(
            hostname=hostinfo.hostname,
            peername=hostinfo.peername,
            commonname=get_common_name(hostinfo.cert),
            SAN=get_alt_names(hostinfo.cert),
            issuer=get_issuer(hostinfo.cert),
            notbefore=hostinfo.cert.not_valid_before_utc,
            notafter=hostinfo.cert.not_valid_after_utc
    )
    print(s, flush=True)
    print_extensions(hostinfo.cert.extensions)


def check_it_out(hostname, port):
    hostinfo = get_certificate(hostname, port)
    print_basic_info(hostinfo)


if __name__ == '__main__':
    if True:
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as e:
            for hostinfo in e.map(lambda x: get_certificate(x[0], x[1]), HOSTS):
                print_basic_info(hostinfo)

        exit()
