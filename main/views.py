from django.views.generic import TemplateView , ListView , View
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext as _
from main.models import Category , User
from .forms import VendorProfileForm, ContactForm


class HomePageView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.filter(is_active=True)
        context["vendors"] = User.objects.filter(is_active=True, scope_level=User.Scope.CUSTOMER)
        return context


class PolicyPageView(TemplateView):
    template_name = 'pages/policy.html'


class RefundPageView(TemplateView):
    template_name = 'pages/refund.html'


class CategoriesListView(ListView):
    template_name = 'pages/categories.html'
    model = Category
    context_object_name = 'categories'

class AuthView(View):
    template_name = "pages/auth_page.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        if 'email' in request.POST and 'password' in request.POST:
            # Login form submitted
            user = authenticate(request, email=request.POST['email'], password=request.POST['password'])
            if user is not None:
                login(request, user)
                messages.success(request, _("تم تسجيل الدخول بنجاح."))
                return redirect("home")  # change to your success URL
            else:
                messages.error(request, _("بيانات الاعتماد غير صحيحة."))
        else:
            # Registration form submitted
            try:
                password1 = request.POST['password1']
                password2 = request.POST['password2']
                if password1 != password2:
                    messages.error(request, _("كلمتا المرور غير متطابقتين."))
                    return redirect("auth_view")

                user = User.objects.create_user(
                    email=request.POST['email'],
                    password=password1,
                    first_name=request.POST['full_name'].split(" ")[0],
                    last_name=" ".join(request.POST['full_name'].split(" ")[1:]) or "_UNKNOWN",
                    scope_level=User.Scope.CUSTOMER,
                    country="_UNKNOWN"
                )
                messages.success(request, _("تم إنشاء الحساب بنجاح. يمكنك تسجيل الدخول الآن."))
            except Exception as e:
                messages.error(request, _("حدث خطأ أثناء التسجيل: ") + str(e))

        return redirect("auth_view")  # reload page with messages

def vendor_register(request):
    if request.method == 'POST':
        form = VendorProfileForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.pop('username')
            password = form.cleaned_data.pop('password')

            if User.objects.filter(username=username).exists():
                form.add_error('username', _('اسم المستخدم موجود بالفعل.'))
            else:
                user = User.objects.create_user(username=username, password=password)
                vendor_profile = form.save(commit=False)
                vendor_profile.user = user
                vendor_profile.save()
                form.save_m2m()  # Save many-to-many data
                return redirect('auth_view')
    else:
        form = VendorProfileForm()
    return render(request, 'pages/register_vendor.html', {'form': form})

def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("تم إرسال الرسالة بنجاح."))
            return redirect("contact")
    else:
        form = ContactForm()
    return render(request, "pages/contact.html", {"form": form})
class AboutPageView(TemplateView):
    template_name = 'pages/about.html'
