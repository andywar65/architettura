from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.documents.models import Document
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel

class ScenePage(Page):
    introduction = models.CharField(max_length=250, null=True, blank=True, help_text="Project description",)
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

    search_fields = Page.search_fields + [
        index.SearchField('introduction'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('introduction'),
            ImageChooserPanel('image'),
            FieldPanel('date_published'),
        ], heading="Presentation"),
    ]
