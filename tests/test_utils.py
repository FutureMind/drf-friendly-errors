from unittest import TestCase

from rest_framework_friendly_errors.utils import update_field_settings


class UpdateFieldSettingTestCase(TestCase):

    def setUp(self):
        self.FIELD_SETTING = {
            'CharField': {'required': 2001, 'null': 2003, 'blank': 2004,
                          'max_length': 2005, 'min_length': 2006},
            'EmailField': {'required': 2001, 'invalid': 2002, 'null': 2003,
                           'blank': 2004, 'max_length': 2005, 'min_length': 2006},
        }

    def test_update_settings_with_empty_dict(self):
        USER_SETTING = {}
        setting = update_field_settings(self.FIELD_SETTING, USER_SETTING)
        self.assertEqual(setting, self.FIELD_SETTING)

    def test_update_existing_setting(self):
        USER_SETTING = {
            'CharField': {'required': 10},
            'EmailField': {'required': 11}
        }
        setting = update_field_settings(self.FIELD_SETTING, USER_SETTING)
        self.assertEqual(setting['CharField']['required'], 10)
        self.assertEqual(setting['EmailField']['required'], 11)
        self.assertEqual(setting['CharField']['null'], 2003)
        self.assertEqual(setting['EmailField']['null'], 2003)

    def test_update_and_add_new_field_setting(self):
        USER_SETTING = {
            'CharField': {'required': 10},
            'EmailField': {'required': 11},
            'CustomField': {'null': 12}
        }
        setting = update_field_settings(self.FIELD_SETTING, USER_SETTING)
        self.assertEqual(setting['CharField']['required'], 10)
        self.assertEqual(setting['EmailField']['required'], 11)
        self.assertEqual(setting['CharField']['max_length'], 2005)
        self.assertEqual(setting['EmailField']['max_length'], 2005)
        self.assertEqual(setting['CustomField']['null'], 12)
