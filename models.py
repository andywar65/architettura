from django import forms
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.documents.models import Document
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel

class MaterialPage(Page):
    introduction = models.CharField(max_length=250, null=True, blank=True,
    help_text="Material description",)

    search_fields = Page.search_fields + [
        index.SearchField('introduction'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
        InlinePanel('image_files', label="Images",),
    ]

class MaterialPageImages(Orderable):
    page = ParentalKey(MaterialPage, related_name='image_files')
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete = models.SET_NULL,
        related_name = '+',
        help_text="Sets general appearance of material",
    )
    color = models.CharField(max_length=250, default="white", help_text="Accepts hex (#ffffff) or HTML color",)
    pattern = models.BooleanField(default=False, help_text="Is it a 1x1 meter pattern?",)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('pattern'),
        FieldPanel('color'),
    ]

class ScenePage(Page):
    introduction = models.CharField(max_length=250, null=True, blank=True,
    help_text="Scene description",)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )
    date_published = models.DateField(
        "Date article published", blank=True, null=True
        )
    author = models.ForeignKey(User, blank=True, null=True,
        on_delete=models.PROTECT)

    shadows = models.BooleanField(default=False, help_text="Want to cast shadows?",)
    fly_camera = models.BooleanField(default=False, help_text="Vertical movement of camera?",)
    double_face = models.BooleanField(default=False, help_text="Planes are visible on both sides?",)
    ar = models.BooleanField(default=False, help_text="Is it Augmented Reality?",)

    equirectangular_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete = models.SET_NULL,
        related_name = '+',
        help_text="Landscape surrounding your project",
        )
    ambient_light_intensity = models.FloatField(default="1",
        help_text="Range 1 to 0",)
    ambient_light_color = models.CharField(max_length=250, default="white",
        help_text="Accepts hex (#ffffff) or HTML color",)
    hemispheric_color = models.CharField(max_length=250, default="white",
        help_text="Ambient light color from below",)

    search_fields = Page.search_fields + [
        index.SearchField('introduction'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('introduction'),
            ImageChooserPanel('image'),
            FieldPanel('author'),
            FieldPanel('date_published'),
        ], heading="Presentation", classname="collapsible collapsed"),
        MultiFieldPanel([
            InlinePanel('cad_files', label="CAD file/s",),
            FieldPanel('ar'),
            FieldPanel('shadows'),
            FieldPanel('fly_camera'),
            FieldPanel('double_face'),
        ], heading="VR/AR settings", classname="collapsible collapsed"
        ),
        MultiFieldPanel([
            ImageChooserPanel('equirectangular_image'),
            FieldPanel('ambient_light_intensity'),
            FieldPanel('ambient_light_color'),
            FieldPanel('hemispheric_color'),
        ], heading="Ambient settings", classname="collapsible collapsed"
        ),
        InlinePanel('layers', label="Layers",),
    ]

class ScenePageLayer(Orderable):
    page = ParentalKey(ScenePage, related_name='layers')
    name = models.CharField(max_length=250, default="0",
        help_text="As in CAD file",)
    material = models.ForeignKey(MaterialPage, blank=True, null=True,
        on_delete=models.SET_NULL)

    panels = [
        FieldPanel('name'),
        FieldPanel('material'),
    ]

class ScenePageCadFile(Orderable):
    page = ParentalKey(ScenePage, related_name='cad_files')
    dxf_file = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        on_delete = models.SET_NULL,
        related_name = '+',
        help_text="CAD file of your project",
        )
    x_position = models.FloatField(default="0",
        help_text="In meters, displacement with respect to axis origin",)
    y_position = models.FloatField(default="0", help_text="In meters, see above",)
    z_position = models.FloatField(default="0", help_text="In meters, see above",)

    panels = [
        DocumentChooserPanel('dxf_file'),
        FieldPanel('x_position'),
        FieldPanel('y_position'),
        FieldPanel('z_position'),
    ]
