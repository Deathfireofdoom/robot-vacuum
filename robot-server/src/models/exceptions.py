# NOTE: Maybe should have implemented a cutsom error instead.
#       But for small projects I believe this is ok.


def get_type_error_for_data_validation(
    value_name: str, actual_type: type, expected_type: type
) -> TypeError:
    return TypeError(
        f"'{value_name}' must be of type {expected_type.__name__}, not {actual_type.__name__}"
    )
