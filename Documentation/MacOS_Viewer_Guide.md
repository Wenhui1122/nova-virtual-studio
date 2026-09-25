# Presenting the Studio on macOS

## Quick start

The project download is a ZIP archive, not an installer. Extract it before opening the files. Local file links stop working if the corresponding files are moved or deleted.

1. Locate `NOVA_Mac_Viewer.html` in the extracted project folder.
2. Right-click it and choose **Open With → Safari** or **Microsoft Edge**. No server, dependencies, or internet connection are required.
3. Drag to orbit. Use the mouse wheel or a two-finger vertical trackpad gesture to zoom.
4. Select **Desk detail**, then enable **Wireframe** to inspect the actual triangulated mesh.
5. Disable **Trusses & lights** to uncover the backdrop, or hide other layers to isolate the desk.
6. Select **Present** to hide the sidebar, or **Save view as PNG** to export the current image.

The HTML contains all geometry, rendering code, and a fallback image. Copying this single file to another computer is enough to present the model. It does not require adjacent OBJ or PNG files. If a file preview shows source code, open the downloaded file directly in a browser rather than in an editor or GitHub's source preview.

## Keyboard controls

Click the model or focus the canvas with Tab before using these controls:

| Key | Action |
| --- | --- |
| Arrow keys | Orbit the camera |
| `+` or `=` | Zoom in |
| `-` | Zoom out |
| `R` | Restore the overview |

## Fallback preview

If an embedded preview does not execute JavaScript, or WebGL cannot initialize, the page retains a static image and instructions. Open the original HTML in Safari or Edge for interactive viewing. If the graphics context is interrupted, reload the page. The PNG files in `Preview/` can also be opened in macOS Preview.

## Suggested presentation sequence

Overview → Front view → Desk detail → Hide unrelated layers → Enable wireframe → Explain your modifications.

The viewer displays the actual project geometry and changes the viewing angle in real time; it is not a prerecorded video. It does not edit vertices, execute MAXScript, or save native `.max` files. Use the original Max script or OBJ for further modelling.

## Verification scope

Geometry checks and embedded JavaScript syntax checks have been completed. Viewer-exported images are included in the repository. A comprehensive Safari/Edge compatibility test has not been performed. The automated browser tool could not open local file URLs, so no automated browser acceptance test is claimed.
