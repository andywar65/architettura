class MaterialIndexPage(Page):
    introduction = models.TextField(
        help_text='Text to describe the page',
        blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
    ]

    # Speficies that only MaterialPage objects can live under this index page
    subpage_types = ['MaterialPage']

    # Defines a method to access the children of the page (e.g. MaterialPage
    # objects).
    def children(self):
        return self.get_children().specific().live()

    # Overrides the context to list all child items, that are live, by the
    # date that they were published
    # http://docs.wagtail.io/en/latest/getting_started/tutorial.html#overriding-context
    def get_context(self, request):
        context = super(MaterialIndexPage, self).get_context(request)
        context['posts'] = MaterialPage.objects.descendant_of(
            self).live().order_by(
            '-first_published_at')
        return context

class ScenePageCadFile(Orderable):
    page = ParentalKey(ScenePage, related_name='cad_files')
    dxf_file = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        on_delete = models.SET_NULL,
        related_name = '+',
        help_text="Additional CAD files of your project",
        )
    x_position = models.FloatField(default="0",
        help_text="In meters, displacement with respect to axis origin",)
    y_position = models.FloatField(default="0", help_text="In meters, see above",)
    z_position = models.FloatField(default="0", help_text="In meters, see above",)
    rotation = models.FloatField(default="0",
        help_text="In degrees, counterclockwise around Z axis",)

    panels = [
        DocumentChooserPanel('dxf_file'),
        FieldPanel('x_position'),
        FieldPanel('y_position'),
        FieldPanel('z_position'),
        FieldPanel('rotation'),
    ]

class ArScenePage(Page):
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
    scene = models.ForeignKey(ScenePage, blank=True, null=True,
        on_delete=models.PROTECT, help_text="Choose Scene you'd like to see in AR")

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
        FieldPanel('scene'),
    ]

    def add_new_layers(self):
        self.scene.path_to_dxf = os.path.join(settings.MEDIA_ROOT, 'documents', self.scene.dxf_file.filename)
        add_new_layers_ext(self.scene)
        return

    def get_object_assets(self):
        object_dict = aframe.get_object_dict(self.scene)
        return object_dict

    def get_material_assets(self):
        return get_material_assets_ext(self.scene)

    def get_entities(self):
        mode = 'ar'
        return get_entities_ext(self.scene, mode)

class DigkomPage(Page):
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
    scene = models.ForeignKey(ScenePage, blank=True, null=True,
        on_delete=models.PROTECT,
        help_text="Choose Scene you'd like to see digitalkOmiX style")

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
        FieldPanel('scene'),
    ]

    def background(self):
        return self.scene.background

    def equirectangular_image(self):
        return self.scene.equirectangular_image

    def add_new_layers(self):
        self.scene.path_to_dxf = os.path.join(settings.MEDIA_ROOT, 'documents',
            self.scene.dxf_file.filename)
        add_new_layers_ext(self.scene)
        return

    def get_material_assets(self):
        return get_material_assets_ext(self.scene)

    def get_object_assets(self):
        object_dict = aframe.get_object_dict(self.scene)
        return object_dict

    def get_entities(self):
        mode = 'digkom'
        return get_entities_ext(self.scene, mode)

    def get_ambient_light(self):
        return get_ambient_light_ext(self.scene)
