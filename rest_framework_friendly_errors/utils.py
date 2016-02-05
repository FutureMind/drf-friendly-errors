def update_field_settings(setting, user_setting):
    for field in user_setting:
        field_type = setting.get(field)
        if field_type is None:
            setting[field] = user_setting[field]
        else:
            for key in user_setting[field]:
                setting[field][key] = user_setting[field][key]
    return setting
