---
name: Speed up prepare download
overview: Yes — most of the “Preparing” time is work before bytes transfer, and downloads run one track at a time. We can cut that prep overhead without turning on risky multi-track community parallelism.
todos:
  - id: lazy-songlink
    content: Fetch GetStreamingURLs only when trying Tidal/Amazon, not before the whole auto loop
    status: completed
  - id: cache-streaming-urls
    content: Session-cache GetStreamingURLs / Songstats results by Spotify track ID (in-memory)
    status: completed
  - id: skip-meta-refetch
    content: Skip per-track Spotify metadata refetch when queue track already has needed fields
    status: completed
  - id: prefetch-next
    content: Prefetch next track ISRC/streaming URLs while current track downloads (still one download at a time)
    status: completed
  - id: preparing-stage-ui
    content: Show preparing stage text in toast/Details so prep work is visible
    status: completed
  - id: readme-note
    content: Document speedups in README-changes.md
    status: completed
isProject: false
---

# Speed up preparing and downloading

## What “Preparing” is today

The toast label **Preparing** is not a separate mode. In [`frontend/src/components/DownloadProgressToast.tsx`](frontend/src/components/DownloadProgressToast.tsx) it shows whenever the queue is processing **and** no download bytes have been counted yet (`mb_downloaded === 0`).

So “Preparing” covers all of this **before** the FLAC stream starts:

```mermaid
flowchart LR
  skip[Parallel existing-file check] --> meta[Per-track Spotify metadata refetch]
  meta --> isrc[ISRC resolve]
  isrc --> songlink[song.link scrape for Tidal/Amazon]
  songlink --> try[Try sources in auto order]
  try --> bytes[Bytes transfer shown]
```

Batch downloads in [`frontend/src/hooks/useDownload.ts`](frontend/src/hooks/useDownload.ts) are **strictly sequential** (`for` + `await downloadWithItemID`). Existing-file checks are already parallel; the track loop is not.

Hard limits we will **not** fight in this change:

- Community download APIs rate-limit and schedule breaks (seen as long “waiting … before retry” waits in Go). Parallelizing many community downloads usually hits the break sooner.
- Identity / duration checks after download stay as-is.

## Highest-impact speedups (chosen approach)

Confirmed by bottleneck mapping ([Map download prepare bottlenecks](7b4f7907-f166-4114-ad85-65f878c94a5c)): the largest prep cost is uncached SongLink/Songstats scraping; community downloads must stay sequential.

### 1. Lazy `song.link` / streaming URL fetch

Today auto mode always calls `GetStreamingURLs` **before** trying any source whenever Tidal or Amazon appear in the order ([`useDownload.ts`](frontend/src/hooks/useDownload.ts) ~771–779), even if Qobuz would have succeeded and never needed those URLs.

Change: fetch streaming URLs **only when entering the Tidal or Amazon branch**. If the order is `qobuz-…` and Qobuz succeeds, song.link is skipped entirely for that track.

Also apply the same change in `downloadWithAutoFallback`.

### 1b. Session-cache streaming URLs by Spotify ID

`GetAllURLsFromSpotify` / Songstats currently have **no URL cache** (unlike ISRC, which already uses a DB cache). Add an in-process map keyed by Spotify track ID (frontend helper and/or Go side of `GetStreamingURLs`) so retries, prefetch, and fallback paths do not scrape song.link twice for the same track.

### 2. Skip redundant Spotify metadata refetch

Every queued track currently re-fetches `https://open.spotify.com/track/{id}` even when the artist discography already provided artists, album artist, release date, track number, UPC, etc. ([`downloadWithItemID`](frontend/src/hooks/useDownload.ts) ~697–724).

Change: only call `fetchSpotifyMetadata` when required fields are missing (or when a template needs something not on the track). Artist batch downloads like Hariprabodham (498 tracks) avoid hundreds of extra Spotify round-trips.

### 3. Prefetch the next track while the current one downloads

While track _N_ is transferring, start a background prep for track _N+1_: ISRC resolve + (if needed) streaming URLs. Store results in a small in-memory map keyed by Spotify ID and consume them in `downloadWithItemID`.

Keep concurrency at **one active community download** so we do not accelerate rate-limit / break. This only overlaps network prep with transfer time.

### 4. Clearer preparing stages (small UX)

Update the toast (and/or Details panel activity) so “Preparing” can show a short stage such as `Resolving links…` / `Starting Tidal…` instead of a blank spinner. Same wall-clock, less “stuck” feeling.

## What we will not do in this pass

- Multi-track parallel community downloads (would need a careful concurrency setting and still fights shared cooldowns).
- Changing community retry / break policy.
- Removing identity/duration validation.

## Immediate setting tip (no code)

If most tracks have ISRCs, putting **Qobuz first** in auto order already reduces prepare time today, because Qobuz does not need song.link. Lazy fetch (item 1) makes Tidal-first orders less punitive when Qobuz ends up being the winner.

## Files to touch

- [`frontend/src/hooks/useDownload.ts`](frontend/src/hooks/useDownload.ts) — lazy streaming URLs, conditional metadata, next-track prefetch
- [`frontend/src/lib/download-activity.ts`](frontend/src/lib/download-activity.ts) / [`DownloadProgressToast.tsx`](frontend/src/components/DownloadProgressToast.tsx) — optional stage text
- [`README-changes.md`](README-changes.md) — short note on the speedups

## Success criteria

- Artist discography batches spend less time in “Preparing” per track (no duplicate Spotify fetch when data is present; no song.link when Qobuz succeeds first).
- Still one download at a time; cooldown / identity behavior unchanged.
- Hariprabodham-style run still skips existing files in parallel at batch start.
