import os
from math import fabs
from architettura import aframe, dxf, blobs

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel
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

    def write_html(self):
        output = []
        i = 1
        layers = self.layers.all()
        if layers:

            for layer in layers:

                thickness = fabs(float(layer.thickness)/1000)
                if thickness == 0:
                    thickness = 0.1
                    name = str(i) + '- ' + layer.name + ' (variable)'
                else:
                    name = str(i) + '- ' + layer.name + ' (' + str(thickness*1000) + ' mm)'
                if i == 1:
                    dist = 0
                else:
                    dist += dist2 + thickness/2
                output.append({'dist': -dist, 'color': dxf.cad2hex(i),
                    'thick': thickness, 'text': name})
                i += 1
                dist2 = thickness/2

        return output

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

    def add_new_layers(self):

        self.layer_dict = {}
        #prepare a dictionary with dummy values plus color
        self.layer_dict['0'] = [self.title, False, False, False,
            '#ffffff', 'default']

        return

    def get_object_assets(self):

        self.ent_list = []
        #prepare the list of entities for general use
        lines = blobs.get_material_blob().splitlines()
        for line in lines:
            blob = {}
            ent = {}
            pairs = line.split('=;')
            for pair in pairs:
                couple = pair.split('=:')
                blob[couple[0]] = couple[1]
            ent['id'] = blob.pop('id', 'ID')
            ent['tag'] = blob.pop('tag', 'a-entity')
            ent['closing'] = int(blob.pop('closing', 1))
            if 'extras' in blob:
                ent['extras'] = blob.pop('extras')
            ent['blob'] = blob
            self.ent_list.append(ent)

        return

    def get_material_assets(self):
        image_dict = {}
        self.material_dict = {}
        components = MaterialPageComponent.objects.filter(page_id=self.id)
        comp_list = []
        for comp in components:
            values = (comp.name, comp.image,
                comp.pattern, comp.color)
            comp_list.append(values)
            if comp.image:
                image_dict[self.title + '-' + comp.name] = comp.image
        self.material_dict[self.title] = comp_list

        return image_dict

    def get_entities(self):
        for ent in self.ent_list:
            blob = ent['blob']

            if ('material' in blob or 'obj-model' in blob or
                'gltf-model' in blob):
                blob['shadow'] = 'cast: true; receive: true'
            #set layer color
            if blob['layer'] in self.layer_dict:
                layer = self.layer_dict[blob['layer']]
                if layer[1]:#layer is invisible
                    blob['visible'] = 'false'
                if layer[3] and 'material' in blob:#layer casts/receives no shadows
                    blob['shadow'] = 'cast: false; receive: false'
                layer_color = f'color: {layer[4]}; '
            else:
                layer_color = 'color: #ffffff; '
            #if requested, set material
            if 'material' in blob:
                if blob['material'] in self.material_dict:
                    components = self.material_dict[blob['material']]
                    try:
                        comp = components[int(blob['component'])]
                        blob['material'] = f'src: #{blob["material"]}-{comp[0]}; '
                        blob['material'] += f'color: {comp[3]}; '
                        if comp[2]:
                            blob['material'] += f'repeat: {blob["repeat"]}; '
                    except:
                        pass
                elif layer[0] in self.material_dict:
                    components = self.material_dict[layer[0]]#components is a list
                    try:
                        comp = components[int(blob['component'])]
                        blob['material'] = f'src: #{layer[0]}-{comp[0]}; '
                        blob['material'] += f'color: {comp[3]}; '
                        if comp[2]:
                            blob['material'] += f'repeat: {blob["repeat"]}; '
                    except:
                        pass
                elif blob['material'] == '':
                    blob['material'] = layer_color
                elif blob['material'][0] == '#':
                    blob['material'] = f'color: {blob["material"]}; '
                if layer[2]:
                    blob['material'] += 'wireframe: true;'
            #loop through blob items
            for key, value in blob.items():
                if key == 'light' or key[:4] == 'line' or key == 'text':
                    if 'color' in blob and blob['color'] != '':
                        blob[key] = value + f'color: {blob["color"]}; '
                    else:
                        try:
                            comp = components[0]
                            blob[key] += f'color: {comp[3]}; '
                        except:
                            blob[key] = value + layer_color
                elif key == 'obj-model':
                    obj = blob['obj-model']
                    blob['obj-model'] = f'obj: #{obj}.obj; mtl: #{obj}.mtl;'
                elif key == 'gltf-model':
                    blob['gltf-model'] = f'#{blob["gltf-model"]}.gltf'
                    ent['extras'] = 'animation-mixer'
                elif key == 'href':
                    try:
                        if blob['href'] == '#parent':
                            target = self.get_parent()
                        elif blob['href'] == '#child':
                            target = self.get_first_child()
                        elif blob['href'] == '#previous' or blob['href'] == '#prev':
                            target = self.get_prev_sibling()
                        elif blob['href'] == '#next':
                            target = self.get_next_sibling()
                        blob['href'] = target.url
                        blob['title'] = target.title
                        try:
                            eq_image = target.specific.equirectangular_image
                            blob['image'] = eq_image.file.url
                        except:
                            pass
                    except:
                        blob['href'] = ''
                if key == 'light':
                    blob['light'] += 'castShadow: true; '

            #cannot pop keys inside loop
            values = ('component', 'layer', 'repeat', 'color', 'partition')
            for v in values:
                if v in blob:
                    blob.pop(v)
            if ent['tag'] == 'a-cursor':
                blob['color'] = '#2E3A87'
                close = ['a-cursor', 'a-camera', 'a-entity']
            else:
                close = []
                for c in range(ent['closing']):
                    if c == 0:
                        close.append(ent['tag'])
                    else:
                        close.append('a-entity')
            ent['closing'] = close
        return self.ent_list

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

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('image'),
        FieldPanel('pattern'),
        FieldPanel('color'),
    ]

class DxfPage(Page):
    introduction = models.CharField(max_length=250, null=True, blank=True,
    help_text="File description",)
    dxf_file = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        on_delete = models.SET_NULL,
        related_name = '+',
        help_text="CAD file of your project",
        )
    block = models.BooleanField(default=False,
        help_text="Prevent DXF from changing Database?",)
    object_repository = models.URLField(
        help_text="URL of external repository for OBJ/GLTF files",
        blank=True, null=True)
    entities = models.TextField(blank=True,
        default='id=:identity=;tag=:a-entity=;closing=:1',
        )

    search_fields = Page.search_fields + [
        index.SearchField('introduction'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
        MultiFieldPanel([
            DocumentChooserPanel('dxf_file'),
            FieldPanel('block'),
            FieldPanel('object_repository'),
        ], heading="Sources", ),
        InlinePanel('layers', label="Layers",),
        FieldPanel('entities'),
    ]

    def add_new_layers(self):
        """Collects layers in dxf and adds Dxf Page Layers

        Works only if unblocked. Gets a dictionary of layers from dxf and
        refreshes layers in db. Returns nothing.
        """
        #skip if blocked
        if self.block:
            return
        #set path to dxf, once and for all
        self.path_to_dxf = os.path.join(settings.MEDIA_ROOT, 'documents',
            self.dxf_file.filename)
        #get layers in dxf
        layer_dict = dxf.get_layer_dict(self)
        #delete existing Dxf Page Layers
        DxfPageLayer.objects.filter(page_id=self.id).delete()
        #add layers in db
        for name, color in layer_dict.items():
            lb = DxfPageLayer(page_id=self.id, name=name, color=color)
            lb.save()

        return

    def add_entities(self):
        #skip if blocked
        if self.block:
            return
        #collect entities from dxf
        collection = dxf.parse_dxf(self)
        collection = dxf.reference_openings(collection)
        collection = dxf.reference_animations(collection)
        #make entity dictionary
        dxf.make_entities_dict(self, collection)
        #delete existing Entities
        self.entities = ''
        #add entities in db
        for identity, blob in self.ent_dict.items():
            self.entities += blob + '\n'
        #prevent dxf file from overriding again database
        self.block = True
        self.save()
        return

    def get_object_assets(self):
        self.ent_list = []
        #prepare the list of entities for general use
        lines = self.entities.splitlines()
        for line in lines:
            blob = {}
            ent = {}
            pairs = line.split('=;')
            for pair in pairs:
                couple = pair.split('=:')
                blob[couple[0]] = couple[1]
            ent['id'] = blob.pop('id', 'ID')
            ent['tag'] = blob.pop('tag', 'a-entity')
            ent['closing'] = int(blob.pop('closing', 1))
            if 'extras' in blob:
                ent['extras'] = blob.pop('extras')
            ent['blob'] = blob
            self.ent_list.append(ent)
        #prepare object dictionary for template
        if self.object_repository:
            path = self.object_repository
        else:
            path = os.path.join(settings.MEDIA_URL, 'documents')
        object_dict = {}
        for ent in self.ent_list:
            blob = ent['blob']
            if 'obj-model' in blob:
                object_dict[blob['obj-model'] + '.' + 'obj'] = path
                object_dict[blob['obj-model'] + '.' + 'mtl'] = path
            if 'gltf-model' in blob:
                object_dict[blob['gltf-model'] + '.' + 'gltf'] = path

        return object_dict

    def get_entities(self):
        page_layers = DxfPageLayer.objects.filter(page_id=self.id)
        for ent in self.ent_list:
            blob = ent['blob']
            #set layer color
            try:
                layer = page_layers.get(name=blob['layer'])
                layer_color = f'color: {layer.color}; '
            except:
                layer_color = 'color: #ffffff; '
            #if requested, set material color
            if 'material' in blob:
                if blob['material'] == '':
                    blob['material'] = layer_color
                elif blob['material'][0] == '#':
                    blob['material'] = f'color: {blob["material"]}; '
                else:
                    blob['material'] = layer_color
            #loop through blob items
            for key, value in blob.items():
                if key == 'light' or key[:4] == 'line' or key == 'text':
                    if 'color' in blob and blob['color'] != '':
                        blob[key] = value + f'color: {blob["color"]}; '
                    else:
                        blob[key] = value + layer_color
                elif key == 'obj-model':
                    obj = blob['obj-model']
                    blob['obj-model'] = f'obj: #{obj}.obj; mtl: #{obj}.mtl;'
                elif key == 'gltf-model':
                    blob['gltf-model'] = f'#{blob["gltf-model"]}.gltf'
                    ent['extras'] = 'animation-mixer'
            #cannot pop keys inside loop
            values = ['component', 'layer', 'repeat', 'color', 'partition']
            for v in values:
                if v in blob:
                    blob.pop(v)
            if ent['tag'] == 'a-cursor':
                blob['color'] = '#2E3A87'
                close = ['a-cursor', 'a-camera', 'a-entity']
            else:
                close = []
                for c in range(ent['closing']):
                    if c == 0:
                        close.append(ent['tag'])
                    else:
                        close.append('a-entity')
            ent['closing'] = close
        return self.ent_list

class DxfPageLayer(Orderable):
    page = ParentalKey(DxfPage, related_name='layers')
    name = models.CharField(max_length=250, default="0",
        help_text="As in CAD file",)
    color = RGBColorField(default='#ffffff',
        help_text="Layer color",)

    panels = [
        FieldPanel('name'),
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
    mode_choices = (('scene', 'Keyboard enabled (W-A-S-D), no checkpoints'),
        ('digkom', 'Keyboard disabled, use checkpoints'),
        ('ar', 'Augmented Reality'),
    )
    mode = models.CharField(max_length=250, blank=False, choices=mode_choices,
        default='scene', help_text="How do you move in the scene",)
    dxf_file = models.ForeignKey(DxfPage, blank=True, null=True,
        on_delete=models.SET_NULL)
    shadows = models.BooleanField(default=False, help_text="Want to cast shadows?",)
    fly_camera = models.BooleanField(default=False,
        help_text="Vertical movement of camera?",)
    double_face = models.BooleanField(default=False,
        help_text="Planes are visible on both sides?",)

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
            FieldPanel('mode'),
            FieldPanel('dxf_file'),
            #DocumentChooserPanel('dxf_file'),
            #InlinePanel('cad_files', label="Other CAD file/s",),
            FieldPanel('shadows'),
            FieldPanel('fly_camera'),
            FieldPanel('double_face'),
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

    def get_template(self, request):
        if self.mode == 'digkom':
            return 'architettura/digkom_page.html'
        return 'architettura/scene_page.html'

    def add_new_layers(self):

        self.layer_dict = {}
        dxf_layers = DxfPageLayer.objects.filter(page_id=self.dxf_file.id)
        #prepare a dictionary with dummy values plus color
        for layer in dxf_layers:
            self.layer_dict[layer.name] = ['default', False, False, False,
                layer.color, 'default']
        #populate dictionary or create new layer
        for name, list in self.layer_dict.items():
            try:
                a = ScenePageLayer.objects.get(page_id=self.id, name=name)
                if a.material:
                    list[0] = a.material.title
                list[1] = a.invisible
                list[2] = a.wireframe
                list[3] = a.no_shadows
                if a.partition:
                    list[5] = a.partition.title
                self.layer_dict[name] = list
            except:
                b = ScenePageLayer(page_id=self.id, name=name)
                b.save()
        #erase layers if they are no more in dxf page
        page_layers = ScenePageLayer.objects.filter(page_id=self.id)
        for page_layer in page_layers:
            if page_layer.name not in self.layer_dict:
                page_layer.delete()
        return

    def get_object_assets(self):
        self.ent_list = []
        #prepare the list of entities for general use
        lines = self.dxf_file.entities.splitlines()
        for line in lines:
            blob = {}
            ent = {}
            pairs = line.split('=;')
            for pair in pairs:
                couple = pair.split('=:')
                blob[couple[0]] = couple[1]
            ent['id'] = blob.pop('id', 'ID')
            ent['tag'] = blob.pop('tag', 'a-entity')
            ent['closing'] = int(blob.pop('closing', 1))
            if 'extras' in blob:
                ent['extras'] = blob.pop('extras')
            ent['blob'] = blob
            self.ent_list.append(ent)
        #prepare object dictionary for template
        if self.dxf_file.object_repository:
            path = self.dxf_file.object_repository
        else:
            path = os.path.join(settings.MEDIA_URL, 'documents')
        object_dict = {}
        for ent in self.ent_list:
            blob = ent['blob']
            if 'obj-model' in blob:
                object_dict[blob['obj-model'] + '.' + 'obj'] = path
                object_dict[blob['obj-model'] + '.' + 'mtl'] = path
            if 'gltf-model' in blob:
                object_dict[blob['gltf-model'] + '.' + 'gltf'] = path
        return object_dict

    def get_material_assets(self):
        image_dict = {}
        self.material_dict = {}
        self.part_dict = {}
        materials = MaterialPage.objects.all()
        partitions = PartitionPage.objects.all()
        for name, list in self.layer_dict.items():
            try:
                m = materials.get(title=list[0])
                if m.title not in self.material_dict:
                    components = MaterialPageComponent.objects.filter(page_id=m.id)
                    comp_list = []
                    for comp in components:
                        values = (comp.name, comp.image,
                            comp.pattern, comp.color)
                        comp_list.append(values)
                        if comp.image:
                            image_dict[m.title + '-' + comp.name] = comp.image
                    self.material_dict[m.title] = comp_list
            except:
                pass
            try:
                p = partitions.get(title=list[5])
                if p.title not in self.part_dict:
                    self.part_dict[p.title] = ''
            except:
                pass
        for ent in self.ent_list:
            blob = ent['blob']
            if ('material' in blob and blob['material'] != '' and
                blob['material'][0] != '#'):
                try:
                    m = materials.get(title=blob['material'])
                    if m.title not in self.material_dict:
                        components = MaterialPageComponent.objects.filter(page_id=m.id)
                        comp_list = []
                        for comp in components:
                            values = (comp.name, comp.image,
                                comp.pattern, comp.color)
                            comp_list.append(values)
                            if comp.image:
                                image_dict[m.title + '-' + comp.name] = comp.image
                        self.material_dict[m.title] = comp_list
                except:
                    m = MaterialPage(title=blob['material'])
                    self.add_child(instance=m)
            if 'partition' in blob and blob['partition'] != '':
                try:
                    p = partitions.get(title=blob['partition'])
                    if p.title not in self.part_dict:
                        self.part_dict[p.title] = ''
                except:
                    p = PartitionPage(title=blob['partition'])
                    self.add_child(instance=p)
        return image_dict

    def get_entities(self):
        for ent in self.ent_list:
            blob = ent['blob']
            if self.shadows:
                if ('material' in blob or 'obj-model' in blob or
                    'gltf-model' in blob):
                    blob['shadow'] = 'cast: true; receive: true'
            #set layer color
            if blob['layer'] in self.layer_dict:
                layer = self.layer_dict[blob['layer']]
                if layer[1]:#layer is invisible
                    blob['visible'] = 'false'
                if layer[3] and 'material' in blob:#layer casts/receives no shadows
                    blob['shadow'] = 'cast: false; receive: false'
                layer_color = f'color: {layer[4]}; '
            else:
                layer_color = 'color: #ffffff; '
            #if requested, set material
            if 'material' in blob:
                if blob['material'] in self.material_dict:
                    components = self.material_dict[blob['material']]
                    try:
                        comp = components[int(blob['component'])]
                        blob['material'] = f'src: #{blob["material"]}-{comp[0]}; '
                        blob['material'] += f'color: {comp[3]}; '
                        if comp[2]:
                            blob['material'] += f'repeat: {blob["repeat"]}; '
                        if self.double_face:
                            blob['material'] += 'side: double; '
                    except:
                        pass
                elif layer[0] in self.material_dict:
                    components = self.material_dict[layer[0]]#components is a list
                    try:
                        comp = components[int(blob['component'])]
                        blob['material'] = f'src: #{layer[0]}-{comp[0]}; '
                        blob['material'] += f'color: {comp[3]}; '
                        if comp[2]:
                            blob['material'] += f'repeat: {blob["repeat"]}; '
                        if self.double_face:
                            blob['material'] += 'side: double; '
                    except:
                        pass
                elif blob['material'] == '':
                    blob['material'] = layer_color
                elif blob['material'][0] == '#':
                    blob['material'] = f'color: {blob["material"]}; '
                if layer[2]:
                    blob['material'] += 'wireframe: true;'
            #loop through blob items
            for key, value in blob.items():
                if key == 'light' or key[:4] == 'line' or key == 'text':
                    if 'color' in blob and blob['color'] != '':
                        blob[key] = value + f'color: {blob["color"]}; '
                    else:
                        try:
                            comp = components[0]
                            blob[key] += f'color: {comp[3]}; '
                        except:
                            blob[key] = value + layer_color
                elif key == 'obj-model':
                    obj = blob['obj-model']
                    blob['obj-model'] = f'obj: #{obj}.obj; mtl: #{obj}.mtl;'
                elif key == 'gltf-model':
                    blob['gltf-model'] = f'#{blob["gltf-model"]}.gltf'
                    ent['extras'] = 'animation-mixer'
                elif key == 'href':
                    try:
                        if blob['href'] == '#parent':
                            target = self.get_parent()
                        elif blob['href'] == '#child':
                            target = self.get_first_child()
                        elif blob['href'] == '#previous' or blob['href'] == '#prev':
                            target = self.get_prev_sibling()
                        elif blob['href'] == '#next':
                            target = self.get_next_sibling()
                        blob['href'] = target.url
                        blob['title'] = target.title
                        try:
                            eq_image = target.specific.equirectangular_image
                            blob['image'] = eq_image.file.url
                        except:
                            pass
                    except:
                        blob['href'] = ''
                if key == 'light' and self.shadows:
                    blob['light'] += 'castShadow: true; '
            if ent['id'] == 'camera-ent':
                if self.mode == 'digkom':
                    blob['movement-controls'] = 'controls: checkpoint'
                    blob['checkpoint-controls'] = 'mode: animate'
            elif ent['id'] == 'camera':
                if self.mode == 'digkom':
                    blob['wasd-controls'] = 'enabled: false'
                else:
                    blob['wasd-controls'] = f'fly: {str(self.fly_camera).lower()}'
            #cannot pop keys inside loop
            values = ('component', 'layer', 'repeat', 'color', 'partition')
            for v in values:
                if v in blob:
                    blob.pop(v)
            if ent['tag'] == 'a-cursor':
                blob['color'] = '#2E3A87'
                close = ['a-cursor', 'a-camera', 'a-entity']
            else:
                close = []
                for c in range(ent['closing']):
                    if c == 0:
                        close.append(ent['tag'])
                    else:
                        close.append('a-entity')
            ent['closing'] = close
        return self.ent_list

    def get_ambient_light(self):
        return get_ambient_light_ext(self)

    def get_survey(self):
        survey = SurveyPage.objects.filter(scene_id=self.id)
        return survey

    def get_material_list(self):
        material_list = []
        for name, list in self.material_dict.items():
            try:
                m = MaterialPage.objects.get(title=name)
                material_list.append(m)
            except:
                pass
        return material_list

    def get_part_list(self):
        part_list = []
        for name, list in self.part_dict.items():
            try:
                m = PartitionPage.objects.get(title=name)
                part_list.append(m)
            except:
                pass
        return part_list

class ScenePageLayer(Orderable):
    page = ParentalKey(ScenePage, related_name='layers')
    name = models.CharField(max_length=250, default="0",
        help_text="As in CAD file",)
    invisible = models.BooleanField(default=False, help_text="Hide layer?",)
    wireframe = models.BooleanField(default=False,
        help_text="Display only wire frame?",)
    no_shadows = models.BooleanField(default=False,
        help_text="Layer casts no shadows?",)
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
        on_delete=models.SET_NULL, help_text="Choose Scene to be surveyed")

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
        #we still have to produce the scene page layer dict
        #TODO erase layers if they are no more in dxf
        self.scene.add_new_layers()
        for name, list in self.scene.layer_dict.items():
            try:
                a = SurveyPageLayer.objects.get(page_id=self.id, name=name)
            except:
                b = SurveyPageLayer(page_id=self.id, name=name)
                b.save()
        return

    def get_entities(self):
        self.scene.path_to_dxf = os.path.join(settings.MEDIA_ROOT, 'documents',
                                self.scene.dxf_file.dxf_file.filename)
        #image dict is useless here, but that's how we get dicts
        image_dict = get_material_assets_ext(self.scene)
        collection = aframe.parse_dxf(self.scene)
        collection = aframe.reference_openings(collection)
        collection = aframe.reference_animations(collection)
        collection = add_partitions(self.scene, collection)
        layer_dict = {}
        layers = SurveyPageLayer.objects.filter(page_id=self.id)
        if layers:
            for layer in layers:
                layer_dict[layer.name] = layer.invisible
        entities_dict = aframe.make_survey(collection, layer_dict)
        return entities_dict

class SurveyPageLayer(Orderable):
    page = ParentalKey(SurveyPage, related_name='layers')
    name = models.CharField(max_length=250, default="0",
        help_text="As in CAD file",)
    invisible = models.BooleanField(default=False, help_text="Exclude layer from survey?",)

    panels = [
        FieldPanel('name'),
        FieldPanel('invisible'),
    ]

def get_material_assets_ext(page_obj):
    aframe.get_entity_material(page_obj)
    for name, list in page_obj.layer_dict.items():
        try:
            m = MaterialPage.objects.get(title=list[0])
            page_obj.material_dict[m.title] = {'0': ['Null']}
        except:
            pass
        try:
            p = PartitionPage.objects.get(title=list[5])
            page_obj.part_dict[p.title] = {'0': ['Null']}
        except:
            pass

    image_dict = {}
    if page_obj.material_dict:
        for material, dummy in page_obj.material_dict.items():
            try:
                m = MaterialPage.objects.get(title=material)
            except:
                if material and material != 'default':
                    m = MaterialPage(title=material)
                    page_obj.add_child(instance=m)
            try:
                components = MaterialPageComponent.objects.filter(page_id=m.id)
                x=0
                component_dict = {}
                for component in components:
                    component_dict[x] = [component.name, component.color,
                        component.pattern]
                    x += 1
                    if component.image:
                        image_dict[m.title + '-' +
                            component.name] = component.image
                page_obj.material_dict[material] = component_dict
            except:
                pass
    if page_obj.part_dict:
        for partition, dummy in page_obj.part_dict.items():
            try:
                p = PartitionPage.objects.get(title=partition)
            except:
                if (partition and
                    partition != 'default' and partition != 'ghost'):
                    p = PartitionPage(title=partition)
                    page_obj.add_child(instance=p)
            try:
                components = PartitionPageComponent.objects.filter(page_id=p.id)
                x=0
                component_dict = {}
                for component in components:
                    component_dict[x] = [component.name, component.thickness,
                        component.weight]
                    x += 1
                page_obj.part_dict[partition] = component_dict
            except:
                pass

    return image_dict

def get_entities_ext(page_obj):
    collection = aframe.parse_dxf(page_obj)
    collection = aframe.reference_openings(collection)
    collection = aframe.reference_animations(collection)
    entities_dict = aframe.make_html(page_obj, collection)
    return entities_dict

def get_ambient_light_ext(page_obj):
    ambient_light = f'color: {page_obj.ambient_light_color}; '
    ambient_light += f'groundColor: {page_obj.hemispheric_color}; '
    ambient_light += f'intensity: {page_obj.ambient_light_intensity}; '
    return ambient_light

def add_partitions(page, collection):
    for x, d in collection.items():
        if (d['2'] == 'a-wall' or d['2'] == 'a-openwall' or
            d['2'] == 'a-window' or d['2'] == 'a-door' or d['2'] == 'a-slab' or
            d['2'] == 'a-stair'):

            layer = page.layer_dict[d['layer']]
            d['PART'] = d.get('PART', layer[5])
            d['p-pool'] = {}
            if d['PART'] == '':
                d['PART'] = layer[5]
            if d['PART'] != 'default':
                try:
                    component_pool = page.part_dict[d['PART']]
                    if component_pool:
                        d['p-pool'] = component_pool
                except:
                    pass

    return collection
