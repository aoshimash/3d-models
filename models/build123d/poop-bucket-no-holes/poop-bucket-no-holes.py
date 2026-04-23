"""Remove the ventilation holes from the "Compact poop bucket S (A1, A1 mini)" STEP.

This script doesn't model the bucket from scratch — it imports the original STEP
file (Autodesk Inventor 2021 export) and uses OpenCascade's defeaturing algorithm
to delete the wall vent holes, stitching the surrounding wall surfaces back into
a hole-free solid.

Source model and license
------------------------
Original model: "Compact poop bucket S (A1, A1 mini)" by Michal (@Michal1980)
    https://makerworld.com/models/451897-compact-poop-bucket-s-a1-a1-mini

The source model is distributed under MakerWorld's **Standard Digital File
License**, which forbids sharing, hosting on other platforms, or distributing
derivative works in any digital or physical form. Consequences for this repo:

  * The source .stp file is NOT included in this repository. You must download
    it yourself from the MakerWorld page above and accept the license.
  * The STL produced by this script (in ./output/) is a derivative work and
    MUST NOT be redistributed, uploaded to other platforms, or shared. It is
    gitignored here on purpose. Keep it local, print it for personal use only.
  * Commercial use of the model or any derivative is not permitted.

Only this Python script itself — which contains no geometry from the original
model, just a generic BRep transformation recipe — is tracked in git.

How it works
------------
1. Load the STEP file with build123d's `import_step`, yielding one `Solid`.
2. Enumerate every face; keep the cylindrical faces whose radius falls in the
   vent-hole range. In the source geometry every vent hole is represented as a
   single analytical cylinder face of radius ≈ 1.65 mm, so a narrow band around
   that radius uniquely identifies them without touching fillets, pegs, or the
   outer body curvature.
3. Feed all those faces to `BRepAlgoAPI_Defeaturing`. The algorithm removes the
   selected faces and extends the adjacent wall surfaces to close the gaps
   analytically (no tessellation, no BSpline patching), so the output face count
   drops by exactly the number of holes removed.
4. Export the resulting solid to STL (for your personal, non-redistributed use).

Running
-------
    cd models/build123d
    uv run python poop-bucket-no-holes/poop-bucket-no-holes.py

The source STEP path defaults to ~/Downloads/. Override with a CLI arg if it
lives elsewhere:

    uv run python poop-bucket-no-holes/poop-bucket-no-holes.py /path/to/bucket.stp
"""

from __future__ import annotations

import sys
from pathlib import Path

from build123d import GeomType, Solid, export_stl, import_step
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.BRepAlgoAPI import BRepAlgoAPI_Defeaturing
from OCP.TopTools import TopTools_ListOfShape

try:
    from ocp_vscode import show
except ImportError:
    show = None


# --- Source file (mm geometry — STEP units are already mm in the input) ---
DEFAULT_SOURCE_STEP = Path.home() / "Downloads" / "Compact poop bucket S (A1, A1 mini).stp"

# --- Hole detection (mm) ---
# Vent holes in the source are r = 1.65 mm cylinder faces. Use a ±0.05 mm band
# to tolerate STEP rounding without accidentally matching the 1.5 mm or 2.0 mm
# cylinders that belong to other features (pegs, small fillets).
HOLE_RADIUS_NOMINAL = 1.65
HOLE_RADIUS_TOLERANCE = 0.05

OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_STL = OUTPUT_DIR / "poop-bucket-no-holes.stl"


def _cylinder_radius(face) -> float | None:
    """Return the analytical radius of a cylinder face, or None if not a cylinder."""
    if face.geom_type != GeomType.CYLINDER:
        return None
    surf = BRepAdaptor_Surface(face.wrapped)
    return surf.Cylinder().Radius()


def find_vent_hole_faces(solid: Solid) -> list:
    """Return every face that looks like a vent hole (cylinder of radius ≈ 1.65 mm)."""
    lo = HOLE_RADIUS_NOMINAL - HOLE_RADIUS_TOLERANCE
    hi = HOLE_RADIUS_NOMINAL + HOLE_RADIUS_TOLERANCE
    hits = []
    for face in solid.faces():
        r = _cylinder_radius(face)
        if r is not None and lo < r < hi:
            hits.append(face)
    return hits


def remove_faces(solid: Solid, faces_to_remove: list) -> Solid:
    """Return a new solid with the given faces removed via OCCT defeaturing."""
    df = BRepAlgoAPI_Defeaturing()
    df.SetShape(solid.wrapped)
    face_list = TopTools_ListOfShape()
    for f in faces_to_remove:
        face_list.Append(f.wrapped)
    df.AddFacesToRemove(face_list)
    df.SetRunParallel(True)
    df.Build()
    if not df.IsDone():
        raise RuntimeError("BRepAlgoAPI_Defeaturing failed to remove the requested faces")
    return Solid(df.Shape())


def patch_bucket(step_path: Path) -> Solid:
    source = import_step(str(step_path))
    solids = source.solids()
    if len(solids) != 1:
        raise RuntimeError(f"Expected exactly one solid in {step_path}, got {len(solids)}")
    original = solids[0]

    holes = find_vent_hole_faces(original)
    print(f"Found {len(holes)} vent-hole faces (r ≈ {HOLE_RADIUS_NOMINAL} mm).")
    if not holes:
        raise RuntimeError("No vent holes detected — the radius tolerance may need widening.")

    patched = remove_faces(original, holes)
    print(
        f"Faces: {len(original.faces())} → {len(patched.faces())} "
        f"(Δ {len(original.faces()) - len(patched.faces())}). "
        f"Volume: {original.volume:.2f} → {patched.volume:.2f} mm³ "
        f"(Δ {patched.volume - original.volume:+.2f})."
    )
    return patched


def main() -> None:
    step_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SOURCE_STEP
    if not step_path.exists():
        raise FileNotFoundError(
            f"STEP file not found: {step_path}\n"
            f"Pass a path as the first argument, or place the file at the default location."
        )

    patched = patch_bucket(step_path)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    export_stl(patched, str(OUTPUT_STL))
    print(f"Exported: {OUTPUT_STL}")

    if show is not None:
        try:
            show(patched)
        except Exception as exc:  # viewer not running is fine
            print(f"(ocp_vscode viewer not connected: {exc})")


if __name__ == "__main__":
    main()
