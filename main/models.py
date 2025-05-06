from django.utils.translation import gettext_lazy as _

from colorfield.fields import ColorField

# User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import PermissionDenied
from django.db import models
from django.contrib import auth
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


def _user_has_perm(user, perm, obj):
    """A backend can raise `PermissionDenied` to short-circuit permission checking."""
    for backend in auth.get_backends():
        if not hasattr(backend, "has_perm"):
            continue
        try:
            if backend.has_perm(user, perm, obj):
                return True
        except PermissionDenied:
            return False
    return False


def _user_has_module_perms(user, app_label):
    """A backend can raise `PermissionDenied` to short-circuit permission checking."""
    for backend in auth.get_backends():
        if not hasattr(backend, "has_module_perms"):
            continue
        try:
            if backend.has_module_perms(user, app_label):
                return True
        except PermissionDenied:
            return False
    return False


class UserManager(BaseUserManager):
    """Custom user manager to handle user creation logic, including vendor, freelancer, and company creation."""

    use_in_migrations = True

    def save_user(
            self,
            email,
            scope_level,
            first_name,
            last_name,
            country,
            password,
            **extrafields,
    ):
        user = self.model(
            email=self.normalize_email(email),
            scope_level=scope_level,
            first_name=first_name,
            last_name=last_name,
            country=country,
            **extrafields,
        )
        if password is not None:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, scope_level, first_name, last_name, country, password=None, **extrafields):
        extrafields["is_superuser"] = False
        extrafields["is_staff"] = False
        return self.save_user(email, scope_level, first_name, last_name, country, password, **extrafields)

    def create_staffuser(self, email, scope_level, first_name, last_name, country, password, **extrafields):
        extrafields["is_staff"] = True
        extrafields["is_superuser"] = False
        return self.save_user(email, scope_level, first_name, last_name, country, password, **extrafields)

    def create_superuser(self, email, scope_level, first_name, last_name, country, password, **extrafields):
        extrafields.setdefault("is_superuser", True)
        extrafields["is_staff"] = True
        return self.save_user(email, scope_level, first_name, last_name, country, password, **extrafields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User model with support for different scope levels."""

    objects = UserManager()

    class Scope(models.IntegerChoices):
        ADMIN = 0
        CUSTOMER = 1


    email = models.EmailField(verbose_name="email address", max_length=255, db_index=True, unique=True)
    first_name = models.CharField(max_length=32, default="_UNKNOWN", verbose_name="First Name")
    last_name = models.CharField(max_length=32, default="_UNKNOWN", verbose_name="Last Name")
    country = models.CharField(max_length=200, default="_UNKNOWN", verbose_name="Country of the user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)
    scope_level = models.IntegerField(choices=Scope.choices, db_index=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["scope_level", "first_name", "last_name", "country"]

    def __str__(self):
        return f"{self.email}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def is_customer(self):
        """Returns True if the user is a vendor (MERCHANT scope)."""
        return self.scope_level == User.Scope.CUSTOMER



class VendorProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="vendor_profile",
        limit_choices_to={'scope_level': User.Scope.CUSTOMER}
    )
    vendor_name = models.CharField(max_length=255, verbose_name=_("Vendor Name"))
    description = models.TextField(verbose_name=_("Vendor Description"))
    whatsapp_number = models.CharField(max_length=20, verbose_name=_("WhatsApp Number"))
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0, verbose_name=_("Rating"))

    def __str__(self):
        return self.vendor_name

class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("Title"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    background_color = ColorField(default="#FFFFFF", verbose_name=_("Background Color"))
    def __str__(self):
        return self.title