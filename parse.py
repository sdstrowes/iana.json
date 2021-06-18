import codecs
import csv
import ipaddress
import requests
import sys
import ujson as json


reader = csv.reader(open("iana-ipv6-special-registry-1.csv", "r"))

urls = [
	"https://www.iana.org/assignments/iana-ipv4-special-registry/iana-ipv4-special-registry-1.csv",
	"https://www.iana.org/assignments/iana-ipv6-special-registry/iana-ipv6-special-registry-1.csv"
]


everything = []
for u in urls:
	r = requests.get(u)
	if r.status_code != 200:
		print("Error fetching "+u)
		print("Aboring")
		sys.exit(1)

	response = r.iter_lines()

#	print(response)
#	for r in response:
#		print(r.decode('utf-8'))

	reader = csv.reader(codecs.iterdecode(response, 'utf-8'))

	for row in reader:
		out = {}

		try:
			ip = ipaddress.ip_network(row[0])
		except ValueError as e:
			continue


		out["prefix"] = row[0]
		if ":" in out["prefix"]:
			out["af"] = 6
		else:
			out["af"] = 4

		out["description"] = row[1]
		out["references"] = row[2]
		out["allocation_date"] = row[3]
		out["termination_date"] = row[4]

		# one case where this is unspecified is 192.88.99.0/24, 6to4; treat as reachable
		tmp = row[5].split()
		value = None
		if len(tmp) > 0:
			value = tmp[0].lower() == 'true'
		elif out["prefix"] == "192.88.99.0/24":
			value = True
		elif out["prefix"] == "2001:10::/28":
			value = False
		out["source"] = value

		tmp = row[6].split()
		value = None
		if len(tmp) > 0:
			value = tmp[0].lower() == 'true'
		elif out["prefix"] == "192.88.99.0/24":
			value = True
		elif out["prefix"] == "2001:10::/28":
			value = False
		out["destination"] = value

		tmp = row[7].split()
		value = None
		if len(tmp) > 0:
			value = tmp[0].lower() == 'true'
		elif out["prefix"] == "192.88.99.0/24":
			value = True
		elif out["prefix"] == "2001:10::/28":
			value = False
		out["forwardable"] = value

		tmp = row[8].split()
		value = None
		if len(tmp) > 0:
			value = tmp[0].lower() == 'true'
		elif out["prefix"] == "192.88.99.0/24":
			value = True
		elif out["prefix"] == "2001:10::/28":
			value = False
		out["globally_reachable"] = value

		tmp = row[9].split()
		value = None
		if len(tmp) > 0:
			value = tmp[0].lower() == 'true'
		elif out["prefix"] == "192.88.99.0/24":
			value = False
		elif out["prefix"] == "2001:10::/28":
			value = False
		out["reserved_by_protocol"] = value

		everything.append(out)

with open("iana-special-registries.json", "w") as outfile:
	outfile.write(json.dumps(everything, indent=2))

