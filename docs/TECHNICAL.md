# CampusLense: retrieval, verification and the LOCUS case

CampusLense was developed for LOCUS Case 01, **Visual University Profile**. The
globe is the entry point; the technical deliverable is a useful visual profile
whose photographs retain sources, categories and uncertainty. The original
[case](../materials/LOCUS-Case-01.pdf) and [regulations](../materials/LOCUS-Regulations-v2.pdf)
are retained alongside the organizer's evidence in [HACKATHON.md](HACKATHON.md).

## A profile is assembled progressively

Resolution starts with the university name and location. The retained submission
notes describe fuzzy name matching over the 14,467-university index, with aliases,
transliteration and external entity lookups. This index is a discovery resource;
it is not a claim that every indexed institution has an equally complete photo profile.

The orchestrator starts source collection in parallel and exposes partial results.
Official university pages, reference sources, image search and social/video
material provide different candidate images and evidence. External providers can
be unavailable, rate-limited or incomplete. Their response state belongs in the
inspection view, rather than being hidden behind an apparently complete gallery.

The retained source uses a Python/FastAPI backend, React/TypeScript frontend,
geographic/entity lookup and a modular `backend/app/pipeline/` implementation.
Source-specific collectors live under `pipeline/sources/`. The visual experience
combines map/globe navigation, campus imagery and provider-backed spatial views.

## Verification combines different kinds of evidence

| Layer | Role |
| --- | --- |
| Exact and perceptual hashes | Find identical and visually similar files |
| CLIP embeddings and category prompts | Provide semantic similarity and categorization evidence |
| Location, source, captions and reference images | Connect the photograph to the intended campus or city |
| Model-backed image inspection | Produce a structured place/category judgment with uncertainty |
| Curation and diversity | Choose useful images without filling a category with near-duplicates |
| Photo passport | Keep the original source and confidence reasoning inspectable |

The submission notes identify CLIP ViT-B/32 and hash/similarity-based duplicate
handling, a Gemini-backed image inspector/editor, structured text generation,
ffmpeg-based video-frame retrieval and Depth Anything V2 Small for parallax.
Those names describe the retained implementation; they are not recommendations
about the best current provider or an assertion of independent photographic certification.

Every source-derived result needs an appropriate interpretation. A camera view
can be photorealistic without proving campus boundaries. A depth map can create
parallax without changing a photograph into a surveyed 3D model. A confidence
score can support review without being a guarantee of authenticity.

## The case requirements have visible counterparts

| LOCUS task | Product evidence |
| --- | --- |
| Find a university and handle ambiguity | Search and geographic results |
| Separate practical photo categories | Campus, dormitory, classroom, library, laboratory, sport, student life and city |
| Remove duplicates and irrelevant material | Hash/embedding duplicate checks, rejection records and curation |
| Check belonging and expose uncertainty | Photo passport and verification panel |
| Preserve a clickable source and date | Source metadata when available; missing information stays visible |
| Produce a useful profile promptly | Progressive collection, cached results and the recorded interface |
| Help applicants compare daily life | Climate, city context, campus tours, comparison and saved universities |

The full [gallery](GALLERY.md) includes Street View/indoor tours, parallax photos,
mobile layouts, search settings and a shareable view that were not all visible in
the initial case-study selection.

## Measurements and a useful manual review

The team-reported internal evaluation used 223 labelled images: verification
precision/recall 0.94/0.94, category accuracy 0.95 and curated-selection accuracy
0.93. The roughly 23-second profile timing belongs to that development record.
These are internal, limited measurements, not a new test of the present hosted app.
The first-place result has separate organizer evidence in [the event record](HACKATHON.md).

To inspect the product, choose a university, open a practical photo category,
inspect one passport and compare it with the verification panel. Then examine
climate/city context and the 3D visit as separate sources of information. A new
university can have sparse or delayed material; that is a condition to inspect,
not a reason to invent missing photographs.

The hosted prototype is linked from the root README. The
[private source](https://github.com/Eye172/locus-hackathon-1) contains startup,
deployment and provider configuration; collaborator access is required at the
12 October 2026 review. The public gallery and retained walkthrough establish
the visible product experience. For an authorized local run, use the source’s
current environment templates with your own restricted provider credentials.

## Identify the retained presentation versions

- `media/CampusLense_QwertyS_presentation.pdf`: the named QwertyS package, identical
  to the source's `docs/pitch/CampusLense_QwertyS_2026_v2.pdf`.
- Its PPTX counterpart is retained for editing and review.
- `media/CampusLense_QwertyS_demo.mp4`: the package's 180-second application walkthrough.
- `media/CampusLens.pdf`: the earlier eight-slide draft, including an unfilled team label.
- `media/campuslense-demo.mp4`: the earlier 133.72-second recording.

The named package was retained in the October migration. The archive alone does
not establish which exact binary was submitted at the September deadline. The
completed applicant pilot ran from 1 to 10 October 2026; its results and evidence scope are in the [pilot report](pilot/README.md).
