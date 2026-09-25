# Modelling Exercises and Presentation

## Design rationale

The curved backdrop focuses attention on the anchor desk. The two-level stage establishes hierarchy through height, colour, and illuminated trim. Navy, off-white, and cyan distinguish structure, work surfaces, and display elements. The front area leaves room for camera props; the overhead trusses communicate the scale and function of a broadcast studio. This is a stylized modelling exercise, not a construction specification.

## Three suggested modifications

### 1. Reshape the anchor desk

Save a separate copy as `NovaStudio_Personal_v01.max`. Hide unrelated layers and select the object whose name begins with `Desk tapered body`. Enter the Editable Poly **Vertex** sub-object level. In the front view, select the upper vertices and scale them along X to change the taper. Keep the worktop and illuminated trim wide enough to cover the body.

If you apply a small Chamfer to outer contour edges, save a copy first and inspect the corners for intersections. Do not chamfer every triangulation edge at once.

Deliverable: before-and-after screenshots from the same view, with a short explanation of which vertices changed and why. The source geometry is triangulated; do not describe it as an all-quad mesh.

### 2. Refine the LED backdrop and colour palette

In the Material Editor, change `NOVA_Screen` and `NOVA_Cyan` to develop a deliberate personal palette. Check whether the illuminated trim competes with the main subject. Move or scale individual data bars to balance the visual density on the two sides. Preserve gaps between screen modules and avoid intersections with the trim.

Deliverable: two palette variations and a short explanation of foreground/background hierarchy. Standard Material self-illumination changes the material's appearance; it does not provide physically accurate illumination of surrounding objects.

### 3. Adjust cameras and organize the scene

Reposition `NOVA Presenter Camera` and its target to create a clean composition around the desk, signage, and stage edge. Add a close-up camera for the desk's rounded corners and front inset. Refine object names, hide geometry that distracts from the presentation, and save a personal final version.

Deliverable: an overview, a desk close-up, and a viewport image with edges visible. Adjust lights for the renderer you actually use; the supplied script only configures basic Scanline lighting.

## Modelling methods to explain

- **Anchor desk:** a rounded rectangular profile extruded between lower and upper vertex rings. Scaling the upper ring creates the taper. The body, trim, and worktop are separate objects.
- **LED wall:** short annular sectors with inner and outer surfaces, top and bottom surfaces, and closed ends, arranged around a shared centre.
- **Stage:** elliptical profiles extruded along Z; changing height and radii produces the steps.
- **Trusses:** cylinders aligned between endpoint pairs form longitudinal chords and repeated diagonal braces.
- **Camera props:** box-shaped housings, cylindrical lenses, and three angled cylindrical legs create recognizable silhouettes at a consistent scale.

## Two-minute demonstration

1. Show the overview and explain the studio zones and scale.
2. Hide unrelated layers and show the desk assembly and your modifications.
3. Enable Wireframe or Edged Faces and explain the trade-off between curve segmentation and mesh complexity.
4. Show the second camera view and a render you saved yourself.
5. Identify the AI-assisted generated baseline and the specific edits and verification you completed personally.

## In-application acceptance checklist

- [ ] The script runs without errors; eight geometry layers and two viewing cameras are present.
- [ ] Units are centimetres and object dimensions are consistent.
- [ ] Individual desk or screen objects allow vertex and polygon editing.
- [ ] There are no obvious reversed faces, black surfaces, or overlapping-surface flicker; materials display correctly.
- [ ] F9 produces a render without cropping the main subject.
- [ ] The scene has been saved as `.max` and successfully reopened.
- [ ] Personal before-and-after comparisons and final screenshots have been retained.

## Portfolio wording

After actually completing customization and software verification, adapt the following statement to match your work:

> Virtual Studio Scene Modelling — Developed and customized an AI-assisted studio scene in 3ds Max, refining the anchor desk, modular LED backdrop, and stage layout. Organized editable geometry and materials, and prepared camera views for presentation.

Keep only the actions you completed. Running a generated script alone does not establish independent manual modelling experience, and this new project should not be backdated as an earlier course achievement.

## API references

- [Autodesk Editable Mesh and construction from vertex/face arrays](https://help.autodesk.com/cloudhelp/2021/ENU/3DSMax-MAXScript/files/GUID-0532C071-4401-4846-8450-3DA5510A3883.htm)
- [Autodesk Mesh Face Methods](https://help.autodesk.com/cloudhelp/2021/ENU/3DSMax-MAXScript/files/GUID-58D1F8B6-0012-4727-AA29-B2C79EA46E16.htm)
