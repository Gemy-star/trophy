from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

class Announcement(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("Title"))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))

    class Meta:
        verbose_name = _("Announcement")
        verbose_name_plural = _("Announcements")

    def __str__(self):
        return self.title



class HomeSlider(models.Model):
    image = models.ImageField(upload_to='slider/', verbose_name=_("Slider Image"))
    # Processed image (1920x600)
    image_resized = ImageSpecField(
        source='image',
        processors=[ResizeToFill(1920, 600)],
        format='JPEG',
        options={'quality': 85}
    )
    heading = models.CharField(max_length=255, verbose_name=_("Heading"))
    subheading = models.TextField(verbose_name=_("Subheading"))
    button_text = models.CharField(max_length=100, verbose_name=_("Button Text"))
    button_url_name = models.CharField(
        max_length=100,
        verbose_name=_("Django URL Name"),
        help_text=_("Enter the Django URL name (e.g. 'about_page', 'blogs_page').")
    )
    order = models.PositiveIntegerField(default=0, verbose_name=_("Display Order"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))

    class Meta:
        ordering = ['order']
        verbose_name = _("Home Slider")
        verbose_name_plural = _("Home Sliders")

    def __str__(self):
        return self.heading

    def get_button_url(self):
        from django.urls import reverse
        try:
            return reverse(self.button_url_name)
        except:
            return "#"