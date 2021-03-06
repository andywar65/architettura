# architettura.APP

A basic BIM as a [Django 2.1.3](https://www.djangoproject.com/) / [Wagtail 2.3](https://wagtail.io/) app that imports [CAD](https://en.wikipedia.org/wiki/AutoCAD_DXF) files and renders Virtual Reality using [A-Frame 0.9.2](https://aframe.io) library.
The repository is archived due to a security issue in Wagtail.

### How to get DXF files

DXF files are drawing exchange files, and they are human readable (if in ASCII format). Obviously you will need a CAD if you want to generate your own files. For free I recommend [NanoCAD](http://nanocad.com/) even if you won't be able to work with solids. It doesn't matter, you won't need them. Unfortunately open source CAD projects never match the industry.

Lots of programs deal with DXF, but the goal here is to have blocks with attributes (data!), not just surfaces. Refer to the DXF constraints paragraph to understand what your files have to look like.

### Install Wagtail app

The app can be cloned or downloaded from [Github](https://github.com/andywar65/architettura). Using a shell get into the project folder and type  `git clone https://github.com/andywar65/architettura`. Add `architettura` to the INSTALLED_APPS in your settings file. Migrate and Collectstatic. The app's templates look for a `base.html` file, so be sure to have one. [Django-colorful](https://github.com/charettes/django-colorful) is also required: type `pip install django-colorful` and add `colorful` to the INSTALLED_APPS. You must add a style tag in `{python root}/lib/site-packages/wagtail/admin/templates/wagtailadmin/pages/_editor_css.html` to display correctly color boxes. Style tag can be found in `static/architettura/css/_editor_css.html`.

### DXF constraints

Generate a DXF in ascii mode and don't try to modify it. DXF is a sequence of key / value pairs, and deleting just one line can break up everything. By now only 3Dfaces and standard blocks (see further) can be translated, other entities will just be ignored. Create as many layers as you need, and place your entities on the desired one. Layers relate to the appearance of the entity, how it's explained in the backend paragraph.

To include meshes, explode them to 3Dfaces (I know it's bad, but this is how it works by now). If you have an Acis solid, use `3DCONVERT` to obtain a mesh, then explode it. In alternative you can build a OBJ-MTL or GLTF block.

### Wagtail backend

Create a page of the `Dxf Page` kind. You will have to enter a Title and introduction.
In the Source section load the most important stuff: the DXF file. It will be stored in the `media/documents` folder. Don't check the `Block` box and eventually insert URL of a CDN with CORS enabled from where you want to eventually [serve 3D model files](https://aframe.io/docs/0.9.0/introduction/hosting-and-publishing.html#hosting-models).
Save and view the page. Your file has been already transformed into VR. If you want to look around, press mouse button, then just move the mouse. To move around press the `W-A-S-D` keys. Notice that entities inherit the original layer color. Ok, now let's go back to editing the page.
Notice that the `Block` box is now checked, this means that if you view the page again, the program will skip the DXF and read it's database: DXF layers have been imported (you can change the color, and add new layers), and there is a list of all the entities extracted from the DXF. The list is a little bit cryptic, but you can change the appearance and position of any entity from here, and even add new ones.

Now, to add materials, create a page of the `Scene Page` kind. You will have to enter a Title plus other page informations (Intro, Image, Author and date).
In the VR Settings panel first select how you want to move around in the scene, with keyboard input or clicking on checkpoints (see interaction), then choose the DXF Page that you want to render. Then you will have to check if you want your shadows on, if you want your camera to be able to fly and if 3D faces must be double sided.
In the Ambient Setting panel load the Equirectangular Image for the VR background (if none, a default one will be picked). Equirectangular images are like those planispheres where Greenland is bigger than Africa. You can also set ambient background colors and lights.

Okay, now publish and go to the frontend to see how your model behaves. At first it should look like in the Dxf Page, apart from how you move around (see Interaction and Checkpoint paragraphs). Now get back to editing the page.

You should notice thet layers have been imported from the Dxf Page. At first entities inherit the original DXF color, but you can change that associating `Materials` and `Partitions` to layers (see next paragraph). You can set them to `Invisible` if you want to turn them off. If you set them to `Wireframe`, all entities on that layer will display only edges. If you set `No shadows` entities on the layer will be unaffected by lighting.

### Materials and Partitions

You saw thet layers in Scene Page can load materials and partitions. These are external pages that can be shared by different Scenes. It is convenient to prepare your own materials in advance.
Each `Material Page` can contain as many `Components` as you want. A Component needs a Name, an Image and a Color. If the image is a 1x1 meter pattern, check the appropriate box. Default color is `white`, but you can change it with the color picker. Color affects appearance of the image. Entities use Components in different ways, some blocks use up to three components for different surfaces. In example, a whole room uses the first component for the paint on walls and the ceiling, the second for tiled surfaces and the third for skirting and pavement.
`Partitions` are taken in account only during surveys (see further). Also Partitions have `Components`, but they refer more to physical characteristics, like `thickness` and unit `weight`. Partition displays what your wall or slab is made of.

### Interaction, keyboard mode

The model window is embedded within your website, but you can go fullscreen by pressing `F` or the visor icon in the right bottom corner of the window. On some mobiles the image will be split in two, with stereoscopic effect. You will need one of those cardboard headgears to appreciate the effect. Press `ESC` to exit fullscreen mode. On laptops, if you want to look around, press mouse button, then just move the mouse. To move around press the `W-A-S-D` keys. On some devices you literally walk to explore the model, but I've never experienced that. Some elements like Doors have animations, just click on them.
Last but not least, press the `Ctrl+Alt+I` to enter the Inspector mode, that makes you inspect and modify the entities of the model. Modifications can be saved to HTML files.
Notice that under the model window you have some lists, with links to surveys (see further), materials and partitions used in the scene.

If you click a `Material`, a mockup scene will be presented, showing how different entities react to inspected material. Similarly, the `Partition` displays a sample of a wall made of different layers.

### Checkpoint mode

In this mode interaction has a different behaviour: keyboard movements are disabled, and you move around clicking on (or gazing at on mobiles) checkpoint entities. Any entity may be transformed into a checkpoint by associating it to a `animation block` with `PROPERTY` set to `checkpoint`in CAD.

### Nesting Pages

When you have several `Scene Pages` you can collect them under a `Scene Index Page`. These pages act like a blog index. Style is borrowed by the [Bakery](https://github.com/wagtail/bakerydemo) CSS, modify it for your needs. Eventually uncomment `navigation_tags` from the templates, it's not a Wagtail native tag.

## Entities

### Lines & Polylines

Lines are very simple entities. In CAD you can assign line color, otherwise it inherits layer color. If line has `thickness`, it is transformed into a plane (see Standard blocks). In this case line must be on X-Y plane or parallel. Polylines are a sequence of lines, and work pretty much the same.

### Standard blocks

Standard blocks may be found in `static/architettura/samples/standard-blocks.dxf` bundled within the app: box, cylinder, cone, sphere, circle, plane, look-at, text, links, curvedimage and lights. These mimic entities of the A-Frame library, with unit dimensions. Insert the block and scale it to the desired width, length and height. You can rotate it along all axis (previous limitations solved thanks to [Marilena Vendittelli](http://www.dis.uniroma1.it/~venditt/)). You can explode some of the standard blocks without affecting geometry: they will degrade to a series of 3D faces.

Standard blocks come with attributes that affect their geometry. In CAD, attributes are prompted when inserting a block, and can be modified in the Property window. To understand how attributes affect geometry, refer to [A-Frame Documentation](https://aframe.io/docs/0.9.0/primitives/a-box.html) .

`a-light` standard block has a `TYPE` attribute which can be set to ambient, directional, point and spot. Directional light is best suited for shadowing. Scale light block to modify shadow camera frustum. Refer to [A-Frame Light Component Documentation](https://aframe.io/docs/0.9.0/components/light.html) for further details.

`a-text` standard block is a text centered in a bounding plane. The attributes control alignment, content and wrap count, which is the number of letters that fill the width of the bounding plane.

`a-camera` standard block lets you choose the position of the camera. Only first camera will be rendered, if no camera is found a standard one will be placed at (0, 0, 0).

`a-link` standard block allows you to link different pages on a click. The `LINK` attribute lets you select among parent, previous, next and first child page. If target has an equirectangular image (see backend paragraph) it will appear in the link. You can also write an URL in the `LINK` field.

`a-curvedimage` standard block is an open cylinder where you can project panoramic images.

`a-animation` standard block animates the blocks that have same insertion point in CAD file. Refer to [A-Frame Animation Component Documentation](https://aframe.io/docs/0.9.0/core/animations.html) for further details on animation attributes. Apart from regular animations, `PROPERTY` can be set to `checkpoint`, `look-at`, `event` and `stalker`.
`Checkpoint` transforms into checkpoints the blocks that have same insertion point in CAD file. Checkpoints are useful to move you around in `digitalkOmiX mode` (see before). Thanks to [Don McCurdy](https://github.com/donmccurdy/aframe-extras) for the component.
`Look-at` and `stalker` have similar behaviour. First gazes towards the camera or given `TARGET`, latter stalkers the camera and may have a `TEXT` in a balloon or a `LINK` (dismissed function at the moment).
`Event` animation connects two entities with given `ID`. On click first entity emits an event targeting second entity, that triggers animation with `startEvents` equal to first `ID`. Thanks to [Supermedium](https://github.com/supermedium/superframe/tree/master/components/animation/examples/events) for the component.

`a-mason` standard block transforms lines and polylines with thickness and a-planes into `Wall` surfaces (see further). To work it has to be attached at insertion point of a-plane or at origin of line or polyline.

### Blocks and BIM standard blocks

`Blocks` are a parametric assembly of primitives. In CAD you just have a bounding box with an insertion point, but setting the `NAME` attribute leads to different results. There will be a list of block types (default is t01 = simple table). `MATERIAL` attribute defines block appearance, other `PARAMETERS` define functionalities peculiar to each block.

You can load a Wavefront OBJ file setting block `NAME` to `obj-mtl` and `PARAM1` to the OBJ filename. OBJ and MTL must have same filename and must be loaded to media/documents with lowercase extension. New standard is GLTF. Set the `NAME` to `gltf` and `PARAM1` to the GLTF filename.

BIM (Building Information Management) standard blocks are recognized as real life building elements. By now we have `Wall`, `Slab`, `Door`, `Window` and `Stair` BIM entities. If you put a `Door/Window` inside a `Wall`, you get a `Openwall`.

In a Wall block you can define it's `PART` to set the partition type (physical characteristics) and `MATERIALs` for interior and exterior surfaces. A single material can describe three stripes of the same wall surface. In Slabs a single material describes ceiling and floor patterns.

Doors can be hinged or sliding, single or double. Geometry and behaviour are defined in CAD (block dimension and attributes), appearance is defined by `MATERIAL`. If you set `PART` attribute to `ghost`, door is not rendered. If a door panel is clicked, an animation is triggered. Windows are similar, but they also have a `SILL`, representing the height of the window sill from the floor. Wall underneath will inherit the material from the wall entity you have poked.

### Survey Pages

A `Survey Page` is useful to calculate surfaces and weights. Create a Survey and select the Scene you want to survey. Save and view the survey. A table of entities is displayed, with informations regarding materials, partitions and dimensions, along with weights of walls and slabs if you provided them with a `Partition`. You can copy and paste the table to a spreadsheet to calculate surfaces and volumes. Edit again the Survey Page: you will notice that Scene Page Layers have been imported, with the ability to exclude them from the survey. This is pretty handy, because you can have multiple surveys targeting the same Scene, taking into account different dimensional aspects (i.e. Demolitions and Reconstructions).
