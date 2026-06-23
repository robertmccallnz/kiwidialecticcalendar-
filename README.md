# The Kiwi Dialectic calendar repo

This repository runs the public course calendar for **The Kiwi Dialectic**.

It does four jobs:

1. Hosts a public browser-view calendar page with GitHub Pages.
2. Stores the editable course and lesson data in `courses.json`.
3. Generates a subscribable `.ics` calendar feed for Google Calendar, Apple Calendar, and Outlook.
4. Documents the workflow for running public, free-subscriber, and paid courses through Substack.

## Live URLs

### Browser calendar
`https://robertmccallnz.github.io/kiwidialecticcalendar-/github-calendar-connector.html`

### ICS subscription feed
`https://raw.githubusercontent.com/robertmccallnz/kiwidialecticcalendar-/main/the-kiwi-dialectic-courses.ics`

## File map

- `github-calendar-connector.html` — the public calendar page served by GitHub Pages.
- `courses.json` — the source of truth for courses, lessons, access labels, and links.
- `the-kiwi-dialectic-courses.ics` — the generated calendar feed for subscriber apps.
- `scripts/generate_ics.py` — the script that builds the ICS file from `courses.json`.
- `.github/workflows/refresh-events.yml` — GitHub Actions workflow for rebuilding the ICS file.
- `how-to-subscribe-calendar.md` — copy for Substack explaining how readers subscribe to the calendar.
- `kiwi-dialectic-course-workflow.md` — the operating guide for how courses, Substack access, and the calendar fit together.

## Core rule

**Substack is the school gate. GitHub calendar is the timetable on the wall.**

Substack decides who can read a course.
The GitHub calendar shows what exists, when it runs, and where readers should click.

## Access types

There are three access states used across the repo.

### `public`
Use when anyone can read the lesson.

- Substack visibility: Everyone
- Calendar button: Open lesson

### `free_subscriber`
Use when a reader must subscribe for free before reading.

- Substack visibility: Free subscribers
- Calendar button: Subscribe free to access

### `paid`
Use when the lesson is for paid subscribers.

- Substack visibility: Paid subscribers
- Calendar button: Upgrade to unlock

## How to add a new course

1. Create the course inside the **Courses** section on Substack.
2. Decide whether the course is public, free-subscriber, or paid.
3. Publish or schedule the lesson posts with the correct Substack visibility.
4. Add the course and lesson entries to `courses.json`.
5. Include real Substack post URLs in the `link` fields.
6. Run the ICS generator or let GitHub Actions rebuild the feed.
7. Check the live calendar page.
8. Test the browser page, lesson buttons, and ICS feed.

## JSON pattern

```json
{
  "title": "Gramsci for Aotearoa",
  "slug": "gramsci-for-aotearoa",
  "status": "Live",
  "access": "free_subscriber",
  "calendar_visibility": "public",
  "description": "Power, hegemony, institutions, and counter-power from below.",
  "lessons": [
    {
      "title": "Lesson 1: Why read Gramsci now?",
      "date": "2026-07-07",
      "time": "19:00",
      "location": "Substack email",
      "access": "free_subscriber",
      "calendar_visibility": "public",
      "teaser": "Free subscribers can read the lesson in the Courses section.",
      "link": "https://your-substack-link"
    }
  ]
}
```

## Visibility rules

- `calendar_visibility: public` → appears on the public calendar and in the ICS feed.
- `calendar_visibility: hidden` → does not appear publicly.

Use `hidden` for unfinished, internal, or sensitive material.

## Editing rules

- Keep titles clean and readable.
- Use real publication links, not placeholders, once a post exists.
- For paid courses, use teasers in the calendar rather than dumping full premium material publicly.
- For free-subscriber courses, make the calendar language clear: readers can see the lesson, but must subscribe free to open it.

## Release checklist

Before every course launch:

- Course intro post is ready.
- Lesson posts are drafted or scheduled.
- Access type is set.
- `courses.json` is updated.
- ICS file is rebuilt.
- Calendar page renders correctly.
- Buttons link to the right Substack pages.
- Access language matches reality.

## If something breaks

### The page loads but course data looks wrong
Check `courses.json` for missing commas, broken quotes, wrong field names, or bad links.

### The lesson appears publicly when it should not
Check `calendar_visibility` in both the course and lesson data.

### The button language is wrong
Check the `access` value in `courses.json`.

### A reader can see the listing but cannot read the lesson
That is usually correct behavior if the lesson is subscriber-only or paid. The gate is on Substack, not on GitHub.
