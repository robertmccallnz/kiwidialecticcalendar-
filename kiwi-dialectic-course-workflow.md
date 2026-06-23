# The Kiwi Dialectic course workflow

## What this system does
The Kiwi Dialectic now has a working course infrastructure split across two layers:

1. **Substack** is where the actual course lives, where posts are published, and where access is controlled.
2. **GitHub calendar** is the public schedule layer, where readers can see what is coming, subscribe to the timetable, and click through to the correct Substack lesson.

The simple rule is this:

**Substack controls access. The calendar controls visibility and routing.**

That means the calendar can tell readers a course exists, but it does not decide who gets to read it. That decision is made by the post visibility in Substack.

## The three access types
Use these three labels consistently across the workflow.

### 1. Public
- Substack post visibility: **Everyone**
- Calendar `access`: `public`
- Calendar button text: **Open lesson**

### 2. Free subscriber
- Substack post visibility: free subscribers
- Calendar `access`: `free_subscriber`
- Calendar button text: **Subscribe free to access**

### 3. Paid
- Substack post visibility: paid subscribers
- Calendar `access`: `paid`
- Calendar button text: **Upgrade to unlock**

## Standard workflow
1. Create the course in the Courses section on Substack.
2. Decide whether the course is public, free-subscriber, or paid.
3. Set the real gate on the Substack posts.
4. Add the course and lessons to `courses.json`.
5. Regenerate the ICS file or let GitHub Actions do it.
6. Check the live calendar page and links.
7. Publish the course announcement and explain access clearly.

## Required fields in `courses.json`
Each course should carry:
- `title`
- `slug`
- `status`
- `access`
- `calendar_visibility`
- `description`
- `lessons`

Each lesson should carry:
- `title`
- `date`
- `time`
- `location`
- `access`
- `calendar_visibility`
- `teaser`
- `link`

## House rule
- Public courses: show full details on the calendar.
- Free-subscriber courses: show full title, date, and a clear subscribe-free button.
- Paid courses: show title, date, and teaser, but keep the premium material on Substack.
- Sensitive or unfinished courses: mark as hidden until ready.

## Key principle
**Substack is the school gate. GitHub calendar is the timetable on the wall.**
