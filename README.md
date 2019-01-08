# architettura.APP

A basic BIM as a [Django 2.1.3](https://www.djangoproject.com/) / [Wagtail 2.3](https://wagtail.io/) app that imports [CAD](https://en.wikipedia.org/wiki/AutoCAD_DXF) files and renders Virtual Reality using [A-Frame 0.8.2](https://aframe.io) library.

### How to get DXF files

DXF files are drawing exchange files, and they are human readable (if in ASCII format). Obviously you will need a CAD if you want to generate your own files. For free I recommend [NanoCAD](http://nanocad.com/) even if you won't be able to work with solids. It doesn't matter, you won't need them. Unfortunately open source CAD projects never match the industry.

Lots of programs deal with DXF, but the goal here is to have blocks with attributes (data!), not just surfaces. Refer to the DXF constraints paragraph to understand what your files have to look like.

### Install Wagtail app

The app can be cloned or downloaded from [Github](https://github.com/andywar65/architettura). Using a shell get into the project folder and type  `git clone https://github.com/andywar65/architettura`. Add `architettura` to the INSTALLED_APPS in your settings file. Migrate and Collectstatic. The app's templates look for a `base.html` file, so be sure to have one.

### DXF constraints

Generate a DXF in ascii mode and don't try to modify it. DXF is a sequence of key / value pairs, and deleting just one line can break up everything. By now only 3Dfaces and standard blocks (see further) can be translated, other entities will just be ignored. Create as many layers as you need, and place your entities on the desired one. Layers relate to the appearance of the entity, how it's explained in the backend paragraph.

To include meshes, explode them to 3Dfaces (I know it's bad, but this is how it works by now). If you have an Acis solid, use `3DCONVERT` to obtain a mesh, then explode it.

### Wagtail backend

Create a page of the `Scene Page` kind. You will have to enter a Title plus other page informations (Intro, Image, Author and date). In the VR Settings panel load the most important stuff: the DXF file. It will be stored in the `media/documents` folder. Then you will have to check if you want your shadows on, if you want your camera to be able to fly and if 3D faces must be double sided. In the Ambient Setting panel load the Equirectangular Image for the VR background (if none, a default one will be picked). Equirectangular images are like those planispheres where Greenland is bigger than Africa. You can also set ambient background colors and lights.

At first entities inherit the original layer color, but you can change that associating Materials to layers. Layers are extracted from DXF first time you view the page, set them to `Invisible` if you want to turn them off. Each `Material Page` can contain as many `Components` as you want. A Component needs a Name, an Image and a Color. If the image is a 1x1 meter pattern, check the appropriate box. Default color is `white`, but you can use hexadecimal notation (like `#ffffff`) or standard HTML colors. Color affects appearance of the image. Entities use Components in different ways, but be sure that a Material has at least three components.

Okay, now publish and go to the frontend to see how your model behaves.

### Interaction

The model window is embedded within your website, but you can go fullscreen by pressing `F` or the visor icon in the right bottom corner of the window. On some mobiles the image will be split in two, with stereoscopic effect. You will need one of those cardboard headgears to appreciate the effect. Press `ESC` to exit fullscreen mode. On laptops, if you want to look around, you have to press and drag the mouse. To move around press the `W-A-S-D` keys. On some mobiles you literally walk to explore the model, but I've never experienced that. Some elements like Doors have animations, just click on them.
Last but not least, press the `Ctrl+Alt+I` to enter the Inspector mode, that makes you inspect and modify the entities of the model. Modifications can be saved to HTML files.

### Nesting Pages

When you have several `Scene Pages` you can collect them under a `Scene Index Page`. This page acts like a blog index. Style is borrowed by the [Bakery](https://github.com/wagtail/bakerydemo) CSS, modify it for your needs.

### Lines

Lines are very simple entities. In CAD you can assign line color, otherwise it inherits layer color. If line has `thickness`, it is transformed into a plane (see Standard blocks). In this case line must be on X-Y plane or parallel.

### Standard blocks

Standard blocks may be found in `static/architettura/samples/standard-blocks.dxf` bundled within the app: box, cylinder, cone, sphere, circle, plane, look-at, text, links, curvedimage and lights. These mimic entities of the A-Frame library, with unit dimensions. Insert the block and scale it to the desired width, length and height. You can rotate it along all axis (previous limitations solved thanks to [Marilena Vendittelli](http://www.dis.uniroma1.it/~venditt/)). You can explode some of the standard blocks without affecting geometry: they will degrade to a series of 3D faces.

Standard blocks come with attributes that affect their geometry. In CAD, attributes are prompted when inserting a block, and can be modified in the Property window. To understand how attributes affect geometry, refer to [A-Frame Documentation](https://aframe.io/docs/0.8.0/primitives/a-box.html) .

Light standard block has a `TYPE` attribute which can be set to ambient, directional, point and spot. Directional light is best suited for shadowing. Scale light block to modify shadow camera frustum. Refer to [A-Frame Light Component Documentation](https://aframe.io/docs/0.8.0/components/light.html) for further details.

Look-at standard block is a plane that always faces the camera.

Text standard block is a text centered in a bounding plane. The attributes control alignment, content and wrap count, which is the number of letters that fill the width of the bounding plane.

Link standard block allows you to link different pages on a click. The `TREE` attribute lets you select among parent, previous, next and first child page. If target has an equirectangular image (see backend paragraph) it will appear in the link.

Curvedimage standard block is an open cylinder where you can project panoramic images.

Animation standard block animates the blocks that have same insertion point in CAD file. Refer to [A-Frame Animation Component Documentation](https://aframe.io/docs/0.8.0/core/animations.html) for further details on animation attributes.

### Blocks and BIM standard blocks

`Blocks` are a parametric assembly of primitives. In CAD you just have a bounding box with an insertion point, but setting the `TYPE` attribute leads to different results. There will be a list of block types (default is t01 = simple table). `MATERIAL` attribute defines block appearance, other `PARAMETERS` define functionalities peculiar to each block.

You can load a Wavefront OBJ file setting block `TYPE` to `obj-mtl` and `PARAM1` to the OBJ filename. OBJ and MTL must have same filename and must be loaded to media/documents with lowercase extension. If set, `MATERIAL` attribute overrides MTL.

BIM (Building Information Management) standard blocks are recognized as real life building elements. By now we have `Wall`, `Slab` and `Door` BIM entities. If you put a Door inside a `Wall`, you get a `Openwall`.

In a Wall block you can define it's `TYPE` to set the partition type (physical characteristics, TODO) and `MATERIALs` for interior and exterior surfaces. A single material can describe three stripes of the same surface. In Slabs a single material describes ceiling and floor patterns.

Doors can be hinged or sliding, single or double. Geometry and behaviour are defined in CAD (block dimension and attributes), appearance is defined by `MATERIAL`. If you set `TYPE` attribute to `ghost`, door panel is not rendered. If a door panel is clicked, an animation is triggered.

### Next improvements

Complete a-tree block.
