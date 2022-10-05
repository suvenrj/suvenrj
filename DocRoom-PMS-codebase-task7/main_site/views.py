from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic

from .forms import PatientForm, SearchPatientForm, UpdateDetailsForm
from .models import Members

#-- White Code --
@login_required
#-- White Code --
def home(request):
    search_form = SearchPatientForm(None)
    patients_not_sent_email = Members.objects.filter(sent_mail=False).exclude()
    return render(request, 'home.html', {"search_form": search_form, 'patients_not_sent_email': patients_not_sent_email})

#-- White Code --
@login_required
#-- White Code --
def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'patient_added.html')
        else:
          return render(request, 'add_patient.html', {"form": form})
    else:
        form = PatientForm(None)
        return render(request, 'add_patient.html', {"form" : form })

#-- White Code --
@login_required
#-- White Code --
def display_patient(request):

    patient_firstname = str(request.GET['firstname'])
    patient_lastname = str(request.GET['lastname'])
    patients = Members.objects.filter(firstname__startswith = patient_firstname,
                                      lastname__startswith= patient_lastname).values()
    patients_list = list(patients)
    displayed_patients = sorted(patients_list, key=lambda d: d['DOB'])[:5]

    return render(request, 'display_patient.html', {"displayed_patients": displayed_patients})

#-- White Code --
@login_required
#-- White Code --
def update_patient_details(request,id):

    member_details=Members.objects.filter(id=id).values(
        'firstname','lastname','DOB','email_id','blood_group','mobile_number','upcoming_appointment')

    if request.method=='POST':
        form=UpdateDetailsForm(request.POST)
        if form.is_valid():
            member=Members.objects.get(id=id)
            member.firstname=form.cleaned_data['firstname']
            member.lastname=form.cleaned_data['lastname']
            member.DOB=form.cleaned_data['DOB']
            member.email_id=form.cleaned_data['email_id']
            member.mobile_number=form.cleaned_data['mobile_number']
            member.blood_group=form.cleaned_data['blood_group']

            if member.upcoming_appointment!=form.cleaned_data['upcoming_appointment'] \
                    and form.cleaned_data['upcoming_appointment'] != None \
                    and form.cleaned_data['upcoming_appointment'] != '':
                member.sent_mail=False
            if form.cleaned_data['upcoming_appointment']==None or form.cleaned_data['upcoming_appointment'] == '':
                member.sent_mail=True

            member.upcoming_appointment = form.cleaned_data['upcoming_appointment']
            member.save()
            return HttpResponseRedirect(reverse(home))
        else:
            return render(request, 'update_patient.html',{'form':form})
    else:
        form = UpdateDetailsForm(member_details[0])

        return render(request, 'update_patient.html',{'form':form})

#-- White Code --
@login_required
#-- White Code --
def send_patient_email(request, id):
    patient = Members.objects.get(id = id)
    patient_email = patient.email_id
    send_mail(
        'Example',
        'Here is the message.',
        'suvenjagtiani@gmail.com',
        [str(patient_email)],
        fail_silently=False)
    patient.sent_mail = True
    patient.save()

    return HttpResponseRedirect(reverse(home))

class SignUpView(generic.CreateView):

    #-- White Code --
    form_class = UserCreationForm
    success_url = reverse_lazy("home")
    template_name = "registration/signup.html"
    #-- White Code --
