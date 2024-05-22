from django import forms


def get_single_error_from_form(form: forms.ModelForm) -> str:
    if form.non_field_errors():
        return form.non_field_errors()[0]

    for field in form:
        if field.errors:
            return field.errors[0]
    return "Some error occured. Please check if all fields are valid and submit again."
