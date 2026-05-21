import ssl
import socket
# import OpenSSL
from cryptography import x509
import cryptography
import pip_system_certs.wrapt_requests  # Force l'intégration


def get_certificate(host, port=443, timeout=10):
    context = ssl.create_default_context()
    conn = socket.create_connection((host, port))
    sock = context.wrap_socket(conn, server_hostname=host)
    sock.settimeout(timeout)
    try:
        der_cert = sock.getpeercert(True)
    finally:
        sock.close()
    return ssl.DER_cert_to_PEM_cert(der_cert)


# certificate = get_certificate('example.com')
# certificate = get_certificate('echange.asp-public.fr')
certificate = get_certificate('www.google.fr')

cert = x509.load_pem_x509_certificate(
    certificate.encode() if isinstance(certificate, str) else certificate)

print("issuer:", cert.issuer.rfc4514_string())
print("not_valid_after:", cert.not_valid_after_utc.strftime('%Y-%m-%d %H:%M:%S'))
print("not_valid_before:", cert.not_valid_before_utc.strftime('%Y-%m-%d %H:%M:%S'))
print("serial_number:", cert.serial_number)
# print(f"\n{cert.signature=}")
print("subject:", cert.subject.rfc4514_string())
print("version:", cert.version.name, "=", cert.version.value)
print("Objects Identifier:")
for certificat in cert.extensions:
    print(f"- {str(certificat.critical):5}", end=", ")

    print(f"{certificat.oid._name:30}", end=" = ")
    print(certificat.oid.dotted_string)

    if hasattr(certificat.value, "__iter__"):
        for cert in certificat.value:

            if type(cert) is cryptography.hazmat.bindings._rust.ObjectIdentifier:
                if hasattr(cert, "dotted_string"):
                    print("    * dotted_string:", cert.dotted_string)

            elif type(cert) is cryptography.x509.extensions.DistributionPoint:
                if hasattr(cert, "full_name"):
                    print("    * full_name: ", end="")
                    for name in cert.full_name:
                        print(name.value, end=", ")
                    print()

            elif type(cert) is cryptography.x509.extensions.AccessDescription:            
                if hasattr(cert, "access_location"):
                    print("    * access_location:", cert.access_location.value)
                if hasattr(cert, "access_method"):
                    print("    * access_method:", cert.access_method._name, "=", cert.access_method.dotted_string)

            elif type(cert) is cryptography.x509.general_name.DNSName:
                if hasattr(cert, "value"):
                    print("    * value:", cert.value)

            elif type(cert) is cryptography.x509.extensions.PolicyInformation:
                if hasattr(cert, "policy_identifier"):
                    print("    * policy_identifier:", cert.policy_identifier._name, "=", cert.policy_identifier.dotted_string)
                if hasattr(cert, "policy_qualifiers"):
                    print("    * policy_qualifiers:", cert.policy_qualifiers)

            elif type(cert) is cryptography.hazmat.bindings._rust.x509.Sct:
                print("   [", cert.signature_algorithm, end=", ")
                print(cert.signature_hash_algorithm.name, "]")
                if hasattr(cert, "entry_type"):
                    print("    * entry_type:", cert.entry_type)
                if hasattr(cert, "extension_bytes"):
                    print("    * extension_bytes:", cert.extension_bytes)
                if hasattr(cert, "log_id"):
                    print("    * log_id:", cert.log_id)
                if hasattr(cert, "timestamp"):
                    print("    * timestamp:", cert.timestamp)
                if hasattr(cert, "version"):
                    print("    * version:", cert.version)
            else:
                raise TypeError("type de certificat inconnu:", type(cert))

    else:
        print("    * value:", certificat.value)
        print("    * oid:", certificat.oid._name, "=", certificat.oid.dotted_string)
