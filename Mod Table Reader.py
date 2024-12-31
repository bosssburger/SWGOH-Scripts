import re

# Create all the keys (mod combos)
sets = ["Critical Chance", "Critical Damage", "Defense", "Health", "Offense", "Potency", "Speed", "Tenacity"]
slots = ["Arrow", "Triangle", "Circle", "Cross"]
primaries = ["Health", "Protection", "Offense", "Defense"]
slot_primaries = {}

for slot in slots:
	val = primaries.copy()
	if slot == "Arrow":
		val.extend(["Speed", "Accuracy", "Critical Avoidance"])
	elif slot == "Triangle":
		val.extend(["Critical Chance", "Critical Damage"])
	elif slot == "Cross":
		val.extend(["Tenacity", "Potency"])

	if slot == "Circle":
		slot_primaries.update({slot : primaries[0:2]})
	else:
		slot_primaries.update({slot : val})

mod_frequencies = {}

for mod in sets:
	for slot in slot_primaries.keys():
		for primary in slot_primaries.get(slot):
			mod_frequencies.update({(mod, slot, primary) : 0})

table = open("SWGOH Mod Table Raw.txt")

txt = table.read()
table.close()
char_info_blocks = re.findall(r'(?s)(units.*?</tr>)', txt)

char_info_dict = {}
total_mods = 0

for char_info in char_info_blocks:

	# Finds sets used by character (group 1)
	used_sets = set(re.findall(r'(?s)data-bs-toggle.*?\d%.{13}(\w+( \w+)?)', char_info))

	# Finds primaries for each slot (group 1, if second option available then second option is group 2)
	used_primaries = re.findall(r'<td>(\w+( \w+)?)( \/ \w+( \w+)?)?', char_info)
	
	for info in used_sets:
		set_type = info[0]
		for i in range(0, 4):
			primary = used_primaries[i][0]

			key = (set_type, slots[i], primary)
			mod_frequencies.update({key : mod_frequencies.get(key) + 1})
			total_mods += 1

			if "/" in used_primaries[i][2]:
				primary = used_primaries[i][2][3:]

				key = (set_type, slots[i], primary)
				mod_frequencies.update({key : mod_frequencies.get(key) + 1})
				total_mods += 1

f = open("Mod Results.csv", "w")

for mod in mod_frequencies.keys():
	f.write(mod[0] + "," + mod[1] + "," + mod[2] + "," + str(mod_frequencies.get(mod)/total_mods*500) + "\n")

f.close()