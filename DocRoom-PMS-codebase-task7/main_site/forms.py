from django import forms
from .models import Members


class PatientForm(forms.ModelForm):
    class Meta:
        model = Members
        exclude=['upcoming_appointment', 'sent_mail']

    def clean_mobile_number(self):
        mobile = self.cleaned_data['mobile_number']
        if len(mobile) != 10:
            raise forms.ValidationError('INVALID MOBILE NUMBER')
        for x in mobile:
            if ord(x) > 57 or ord(x) < 48:
                raise forms.ValidationError('INVALID MOBILE NUMBER')
        else:
            return mobile

    def clean_blood_group(self):
        blood_groups=['A+', 'A-', 'B+', 'B-', 'O']
        blood_group = self.cleaned_data['blood_group']
        if blood_group not in blood_groups:
            raise forms.ValidationError('INVALID BLOOD GROUP')
        return blood_group

    def clean(self):
        first_name = self.cleaned_data['firstname']
        last_name = self.cleaned_data['lastname']
        DOB = self.cleaned_data['DOB']
        if Members.objects.filter(firstname=first_name, lastname=last_name, DOB=DOB).values():
            raise forms.ValidationError('Patient already Exists')
        return self.cleaned_data


class SearchPatientForm(forms.Form):
    firstname = forms.CharField(max_length=255)
    lastname = forms.CharField(max_length=255)


class UpdateDetailsForm(forms.Form):

    firstname = forms.CharField(max_length=255)
    lastname = forms.CharField(max_length=255)
    DOB = forms.DateField()
    blood_group= forms.CharField(max_length=255)
    email_id = forms.EmailField(max_length=255)
    mobile_number = forms.CharField(max_length=255)
    upcoming_appointment = forms.DateTimeField(required=False)

    def clean_mobile_number(self):
        mobile = self.cleaned_data['mobile_number']
        if len(mobile) != 10:
            raise forms.ValidationError('INVALID MOBILE NUMBER')
        for x in mobile:
            if ord(x) > 57 or ord(x) < 48:
                raise forms.ValidationError('INVALID MOBILE NUMBER')
        else:
            return mobile

    def clean_blood_group(self):
        blood_groups = ['A+', 'A-', 'B+', 'B-', 'O']
        blood_group = self.cleaned_data['blood_group']
        if blood_group not in blood_groups:
            raise forms.ValidationError('INVALID BLOOD GROUP')
        return blood_group
