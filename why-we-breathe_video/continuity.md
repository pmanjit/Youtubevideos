# Continuity and Style Lock

## User-provided reference images

- `refs/user-cozy-textured.png` — cozy interior, blue sofa, warm lamp, soft hand-drawn texture.
- `refs/user-cinematic-storytime.png` — illustrated cave/fire scene, deeper blue/orange lighting and textured backgrounds.
- `refs/user-expressive-comic.png` — simple white round-headed stick figure with black line body, minimal expressive face, and bold contour.

## Approved production anchors

The user approved the corrected stick-character tests as the anchor direction. The first human-like test is rejected and must not be used as a subject reference.

- **Style anchor:** `refs/style-test-03-stick-character.png`
- **Character anchor:** `refs/user-expressive-comic.png`, reinforced by the figure in `refs/style-test-03-stick-character.png`
- **Ancient-shore setting anchor:** `refs/style-test-04-stick-character-ancient.png`
- **Modern living-room setting reference:** `refs/user-cozy-textured.png`

### Exact prompt — approved style/character test 03

Create ONE single 16:9 frame for an illustrated science story. Main character MUST match the supplied expressive-comic reference's character design: a very simple cartoon stick figure, oversized smooth white circular head, tiny black oval eyes, curved black brows, small simple mouth, thin black line torso and limbs, simple white hands, no realistic anatomy, no detailed human body, no clothing, no hair. Preserve the reference's recognizable proportions and bold hand-drawn black ink contours; pose can change. Scene: the stick figure stands beside a softly drawn cozy living-room sofa, one hand resting on the chest while taking a thoughtful breath; a few pale-blue curved air lines approach the nose, and a small warm yellow glow marks the chest. Use an off-white/cream paper background, muted slate-blue sofa, restrained mustard-yellow accent behind the figure, subtle paper grain, and sparse stippled shadow. Keep room details simplified and secondary so the stick figure is the focal point. Eye-level medium-wide shot, clear single instant, no panels. Do not render the character as a realistic or normally proportioned human; do not add realistic facial features or anatomical detail. No text, labels, captions, logos, or watermark.

### Exact prompt — approved ancient-shore test 04

Create ONE single 16:9 illustrated science-story frame, not a collage. Recurring narrator character MUST match the supplied expressive-comic reference exactly in design: oversized smooth white circular head, tiny black oval eyes, simple curved brows and small mouth, thin black stick-figure torso and limbs, simple white hands; no realistic human proportions, no detailed anatomy, no hair, no clothing. The character is a curious guide at the edge of an ancient shallow shoreline, carefully looking down at a patch of tiny blue-green microbial mats in the water. Microbes are simple rounded cell-like forms with no faces. Show a deep blue early ocean, dark volcanic shore and a warm orange sunrise on the horizon; one tiny pale-yellow glint hints at the oxygen story without symbols or labels. The character should be recognizably the same design as the reference, with an appropriate changed pose and curious expression. Hand-drawn 2D story illustration, bold slightly irregular black ink contours, warm cream/ochre and orange against slate blue/deep navy, soft cel-like shading, restrained paper grain, atmospheric but legible background, character as clear focal point, medium-wide low eye-level composition. No photorealism, 3D, glossy gradients, text, captions, logos, or watermark.

## Locked STYLE block — copy verbatim into every final frame prompt

Hand-drawn 2D editorial story illustration on lightly textured off-white paper. Dark, slightly irregular black ink contours, medium-bold outer contour with finer interior marks. Warm cream and ochre balanced with slate blue, deep navy, and restrained orange accents. Soft cel-like shading with subtle paper grain; warm motivated light for interiors and orange dawn/fire, cool blue shadow for night/ancient water. Backgrounds use simplified storybook shapes with moderate detail, kept subordinate to the focal subject. Clear silhouettes and one readable action per frame; expressive but not exaggerated. No photorealism, no 3D, no glossy gradients, no realistic human anatomy, no clothing on the recurring guide, no text or labels.

## Locked CHARACTER identity — copy verbatim whenever the guide appears

Recurring guide: the same simple stick figure shown in the approved anchors: oversized smooth white circular head, thin black stick torso and limbs, simple white hands, tiny black oval eyes, simple curved brows and small mouth; no hair, no clothes, no realistic anatomy, no human body proportions. Preserve exact head-to-body proportions, contour weight, and facial-feature simplicity across all appearances. Vary only pose, gaze, and expression to fit the current beat.

## Location invariants

- **Modern living room:** warm beige walls, blue upholstered sofa, wooden side table, yellow throw, warm lamp; restrained furnishings, no legible screen text.
- **Ancient shoreline:** deep blue shallow water, dark volcanic rocks, warm ochre/orange horizon haze; no modern objects or invented plants/animals.
- **Cellular-scale explanatory imagery:** clean simplified cell and mitochondrion shapes, membrane boundaries and electron/energy flows rendered as small glowing dots or restrained colored paths; no formulas or labels. Keep representations metaphorical and visually clear, not photorealistic.

## Rejected test

- `refs/style-test-01-breathing.png` — rejected by user because its normally proportioned human character does not match the intended stick-figure character. Do not use as an identity reference.

## State

Style and character anchors approved. Final shot prompts are compiled in `visuals.csv`. Frame production is underway; continuity references remain authoritative.

## Continuity invariants

- The guide remains a white circular head on a thin black stick body, with minimal face marks and no hair or clothing.
- The guide's proportions, facial construction, line weight, and contour treatment do not drift; only pose, expression, and gaze vary by shot.
- Oxygen-related metaphorical dots/paths may be warm orange or pale blue; do not render written symbols, letters, or chemical formulas.
- Alternative metabolisms use distinct, simple visual clues (e.g., sulfur/mineral colors, mud, or dissolved compounds) without implying that all life uses oxygen.
- Modern and ancient locations remain visually distinct; no modern artifacts in ancient scenes.
