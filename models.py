import os
from architettura import aframe

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.documents.models import Document
from wagtail.documents.edit_handlers import DocumentChooserPanel

from colorful.fields import RGBColorField

class PartitionPage(Page):
    introduction = models.CharField(max_length=250, null=True, blank=True,
    help_text="Partition description",)

    search_fields = Page.search_fields + [
        index.SearchField('introduction'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
        InlinePanel('layers', label="Components",),
    ]

class PartitionPageComponent(Orderable):
    page = ParentalKey(PartitionPage, related_name='layers')
    name = models.CharField(max_length=250, default="brick",)
    thickness = models.IntegerField(default=0, help_text="In millimeters")
    weight = models.IntegerField(default=0, help_text="In Newtons per cubic meter")

    panels = [
        FieldPanel('name'),
        FieldPanel('thickness'),
        FieldPanel('weight'),
    ]

class MaterialPage(Page):
    introduction = models.CharField(max_length=250, null=True, blank=True,
    help_text="Material description",)

    search_fields = Page.search_fields + [
        index.SearchField('introduction'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
        InlinePanel('image_files', label="Components",),
    ]

    def get_material_assets(self):
        image_dict = {}
        components = MaterialPageComponent.objects.filter(page_id=self.id)
        for component in components:
            try:
                if component.image:
                    image_dict[self.title + '-' + component.name] = component.image
            except:
                pass
        return image_dict

    def get_entities(self):
        self.path_to_dxf = os.path.join(settings.STATIC_ROOT, 'architettura/samples/materials.dxf')

        material_dict = {}
        components = MaterialPageComponent.objects.filter(page_id=self.id)
        x=0
        component_dict = {}
        for component in components:
            component_dict[x] = [component.name, component.color, component.pattern]
            x += 1
        material_dict[self.title] = component_dict
        layer_dict = {}
        layer_dict['0'] = [self.title, False, False, False, '#ffffff']
        collection = aframe.parse_dxf(self, material_dict, layer_dict)
        collection = aframe.reference_openings(collection)
        collection = aframe.reference_animations(collection)
        for x, d in collection.items():
            d['MATERIAL'] = self.title
            d['WMATERIAL'] = self.title
            d['pool'] = component_dict
            d['wpool'] = component_dict
        mode = 'scene'
        self.shadows = True
        self.double_face = False
        self.fly_camera = False
        entities_dict = aframe.make_html(self, collection, mode)
        return entities_dict

class MaterialPageComponent(Orderable):
    page = ParentalKey(MaterialPage, related_name='image_files')
    name = models.CharField(max_length=250, default="0",)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete = models.SET_NULL,
        related_name = '+',
        help_text="Sets general appearance of material component",
    )
    color = RGBColorField(default='#ffffff',
        help_text="Component color",)
    pattern = models.BooleanField(default=False,
        help_text="Is it a 1x1 meter pattern?",)
    #thickness = models.IntegerField(default=0, help_text="In millimeters")
    #weight = models.IntegerField(default=0, help_text="In Newtons per cubic meter")

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('image'),
        FieldPanel('pattern'),
        FieldPanel('color'),
        #FieldPanel('thickness'),
        #FieldPanel('weight'),
    ]

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
    dxf_file = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        on_delete = models.SET_NULL,
        related_name = '+',
        help_text="CAD file of your project",
        )
    shadows = models.BooleanField(default=False, help_text="Want to cast shadows?",)
    fly_camera = models.BooleanField(default=False,
        help_text="Vertical movement of camera?",)
    double_face = models.BooleanField(default=False,
        help_text="Planes are visible on both sides?",)
    object_repository = models.URLField(
        help_text="URL of external repository for OBJ files", blank=True, null=True
        )

    background = RGBColorField(default='#000000',
        help_text="Background color",)
    equirectangular_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete = models.SET_NULL,
        related_name = '+',
        help_text="Landscape surrounding your project",
        )
    ambient_light_intensity = models.FloatField(default="0.5",
        help_text="Range 1 to 0",)
    ambient_light_color = RGBColorField(default='#ffffff',
        help_text="General ambient light color",)
    hemispheric_color = RGBColorField(default='#ffffff',
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
            DocumentChooserPanel('dxf_file'),
            InlinePanel('cad_files', label="Other CAD file/s",),
            FieldPanel('shadows'),
            FieldPanel('fly_camera'),
            FieldPanel('double_face'),
            FieldPanel('object_repository'),
        ], heading="VR settings", classname="collapsible"
        ),
        MultiFieldPanel([
            FieldPanel('background'),
            ImageChooserPanel('equirectangular_image'),
            FieldPanel('ambient_light_intensity'),
            FieldPanel('ambient_light_color'),
            FieldPanel('hemispheric_color'),
        ], heading="Ambient settings", classname="collapsible collapsed"
        ),
        InlinePanel('layers', label="Layers",),
    ]

    def add_new_layers(self):
        self.path_to_dxf = os.path.join(settings.MEDIA_ROOT, 'documents', self.dxf_file.filename)
        add_new_layers_ext(self)
        return

    def get_object_repository(self):
        return get_object_repository_ext(self)

    def get_material_assets(self):
        return get_material_assets_ext(self)

    def get_object_assets(self):
        object_dict = aframe.get_object_dict(self)
        return object_dict

    def get_entities(self):
        mode = 'scene'
        return get_entities_ext(self, mode)

    def get_ambient_light(self):
        return get_ambient_light_ext(self)

    def get_survey(self):
        survey = SurveyPage.objects.filter(scene_id=self.id)
        return survey

class ScenePageLayer(Orderable):
    page = ParentalKey(ScenePage, related_name='layers')
    name = models.CharField(max_length=250, default="0",
        help_text="As in CAD file",)
    invisible = models.BooleanField(default=False, help_text="Hide layer?",)
    wireframe = models.BooleanField(default=False, help_text="Display only wire frame?",)
    no_shadows = models.BooleanField(default=False, help_text="Layer casts no shadows?",)
    material = models.ForeignKey(MaterialPage, blank=True, null=True,
        on_delete=models.SET_NULL)
    partition = models.ForeignKey(PartitionPage, blank=True, null=True,
        on_delete=models.SET_NULL)

    panels = [
        FieldPanel('name'),
        FieldPanel('invisible'),
        FieldPanel('wireframe'),
        FieldPanel('no_shadows'),
        FieldPanel('material'),
        FieldPanel('partition'),
    ]

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

class SceneIndexPage(Page):
    introduction = models.TextField(
        help_text='Text to describe the page',
        blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
    ]

    # Speficies that only ScenePage objects can live under this index page
    subpage_types = ['ScenePage']

    # Defines a method to access the children of the page (e.g. ScenePage
    # objects).
    def children(self):
        return self.get_children().specific().live()

    # Overrides the context to list all child items, that are live, by the
    # date that they were published
    # http://docs.wagtail.io/en/latest/getting_started/tutorial.html#overriding-context
    def get_context(self, request):
        context = super(SceneIndexPage, self).get_context(request)
        context['posts'] = ScenePage.objects.descendant_of(
            self).live().order_by(
            '-first_published_at')
        return context

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
        on_delete=models.PROTECT, help_text="Choose Scene you'd like to see digitalkOmiX style")

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
        self.scene.path_to_dxf = os.path.join(settings.MEDIA_ROOT, 'documents', self.scene.dxf_file.filename)
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

class SurveyPage(Page):
    introduction = models.CharField(max_length=250, null=True, blank=True,
    help_text="Survey description",)
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
        on_delete=models.PROTECT, help_text="Choose Scene to be surveyed")

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
        InlinePanel('layers', label="Layers",),
    ]

    def add_new_layers(self):
        self.scene.path_to_dxf = os.path.join(settings.MEDIA_ROOT, 'documents', self.scene.dxf_file.filename)
        layer_list = aframe.get_layer_list(self.scene)
        for layer in layer_list:
            try:
                a = SurveyPageLayer.objects.get(page_id=self.id, name=layer)
            except:
                b = SurveyPageLayer(page_id=self.id, name=layer)
                b.save()
        return

    def get_entities(self):
        mode = 'scene'
        material_dict = prepare_material_dict()
        part_dict = prepare_partition_dict()
        layer_dict = prepare_layer_dict(self.scene)
        collection = aframe.parse_dxf(self.scene, material_dict, layer_dict)
        collection = add_partitions(collection, part_dict)
        collection = aframe.reference_openings(collection)
        collection = aframe.reference_animations(collection)
        entities_dict = aframe.make_html(self.scene, collection, mode)
        entities = {'message': 'Hello World'}
        return entities

    def add_partitions(collection, part_dict):
        return collection

class SurveyPageLayer(Orderable):
    page = ParentalKey(SurveyPage, related_name='layers')
    name = models.CharField(max_length=250, default="0",
        help_text="As in CAD file",)
    invisible = models.BooleanField(default=False, help_text="Exclude layer from survey?",)

    panels = [
        FieldPanel('name'),
        FieldPanel('invisible'),
    ]

def add_new_layers_ext(page_obj):
    layer_list = aframe.get_layer_list(page_obj)
    for layer in layer_list:
        try:
            a = ScenePageLayer.objects.get(page_id=page_obj.id, name=layer)
        except:
            b = ScenePageLayer(page_id=page_obj.id, name=layer)
            b.save()

    return

def get_material_assets_ext(page_obj):
    material_dict = aframe.get_entity_material(page_obj)
    try:
        layers = ScenePageLayer.objects.filter(page_id=page_obj.id)
        for layer in layers:
            try:
                m = MaterialPage.objects.get(id=layer.material_id)
                material_dict[m.title] = 'dummy'
            except:
                pass
    except:
        pass
    image_dict = {}
    if material_dict:
        for material, dummy in material_dict.items():
            try:
                m = MaterialPage.objects.get(title=material)
                components = MaterialPageComponent.objects.filter(page_id=m.id)
                for component in components:
                    try:
                        if component.image:
                            image_dict[m.title + '-' + component.name] = component.image
                    except:
                        pass
            except:
                pass
    return image_dict

def get_entities_ext(page_obj, mode):
    material_dict = prepare_material_dict()
    layer_dict = prepare_layer_dict(page_obj)
    collection = aframe.parse_dxf(page_obj, material_dict, layer_dict)
    collection = aframe.reference_openings(collection)
    collection = aframe.reference_animations(collection)
    entities_dict = aframe.make_html(page_obj, collection, mode)
    return entities_dict

def prepare_material_dict():
    material_dict = {}
    try:
        materials = MaterialPage.objects.all()
        if materials:
            for m in materials:
                components = MaterialPageComponent.objects.filter(page_id=m.id)
                x=0
                component_dict = {}
                for component in components:
                    component_dict[x] = [component.name, component.color, component.pattern]
                    x += 1
                material_dict[m.title] = component_dict
    except:
        pass

    return material_dict

def prepare_partition_dict():
    part_dict = {}
    try:
        parts = PartitionPage.objects.all()
        if parts:
            for p in parts:
                components = PartitionPageComponent.objects.filter(page_id=p.id)
                x=0
                component_dict = {}
                for component in components:
                    component_dict[x] = [component.name, component.thickness,
                    component.weight]
                    x += 1
                part_dict[p.title] = component_dict
    except:
        pass

    return part_dict

def prepare_layer_dict(page_obj):
    layer_dict = {}
    try:
        layers = ScenePageLayer.objects.filter(page_id=page_obj.id)
        if layers:
            for layer in layers:
                try:
                    m = MaterialPage.objects.get(id=layer.material_id)
                    layer_dict[layer.name] = [m.title, layer.invisible,
                    layer.wireframe, layer.no_shadows]
                except:
                    layer_dict[layer.name] = ['default', layer.invisible,
                    layer.wireframe, layer.no_shadows]
                try:
                    p = PartitionPage.objects.get(id=layer.partition_id)
                    layer_dict[layer.name].append(p.title)
                except:
                    layer_dict[layer.name].append('default')
    except:
        pass

    return layer_dict

def get_ambient_light_ext(page_obj):
    ambient_light = f'color: {page_obj.ambient_light_color}; '
    ambient_light += f'groundColor: {page_obj.hemispheric_color}; '
    ambient_light += f'intensity: {page_obj.ambient_light_intensity}; '
    return ambient_light
