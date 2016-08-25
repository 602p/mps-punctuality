from ldap3 import Server, Connection, AUTH_SIMPLE, STRATEGY_SYNC, ALL, NTLM
import getpass

HOST="ldap://10.99.1.43:3268"
USERNAME="BUSINESS\\FLELDAPLOOKUP"#@business.k12.mn.us"
PASSWORD=getpass.getpass("Password:")#"takaya"

print("Creating Server...")
s = Server(HOST, get_info=ALL, connect_timeout=5)
print("Creating Conenction")
c = Connection(s,# authentication=NTLM,
  user=USERNAME, password=PASSWORD, auto_bind=False)
print("Opening Connection")
c.open()
print("Binding...")
c.bind()