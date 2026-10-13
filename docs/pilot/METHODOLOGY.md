# Pilot Methodology

[Overview](README.md) · [All metrics](METRICS.md) · [Data](data/)

CampusLense ran an applicant pilot **from 1 to 10 October 2026 inclusive**. This report brings together product analytics, profile-build outcomes, the pilot survey and feedback collected during those ten days.

## Data and reporting

- **Analytics:** visitors, sign-in activity, product events, sessions and return usage. The [Umami screenshots](SCREENSHOTS.md#umami-overview) show the overview, events and sessions for the pilot period.
- **Profile builds:** requests, outcomes, processing time and university coverage.
- **Survey:** 21 responses, including usability, recommendation likelihood, overall satisfaction and feature ratings.
- **Feedback:** thematic counts from messages and bug reports.

The CSV tables contain the report's aggregate metrics and distributions. Summary graphics are rendered from these tables; Umami screenshots show the analytics interface. These two image types are identified in the [gallery](SCREENSHOTS.md).

## Definitions and denominators

An account is a successful sign-in. An activated account has at least one completed university profile. The **418 successful builds** and **263 unique universities** measure different things: multiple builds can refer to the same university.

The daily table contains new visitors, successful sign-ins and successful builds. Funnel stages also include sign-in starts and activated accounts. The 220-second session duration is a **median**; the Umami overview's 170-second figure is an **average**.

- Visitor-to-account conversion: **131 / 486 = 27.0%**.
- Account activation: **104 / 131 = 79.4%**.
- Successful builds: **418 / 497 = 84.1%**. The outcome table contains 418 successes, 47 abandoned waits and 32 failures.
- Next-day return (D1): **25 / 104 = 24.0%**; any event on the next calendar day after activation.
- Day-seven return (D7): **5 / 54 = 9.3%**; the cohort activated on days 1–3 has a complete seven-day observation window.

The CSV denominator field contains a count or a named population where defined; an empty field means no denominator is specified for that metric. Feature-use percentages are not converted into unique account counts. Country shares describe **requested universities**, rather than visitor geography. Feedback themes can overlap, so mentions are not summed as distinct people.

## Survey and rounding

Survey results describe **21 respondents**. Feature-rating distributions group scores into 9–10, 7–8, 5–6 and 0–4; the displayed means are the survey's mean ratings.

NPS uses 7 promoters, 9 passives and 5 detractors:

`(7 − 5) / 21 × 100 = +9.52`, or **+10** rounded to an integer. The CSV uses this calculated value consistently.

Percentages normally use one decimal place in the report, two for NPS, and up to four in the CSV tables. Expenses retain the **$30–70** range used in the pilot budget review.

## Report checks

The offline verifier checks daily totals, build outcomes, percentage calculations, survey group sizes, success criteria, links, images and file checksums. The dashboard is standalone and makes no external requests.

The pilot met **four of eight** criteria. D7 return, NPS, the Ellis test and build success remained below target; the [metrics](METRICS.md#pilot-criteria) and [pilot review](README.md#what-the-pilot-showed) retain those results.
