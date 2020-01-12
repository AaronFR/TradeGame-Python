import re
x = "5 food"

number_regex = re.search("[-+]?[0-9]+", x)
string_regex = re.search("[a-z]+", x)
print(int(number_regex.group()))
print(string_regex.group())
