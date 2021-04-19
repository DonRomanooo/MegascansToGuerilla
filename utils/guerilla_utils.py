# Thank's to Paul-Emile Buteau for resources and pointers
# and Dorian Fevrier's blog for some snippets and references : https://www.fevrierdorian.com/blog/

import guerilla, os
from guerilla import *
from logger import Logger


def create_render_graph(name):
    # create a default rendergraph in the guerilla document
    doc = guerilla.Document()

    # create render graph
    rg = guerilla.Node.create(name, type='RenderGraph', parent=doc)

    # tag node
    all_ = guerilla.Node.create('All', type='RenderGraphNodeTag', parent=rg)
    all_.Tag.set('All')
    all_.Lights.set(True)
    all_out = all_.createoutput()
    all_out.PlugName.set('Output')

    # surface node
    surf = guerilla.Node.create('Surface2', type='RenderGraphNodeShader', parent=rg)
    surf.Mode.set('surface')
    surf.Shader.set('Surface2')
    surf_in = surf.createinput()
    surf_out = surf.createoutput()

    # Trace node
    trace = guerilla.Node.create('Trace', type='RenderGraphNodeSet', parent=rg)
    trace.Membership.set('All,Diffuse,Reflection,Refraction')
    trace_in = trace.createinput()
    trace_in.PlugName.set('set')
    trace_out = trace.createoutput()

    # Lighting node
    light = guerilla.Node.create('Lighting', type='RenderGraphNodeSet', parent=rg)
    light.Membership.set('Lights,Shadows')
    light_in = light.createinput()
    light_in.PlugName.set('set')
    light_out = light.createoutput()

    # all -> surface
    surf_in.Plug.connect(all_out.Plug)

    # surface -> trace
    trace_in.Plug.connect(surf_out.Plug)

    # trace -> light
    light_in.Plug.connect(trace_out.Plug)

    # Layer node
    lay = guerilla.Node.create('Layer', type='RenderGraphNodeRenderLayer',
                               parent=rg)
    lay.Membership.set("layer:Layer")
    lay_vis = lay.createinput()
    lay_vis.PlugName.set('visible')
    lay_matte = lay.createinput()
    lay_matte.PlugName.set('matte')
    lay_out = lay.createoutput()

    # trace -> layer
    lay_vis.Plug.connect(light_out.Plug)

    # Output node
    out = guerilla.Node.create('Output', type='RenderGraphNodeOutput',
                               parent=rg)
    out_in = out.createinput()
    out_in.PlugName.set('Output')

    # layer -> out
    out_in.Plug.connect(lay_out.Plug)

    return rg


def import_alembic(path):
    name = os.path.basename(path)
    with Modifier() as mod:
        refNodes, topNodes = mod.createref(name, path)

    return refNodes, topNodes


def create_surface2(tex_infos, rendergraph):
    
    # load textures from load_textures method
    diffuse_path = tex_infos["Albedo"]
    normal_path = tex_infos["Normal"]
    roughness_path = tex_infos["Roughness"]
    opacity_path = tex_infos["Opacity"]
    translucency_path = tex_infos["Translucency"]

    # surface node
    surf = guerilla.Node.create('Surface2', type='RenderGraphNodeShader', parent=rendergraph)
    surf.Mode.set('surface')
    surf.Shader.set('Surface2')
    surf_in = surf.createinput()
    surf_out = surf.createoutput()

    # diffuse
    if len(diffuse_path) > 0:

        diffuse_node = guerilla.Node.create("DiffuseColor", "AttributeShader", surf)
        diffuse_node.Shader.set("Texture")
        diffuse_node.overrideinheritedattr("File", "")
        diffuse_node.File.set(diffuse_path)
    else:
        print("No diffuse map found !")

    # normal
    if len(normal_path) > 0:
        normal_node = guerilla.Node.create("Normal", "AttributeShader", surf)
        normal_node.Shader.set("NormalMap")
        normal_node.overrideinheritedattr("File", "")
        normal_node.File.set(normal_path)
    else:
        print("No normal map found !")

    # roughness
    if len(roughness_path) > 0:
        roughness_node = guerilla.Node.create("Spec1Roughness", "AttributeShader", surf)
        roughness_node.Shader.set("MaskTexture")
        roughness_node.overrideinheritedattr("File", "")
        roughness_node.File.set(roughness_path)
    else:
        print("No roughness map found !")

    # opacity
    if len(opacity_path) > 0:
        opacity_node = guerilla.Node.create("Opacity", "AttributeShader", surf)
        opacity_node.Shader.set("MaskTexture")
        opacity_node.overrideinheritedattr("File", "")
        opacity_node.File.set(opacity_path)
    else:
        print("No opacity map found !")

    # translucence
    if len(translucency_path) > 0:
        translucence_node = guerilla.Node.create("DiffuseTranslucenceColor", "AttributeShader", surf)
        translucence_node.Shader.set("Texture")
        translucence_node.overrideinheritedattr("File", "")
        translucence_node.File.set(translucency_path)
    else:
        print("No translucency map found !")


    return surf


def create_displace(tex_infos, rendergraph):

    #load textures from load_textures method
    displacement_path = tex_infos["Displacement"]


    # displace
    if len(displacement_path) > 0:
        """displace = rg.loadfile("$(LIBRARY)/rendergraph/shader.gnode")
        with guerilla.Modifier() as mod:
            mod.renamenode(displace[0], "displacement")
        displace_in = displace[0].getinputs()[0]
        displace_out = displace[0].getoutputs()[0]
        displace[0].Shader.set("Displacement")
        displace[0].Mode.set("displacement")"""

        displace = guerilla.Node.create('Displace', type='RenderGraphNodeShader', parent=rg)
        displace.Mode.set('displacement')
        displace.Shader.set('Displacement')
        displace_in = displace.createinput()
        displace_out = displace.createoutput()

        displace_node = guerilla.Node.create("Amount", "AttributeShader", displace)
        displace_node.Shader.set("MaskTexture")
        displace.Amount.overrideinheritedattr("File", "")
        displace.Amount.File.set(displacement_path)

    else:
        print("No displacement map found !")

