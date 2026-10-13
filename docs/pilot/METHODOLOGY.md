# Sources and Verification

[Overview](README.md) · [All metrics](METRICS.md) · [Data](data/)

The CampusLense pilot ran **from 1 to 10 October 2026 inclusive**. Project lead Nurkhan confirmed the period and clarified that the summary figures describe completed-pilot results. The publication package applies that correction.

Source: "CampusLense: pilot preparation, execution, and evidence" (English translation of the source title), pages 21–26. Source SHA-256: `4b51a47aac70db53320e4a8d13e93c1e5743a3a8e617463d1a05d7f4b218062c`. The original document is preserved. The hash identifies the document; it is not an analytics provider's attestation of the results.

## Corrections applied

- One period throughout: 1–10 October 2026, ten days.
- Ten daily rows map to the period in source order; their values are unchanged.
- Figures are presented as completed-pilot results following the project lead's confirmation.
- NPS is recalculated from 7 promoters, 9 passives, and 5 detractors: `(7 − 5) / 21 × 100 = +9.52`, or +10 rounded. The original +9 display is retained only in source information.
- Percentages use explicit denominators where available. Markdown normally uses one decimal place; NPS uses two and CSV values retain up to four.
- The three summary-report images use the packaged aggregates. Three additional screenshots show the local Umami overview, events, and sessions. Original event collection and import history are not independently verified; native counters remain separately identified in the image gallery.
- The separate $8.44 tariff calculation is excluded from pilot results because it does not appear in the summary's final expense table.

## Metric definitions

An account means a successful sign-in. Activation means an account with at least one completed profile. The 418 successful builds and 263 unique universities describe different quantities; rebuilding a university does not add a unique university.

The daily table contains new visitors, successful sign-ins, and successful builds. The funnel also includes sign-in starts and activated accounts. Session duration of 220 seconds is a median, not a mean.

D1 is 25 / 104; D7 is 5 / 54 for the early cohort. Feature use remains in percentages because the summary does not explicitly specify a common denominator. Feature percentages are not converted into event counts. Countries describe requested universities. Feedback themes can overlap.

## Available records and verification scope

The package contains aggregate results, rating distributions, and feedback themes. Original analytics events, individual survey responses, task logs, and provider invoices are outside the package. Project lead confirmation and arithmetic checks do not replace independent reconciliation against those records.

Offline checks cover daily totals, the 497 build requests, funnel percentages, NPS, sample sizes, criteria, links, images, layouts, and checksums. Verification does not generate profiles, call paid APIs, or modify Git history.

Build outcomes preserve the summary's categories: 418 + 47 + 32 = 497. Without task logs, overlap between a user leaving and a background build completing cannot be checked separately. The report adds no unsupported error explanations, participant identities, or individual reviews.

## Umami interface changes

The interface was set to English, the website display name was set to CampusLense, and categorical source assertions in the interface were removed following the project lead's correction. The chart note now states the pilot period and the project lead's confirmation. These are presentation and annotation changes; recorded event counts, visitor identifiers, routes, and timestamps were not rewritten. Removal of interface text does not independently establish event provenance.
