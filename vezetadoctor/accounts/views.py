from django.shortcuts import render,redirect, get_object_or_404
from django.http import JsonResponse
from .models import Profile, Appointment
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, SignUp,  UpdateUser
from django.core.mail import send_mail
<<<<<<< HEAD:vezetadoctor/accounts/views.py
from django.utils.timezone import localtime, make_aware
from django.utils import timezone
from django.conf import settings
from datetime import datetime
from datetime import timedelta

=======
from django.utils.timezone import localtime
from django.utils.timezone import make_aware
from datetime import datetime
>>>>>>> a10639cf17b4206131cd7badbfa2bfeb8061a0b7:vezeta/vezetadoctor/accounts/views.py
# Create your views here.


def index(request):
    profiles = Profile.objects.all()
    return render(request, 'user/index.html', {'profiles':profiles})

def doctor_detail(request, slug):
    doctor = Profile.objects.get(slug=slug)
    return render(request, 'user/doctor_detail.html', {'doctor':doctor})    

@login_required(login_url='loginform')
def myprofile(request):
    user = request.user 
    return render(request, 'user/myprofile.html', {'user': user})

def signup(request):
    if request.method == 'POST':
        form = SignUp(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # التحقق إذا كان اسم المستخدم موجود بالفعل
            if User.objects.filter(username=username).exists():
                messages.error(request, "اسم المستخدم موجود بالفعل. يرجى اختيار اسم مستخدم آخر.")
                return render(request, 'user/signup.html', {'form': form})


            # إنشاء المستخدم
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )

            messages.success(request, "تم التسجيل بنجاح! يمكنك الآن تسجيل الدخول.")
            return redirect('loginform')
    else:
        form = SignUp()

    return render(request, 'user/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)
                messages.success(request, "تم تسجيل الدخول بنجاح!")
                return redirect('index')  
            else:
                messages.error(request, "اسم المستخدم أو كلمة المرور غير صحيحة.")
                return redirect('loginform')  
        else:
            messages.error(request, "الرجاء ملء الحقول بشكل صحيح.")
            return redirect('loginform')
    else:
        form = LoginForm()
        return render(request, 'user/loginform.html', {'form': form})

def logout_view(request):
    if request.user.is_authenticated:
        auth_logout(request)
        messages.success(request, 'تم تسجيل الخروج بنجاح')  
        return redirect('index')
    return JsonResponse({'message': 'User is not authenticated'})

login_required(login_url='loginform')
def updateuser(request):
    if request.method == 'POST':
        form = UpdateUser(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            if password != confirm_password:
                messages.error(request, "كلمة المرور وتأكيد كلمة المرور غير متطابقتين.")
                return redirect('updateuser')

            if password:
                request.user.set_password(password)
                update_session_auth_hash(request, request.user)  
          
            request.user.username = username
            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.save()

            messages.success(request, "تم تحديث البيانات بنجاح!")
            return redirect('myprofile')  
    else:

        form = UpdateUser(initial={
            'username': request.user.username,  
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        })

    return render(request, 'user/updateuser.html', {'form': form})


def doctor_list(request):
    doctors = Profile.objects.all()  # استرجاع جميع الأطباء من قاعدة البيانات
    return render(request, 'user/doctor_list.html', {'doctors': doctors})

@login_required(login_url='loginform')
def updateprofile(request):
    user = request.user 

    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':

        user.username = request.POST.get('username')
        user.email = request.POST.get('email')

        if 'password' in request.POST and request.POST['password']:
            user.set_password(request.POST['password'])
            user.save()
            update_session_auth_hash(request, user)  # لتحديث الجلسة بعد تغيير كلمة المرور

        # تحديث بيانات البروفايل
        profile.name = request.POST.get('name')
        profile.city = request.POST.get('city')
        profile.phone = request.POST.get('phone')
        profile.working_hours = request.POST.get('working_hours')
        profile.waiting_time = request.POST.get('waiting_time')
        profile.services = request.POST.get('services')
        profile.price = request.POST.get('price')

        # تحديث الصورة إذا تم إرسال صورة جديدة
        if 'image' in request.FILES:
            profile.image = request.FILES.get('image')

        profile.twitter = request.POST.get('twitter')
        profile.facebook = request.POST.get('facebook')
        profile.linkedin = request.POST.get('linkedin')
        profile.instagram = request.POST.get('instagram')
        profile.gender = request.POST.get('gender')
        profile.available_times = request.POST.get('available_times')

        # حفظ التغييرات في الـ User و الـ Profile
        user.save()
        profile.save()

        # رسالة نجاح
        messages.success(request, "تم حفظ البيانات بنجاح.")
        return redirect('index')  # إعادة توجيه المستخدم إلى الصفحة الرئيسية

    else:
        # عرض البيانات الحالية للمستخدم
        return render(request, 'user/updateprofile.html', {
            'user': user,
            'profile': profile
        })


<<<<<<< HEAD:vezetadoctor/accounts/views.py



=======
>>>>>>> a10639cf17b4206131cd7badbfa2bfeb8061a0b7:vezeta/vezetadoctor/accounts/views.py
# عرض الأوقات المتاحة للطبيب
def available_times(request, slug):
    doctor = get_object_or_404(Profile, slug=slug)

    available_times_input = doctor.available_times.split('\n')  # افترض أن الأوقات مفصولة بأسطر جديدة
    
    available_times_obj = []
    for time_str in available_times_input:
        try:
            # تحويل الوقت إلى كائن datetime
            available_time = datetime.strptime(time_str.strip(), "%Y-%m-%d %H:%M:%S")  # تأكد من التنسيق الصحيح
            available_times_obj.append(make_aware(available_time)
            )  # تحويل الوقت إلى منطقة الزمن المحلية
        except ValueError:
            pass   # تحويل الوقت إلى منطقة الزمن المحلية

    # تمرير الأوقات المتاحة للطبيب إلى القالب
    return render(request, 'user/available_times.html', {'doctor': doctor, 'available_times': available_times_obj})

<<<<<<< HEAD:vezetadoctor/accounts/views.py
=======




>>>>>>> a10639cf17b4206131cd7badbfa2bfeb8061a0b7:vezeta/vezetadoctor/accounts/views.py
# حجز موعد
@login_required
def book_appointment(request, slug, appointment_time):
    doctor = get_object_or_404(Profile, slug=slug)
    user = request.user

    # تحويل appointment_time إلى كائن datetime
    appointment_time_obj = make_aware(datetime.strptime(appointment_time, "%Y-%m-%d %H:%M:%S"))

    # إنشاء الحجز
    appointment = Appointment.objects.create(
        doctor=doctor,
        user=user,
        appointment_time=appointment_time_obj,
        confirmed=False
    )

    return redirect('appointment_confirmation', appointment_id=appointment.id)

<<<<<<< HEAD:vezetadoctor/accounts/views.py
=======




>>>>>>> a10639cf17b4206131cd7badbfa2bfeb8061a0b7:vezeta/vezetadoctor/accounts/views.py
# تأكيد الحجز
@login_required
def appointment_confirmation(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
        # التحقق إذا كان هناك حجز مؤكد بنفس الوقت للمستخدم
    existing_appointment = Appointment.objects.filter(user=appointment.user,appointment_time=appointment.appointment_time,confirmed=True).first()

    # إذا كان هناك حجز مؤكد سابقًا
    if existing_appointment:
        return render(request, 'user/appointment_confirmation.html', {'appointment': appointment, 'already_booked': True })


    if request.method == 'POST':
        # إرسال إشعار بالبريد الإلكتروني بعد تأكيد الحجز
        send_mail(
            'تأكيد الحجز',
            f'تم تأكيد حجز الموعد مع الدكتور {appointment.doctor.name} في {appointment.appointment_time}.',
            settings.EMAIL_HOST_USER,
            [appointment.user.email],
            fail_silently=False,
        )

        # بعد إرسال البريد الإلكتروني، نقوم بتأكيد الحجز
        appointment.confirmed = True
        appointment.save()

        return render(request, 'user/confirmation.html', {'appointment': appointment})

    return render(request, 'user/appointment_confirmation.html', {'appointment': appointment})

#عرض المواعيد المحجوزة (عرض المواعيد القادمة للمستخدم)
@login_required
def upcoming_appointments(request):
    # استرجاع المواعيد القادمة فقط للمستخدم
    user_appointments = Appointment.objects.filter(user=request.user)

    return render(request, 'user/upcoming_appointments.html', {'appointments':user_appointments})

#from django.core.mail import send_mail
from django.conf import settings

@login_required
def cancel_appointment(request, appointment_id):
    # الحصول على الموعد من خلال ID
    appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)

    # التأكد من أن الموعد في المستقبل قبل إلغاءه
    if appointment.appointment_time > timezone.now():
        appointment.delete()
        messages.success(request, 'تم إلغاء الموعد بنجاح.')
        
        # إرسال البريد الإلكتروني بعد إلغاء الموعد
        subject = 'إلغاء الموعد'
        message = f'مرحبًا {request.user.username},\n\nتم إلغاء موعدك المقرر في {appointment.appointment_time}.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [request.user.email]
        
        send_mail(subject, message, from_email, recipient_list)
    else:
        messages.error(request, 'لا يمكن إلغاء الموعد لأنه تم بالفعل.')

    return redirect('upcoming_appointments')  # إعادة توجيه المستخدم لعرض المواعيد القادمة



def search_doctor(request):
    doctors = Profile.objects.all()

    doctor_name = request.GET.get('username')
    if doctor_name:
        doctors = doctors.filter(name__icontains=doctor_name)

    specialization = request.GET.get('specialization')
    if specialization:
        doctors = doctors.filter(specialty__icontains=specialization)

    location = request.GET.get('location')
    if location:
        doctors = doctors.filter(city__icontains=location)

    return render(request, 'user/search.html', {'doctors': doctors})



@login_required
def doctor_dashboard(request):

    doctor_profile = request.user.profile.name
    
    appointments = Appointment.objects.filter(doctor=doctor_profile, confirmed=True, appointment_time__gte=datetime.now()).order_by('appointment_time')

    appointment_data = []
    for appointment in appointments:
        # استرجاع تفاصيل المريض الذي حجز الموعد
        patient_name = appointment.user.profile.name
        appointment_data.append({
            'appointment': appointment,
            'patient_name': patient_name,
        })

    context = {
        'appointment_data': appointment_data,
        'doctor_profile': doctor_profile,
    }
    
    return render(request, 'user/doctor_dashboard.html', context)
