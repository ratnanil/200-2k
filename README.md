# Training Dashboard

A single-file web app that pulls cycling activities from Strava and visualises weekly progress against a structured training plan.

## What it does

- Connects to Strava via OAuth (one-time setup, then automatic)
- Fetches all cycling activities (Ride, VirtualRide, GravelRide, MountainBikeRide, EBikeRide)
- Shows this week's actual distance / elevation / longest ride / ride count vs the planned targets
- Lists the individual planned rides for the current week (type, date, distance, elevation)
- Renders a Plan vs Actual chart covering the full training block
- Renders historical charts for the last 16 weeks with the plan target as a dynamic goal line
- Falls back to fixed user-defined goals for weeks outside the training block
- Caches activity data in `localStorage` for 30 minutes; manual sync available

## Files

```
index.html   — the entire app (HTML + CSS + JS, no build step, no dependencies to install)
README.md    — this file
```

All runtime dependencies are loaded from CDN:
- [Chart.js 4.4.0](https://www.chartjs.org/) — charts

## Setup

### 1. Host the file

The app needs a real URL because Strava's OAuth redirect cannot target `file://`.

**GitHub Pages (recommended)**
1. Push this repo to GitHub
2. Go to Settings → Pages → Source: `main` branch, root folder
3. Your URL: `https://<username>.github.io/<repo>/`

**Local development**
```bash
python3 -m http.server 8080
# open http://localhost:8080
```

### 2. Create a Strava API application

1. Go to [strava.com/settings/api](https://www.strava.com/settings/api)
2. Create an app (name and description are arbitrary)
3. Set **Authorization Callback Domain** to your hostname, e.g. `<username>.github.io` or `localhost`
4. Note your **Client ID** and **Client Secret**

### 3. First-time app setup

Open the app in a browser. The setup screen asks for:
- Strava Client ID and Client Secret
- Fallback weekly goals (used for weeks outside the training block)

Click **Connect with Strava**, authorise in the Strava popup, and you land on the dashboard. Credentials and tokens are stored in `localStorage` on that device only — nothing is sent anywhere except Strava's own API.

Repeating setup on a new device (e.g. phone) takes about 30 seconds.

## Updating the training plan

The plan is a plain JS array at the top of the `<script>` block in `index.html`:

```js
const TRAINING_PLAN = [
  { date: "2026-03-10", type: "Commute",   km: 56,  hm: 0   },
  { date: "2026-03-12", type: "Hills",     km: 40,  hm: 500 },
  { date: "2026-03-15", type: "Long ride", km: 70,  hm: 700 },
  // ...
];
```

| Field  | Type   | Description                          |
|--------|--------|--------------------------------------|
| `date` | string | ISO date `YYYY-MM-DD`                |
| `type` | string | `"Commute"`, `"Hills"`, `"Long ride"` (controls badge colour) |
| `km`   | number | Planned distance in kilometres       |
| `hm`   | number | Planned elevation gain in metres     |

Weeks are derived automatically from the date using ISO week numbers (Monday–Sunday). To add a new training block, replace or extend the array and push — no other changes needed.

To add a new ride type with a custom badge colour, add an entry to `TYPE_STYLE`:

```js
const TYPE_STYLE = {
  "Commute":   { bg: "#e0f2fe", fg: "#0369a1" },
  "Hills":     { bg: "#fef3c7", fg: "#92400e" },
  "Long ride": { bg: "#f3e8ff", fg: "#7c3aed" },
  "Race":      { bg: "#fce7f3", fg: "#9d174d" }, // example
};
```

## Architecture notes

**No backend.** The app is a static HTML file. All state lives in the browser's `localStorage`:

| Key              | Content                                      |
|------------------|----------------------------------------------|
| `client_id`      | Strava app Client ID                         |
| `client_secret`  | Strava app Client Secret                     |
| `access_token`   | Short-lived Strava access token              |
| `refresh_token`  | Long-lived token used to renew access tokens |
| `token_expiry`   | Unix timestamp of access token expiry        |
| `activities`     | Cached array of ride objects                 |
| `cached_at`      | Timestamp of last activity fetch             |
| `goals`          | User-defined fallback weekly goals (JSON)    |

**Token refresh** happens automatically on page load when the access token is expired or about to expire (within 60 seconds).

**Activity filtering** keeps only activities whose `type` or `sport_type` field is in `RIDE_TYPES`. Virtual rides and e-bike rides are included; runs, swims, etc. are ignored.

**Week aggregation** uses ISO 8601 week numbers (weeks start on Monday). The key format is `YYYY-WWW`, e.g. `2026-W11`.

## Current training block

10 weeks, KW 11–20 (10 March – 17 May 2026). Structure: Commute + Hills + Long ride each week, with recovery weeks at weeks 4 and 8. Peak week targets 200 km / 2000 m elevation.
