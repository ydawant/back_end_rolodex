import json
import re


class Rolodex(object):

    def __init__(self, common_names_file, suffix_file):
        self.common_first_names = {name : int(number_of_times) for number_of_times, name  in [line.strip().split(" ") for line in open(common_names_file, 'r')]}
        self.suffix_set = set([line.strip() for line in open(suffix_file, 'r')])
        self.rolodex_dict = {"entries" : [], "errors" : []}

    def add_rolodex_entry(self, array_tuple):
        '''
        array_tuple: tuple of the row_line and the line content (index, line)

        Adds the RolodexEntry to the entries list, or adds the index of the error to the errors list
        '''

        index, line_array = array_tuple
        if self._has_valid_num_entries(line_array) and self._has_valid_zip_and_phone(line_array[-3:]):
            rolodex_entry = RolodexEntry().create_rolodex_entry(line_array, self.common_first_names, self.suffix_set)
            self.rolodex_dict["entries"].append(rolodex_entry)
        else:
            self.rolodex_dict["errors"].append(index)

    def all_entries(self):
        '''
        Prints out the rolodex_dict, so all entries in the rolodex entries and all error indexes
        '''
        self._sort_entries()
        return json.dumps( self.rolodex_dict, sort_keys=True,
                  indent=2, separators=(',', ': '), default=self._encode_rolodex)

    def _sort_entries(self):
        '''
        Sorts entries list by last name, first name
        '''
        self.rolodex_dict["entries"] = sorted(self.rolodex_dict.get("entries"), key = lambda x: (x.lastname, x.firstname))

    def _encode_rolodex(self, obj):
        '''
        Properly JSON encodes RolodexEntry objects
        '''
        if isinstance(obj, RolodexEntry):
            return obj.__dict__
        return obj

    def _has_valid_num_entries(self, line_array):
        '''
        With the given inputs, it's necessary that each line has at least 4 entries, and no more than 5
        '''
        return 4 <= len(line_array) <=5

    def _has_valid_zip_and_phone(self, info):
        '''
        checks if there is a phone number and zip code contained in the last 3 entries of the line.
        '''
        digits = [x for x in info if x.isdigit()]
        if digits:
            return (len(max(digits, key=len)) == 10 and len(min(digits, key=len)) == 5 and len(digits) == 2)
        else:
            return False

class RolodexEntry(object):

    def __init__(self, firstname='', lastname='', zipcode='', phonenumber='', color=''):
        self.firstname = firstname
        self.lastname = lastname
        self.zipcode = zipcode
        self.phonenumber = phonenumber
        self.color = color

    def create_rolodex_entry(self, line_array, common_first_names, suffixes):
        '''
        Base logic for parsing the line, breaks it up into name, and other
        '''
        if len(line_array) == 4:
            names = line_array[0].split(" ")
            self.firstname = " ".join(names[:-1])
            self.lastname = names[-1]
        else:
            self._parse_name(line_array[:2], common_first_names, suffixes)

        self._parse_additional_info(line_array[-3:])

        return self

    def _parse_name(self, names, common_first_names, suffixes):
        '''
        Parses name. Checks for first name frequency, if that's not fruitful, check if one of the names has a common
        suffix. Unfortunately, I had no way of knowing how frequent those endings are, so started by checking the first
        entry as the more common practice is last_name, first_name. If all else fails - save using that convention.
        '''

        name_0 = names[0]
        name_1 = names[1]

        #checking if first name in common first name list, and frequency of times it shows up
        name_1_frequency = common_first_names.get(name_0, 0)
        name_2_frequency = common_first_names.get(name_1, 0)

        #check if name in first name, if it is, set names
        if name_1_frequency > name_2_frequency:
            self._assign_names(name_0, name_1)
        # only assign first name to second name if frequency is not 0
        elif name_2_frequency is not 0:
            self._assign_names(name_1, name_0)
        #if neither in the first name set, check last name suffixes
        else:
            if any(names[0].endswith(x) for x in suffixes):
                self._assign_names(name_1, name_0)
            elif any(names[1].endswith(x) for x in suffixes):
                self._assign_names(name_0, name_1)
            # if that fails, fallback is just to assume that last name is first, as that's a more standard convention
            else:
                self._assign_names(name_1, name_0)

    def _assign_names(self, first_name, last_name):
        '''
        Helper method to assign the names
        '''
        self.firstname = first_name
        self.lastname = last_name

    def _parse_additional_info(self, info_array):
        '''
        Parse out the other information and assign to relevant field.
        '''
        for item in info_array:
            if item.isdigit():
                if len(item) == 5:
                    self.zipcode = item
                else:
                    self.phonenumber = self._format_phone_numer(item)
            else:
                self.color = item

    def _format_phone_numer(self, phone_number_digits):
        '''
        Formats phone number to the xxx-xxx-xxxx convention
        '''
        return re.sub(r'(\d{3})(\d{3})(\d{4})', "\g<1>-\g<2>-\g<3>", phone_number_digits)