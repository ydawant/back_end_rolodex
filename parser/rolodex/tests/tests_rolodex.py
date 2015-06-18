#!/usr/bin/env python

import unittest
from mock import call
from mock import MagicMock
from rolodex.models import Rolodex
from rolodex.models import RolodexEntry
from run import run


class RolodexTest(unittest.TestCase):

    def setUp(self):
        self.rolodex = Rolodex("common_first_names.csv", "last_suffix.csv")
        self.entry = RolodexEntry(firstname="Yannick", lastname="Dawant", zipcode='12345',
                             phonenumber='1234567890', color='blue')

    def test_has_valid_number_of_entries(self):
        self.assertTrue(self.rolodex._has_valid_num_entries([1,2,3,4]))
        self.assertTrue(self.rolodex._has_valid_num_entries([1,2,3,4,5]))
        self.assertFalse(self.rolodex._has_valid_num_entries([1,2,3]))
        self.assertFalse(self.rolodex._has_valid_num_entries([1,2,3,4,5,6]))

    def test_has_valid_zip_and_phone(self):
        self.assertTrue(self.rolodex._has_valid_zip_and_phone(['1234567890', '12345', 'color']))
        self.assertFalse(self.rolodex._has_valid_zip_and_phone(['1234567890', '1234567890', 'color']))
        self.assertFalse(self.rolodex._has_valid_zip_and_phone(['12345', '12345', 'color']))
        self.assertFalse(self.rolodex._has_valid_zip_and_phone(['12345', '1234567890', '12345']))
        self.assertFalse(self.rolodex._has_valid_zip_and_phone(['12345', 'color']))

    def test_prints_correctly(self):
        self.rolodex.rolodex_dict.get("entries").append(self.entry)
        self.rolodex.rolodex_dict.get("errors").append(1)
        expected = '{\n  "entries": [' \
                   '\n    {' \
                   '\n      "color": "blue",' \
                   '\n      "firstname": "Yannick",' \
                   '\n      "lastname": "Dawant",' \
                   '\n      "phonenumber": "1234567890",' \
                   '\n      "zipcode": "12345"' \
                   '\n    }' \
                   '\n  ],' \
                   '\n  "errors": [' \
                   '\n    1' \
                   '\n  ]' \
                   '\n}'
        self.assertEquals(self.rolodex.all_entries(), expected)

    def test_sorts_correct(self):
        entry2 = RolodexEntry(firstname="Yannick", lastname="A", zipcode='12345',
                             phonenumber='1234567890', color='blue')

        entry3 = RolodexEntry(firstname="Zannick", lastname="Dawant", zipcode='12345',
                             phonenumber='1234567890', color='blue')

        entries_list = self.rolodex.rolodex_dict.get("entries")
        entries_list.append(self.entry)
        entries_list.append(entry3)
        entries_list.append(entry2)
        self.rolodex._sort_entries()
        sorted_List = self.rolodex.rolodex_dict.get("entries")
        self.assertEqual(sorted_List[0].lastname, "A")
        self.assertEqual(sorted_List[1].lastname, "Dawant")
        self.assertEqual(sorted_List[2].firstname, "Zannick")

    def test_valid_entry_creates_rolodex_entry(self):
        self.rolodex.add_rolodex_entry((0,["Yannick Dawant", "12345", "blue", "1234567890"]))
        self.assertEqual(len(self.rolodex.rolodex_dict.get("entries")), 1)
        self.assertEqual(len(self.rolodex.rolodex_dict.get("errors")), 0)

    def test_invalid_entry_adds_to_errors(self):
        self.rolodex.add_rolodex_entry((0,["12345", "blue", "1234567890"]))
        self.assertEqual(len(self.rolodex.rolodex_dict.get("errors")), 1)
        self.assertEqual(len(self.rolodex.rolodex_dict.get("entries")), 0)


class RolodexEntryTest(unittest.TestCase):

    def setUp(self):
        self.rolodex_entry = RolodexEntry()
        self.entry = RolodexEntry(firstname="Yannick", lastname="Dawant", zipcode='12345',
                             phonenumber='1234567890', color='blue')
        self.common_names = {"John": 5, "James": 2}
        self.suffixes = set("is")

    def test_parse_additional_info(self):
        self.rolodex_entry._parse_additional_info(["blue", "56789", '0987654321'])
        self.assertEqual(self.rolodex_entry.color, 'blue')
        self.assertEqual(self.rolodex_entry.zipcode, '56789')
        self.assertEqual(self.rolodex_entry.phonenumber, '098-765-4321')

    def test_phone_number_formatter(self):
        self.assertEqual('123-456-7890', self.rolodex_entry._format_phone_numer('1234567890'))

    def test_parse_name_first_name_has_frequency(self):
        self.rolodex_entry._parse_name(["John", "Dawant"], self.common_names, self.suffixes)
        self.rolodex_entry.firstname = "John"
        self.rolodex_entry.lastname = "Dawant"
        self.rolodex_entry._parse_name(["Dawant", "John"], self.common_names, self.suffixes)
        self.rolodex_entry.firstname = "John"
        self.rolodex_entry.lastname = "Dawant"
        self.rolodex_entry._parse_name(["John", "James"], self.common_names, self.suffixes)
        self.rolodex_entry.firstname = "John"
        self.rolodex_entry.lastname = "James"

    def test_parse_name_suffix_check(self):
        self.rolodex_entry._parse_name(["Yannick", "Festis"], self.common_names, self.suffixes)
        self.rolodex_entry.firstname = "Yannick"
        self.rolodex_entry.lastname = "Festis"

    def test_no_name_matching(self):
        self.rolodex_entry._parse_name(["No", "Dice"], self.common_names, self.suffixes)
        self.rolodex_entry.firstname = "Dice"
        self.rolodex_entry.lastname = "No"


class RunScriptTest(unittest.TestCase):

    def test_run_parses_line_correctly(self):
        rolodex = Rolodex("rolodex/tests/test_names.csv", "rolodex/tests/test_suffixes.csv")
        rolodex.add_rolodex_entry = MagicMock()
        rolodex.all_entries = MagicMock(return_value='')
        run("rolodex/tests/test_data.csv", rolodex)
        self.assertEqual(rolodex.add_rolodex_entry.call_args_list[0], call((0,["Ria Tillotson", "aqua marine", "97671", "1969105548"])))
        self.assertEqual(rolodex.add_rolodex_entry.call_args_list[1], call((1,["Ria", "Tillotson", "aqua marine", "97671", "1969105548"])))
