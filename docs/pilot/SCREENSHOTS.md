# Pilot Report Images

[Overview](README.md) · [Methodology](METHODOLOGY.md) · [Standalone dashboard](dashboard.html)

Three report views visualize the CSV tables, and three Umami screenshots show the pilot analytics interface. All views use English and cover **1–10 October 2026**.

## Overview

![Visitors, accounts, activations, and successful builds over ten days](assets/pilot-overview.png)

486 visitors, 131 successfully signed-in accounts, 104 activations, and 418 successful builds. The daily chart shows new visitors, successful builds, and sign-ins. [Daily CSV](data/daily.csv).

## Quality and retention

![Build outcomes, technical performance, and retention](assets/pilot-quality.png)

497 requests: 418 successful builds, 47 abandoned waits, and 32 failures. Median build time is 34 seconds and p95 is 96 seconds. D1 return is 24.0%; D7 return is 9.3% of the early cohort.

## Feedback

![Survey results, feature ratings, and major feedback themes](assets/pilot-feedback.png)

21 responses, SUS 71, NPS +9.52, and an overall rating of 7.3/10. Theme counts represent mentions, not unique participants.

## Umami overview

![Umami overview for 1–10 October 2026](assets/umami-overview.jpg)

486 visitors, 808 visits, 1,557 views, a rounded 14% bounce rate, and an average visit duration of 2 min 50 s. The average differs from the median session duration of 3 min 40 s used elsewhere in the report. Comparison badges use the preceding period.

## Umami events

![Umami event dashboard for the pilot period](assets/umami-events.jpg)

Event names and counts recorded during the pilot. Event counts and unique account counts are separate metrics; their definitions are described in the [methodology](METHODOLOGY.md).

## Umami sessions

![Umami sessions for the selected pilot period](assets/umami-sessions.jpg)

The session view shows visits, page views, events and device context for the selected period. [Capture metadata](data/umami-capture-info.json).
