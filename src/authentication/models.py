from django.db import models
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):

    class UserTypeChoices(models.TextChoices):
        EMPLOYER = 'EMPLOYER', 'Employer'
        SEEKER = 'SEEKER', 'Job seeker'
        ADMIN = 'ADMIN', 'ADMIN'

    DEFAULT_USER_TYPE = 'SEEKER'
        
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    user_type = models.CharField(max_length=8, choices=UserTypeChoices.choices, default=DEFAULT_USER_TYPE)

    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    # Clean email before saving
    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()
    
    # Set the default 
    def save(self, *args, **kwargs):
        if not self.pk:
            self.user_type = self.DEFAULT_USER_TYPE
            return super().save(*args, **kwargs)


# Manager for Employer Model (proxy)
class EmployerManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role='EMPLOYER')
    
# Proxy Model for Employers
class Employer(User):
    DEFAULT_USER_TYPE = 'EMPOYER'

    objects = EmployerManager()

    class Meta:
        proxy = True

# Manager for Staff Model (proxy)
class StaffManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role='STAFF')

# Proxy model for Staffs
class Staff(User):
    DEFAULT_USER_TYPE = 'SEEKER'

    objects = StaffManager()
    
    class Meta:
        proxy = True