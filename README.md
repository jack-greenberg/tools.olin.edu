# *Tools.Olin* Project Proposal
Jack Greenberg

*A redesign and backend-restructuring of tools.olin.edu to include ability to sign up for trainings and better manage user-tool authorizations.*

## MVP
- A front-end that allows students to...
  - ...see the tools they are trained on
  - ...sign up for trainings
  - ...request training times
- A back-end that allows NINJA’s and shop staff to…
  - ...create trainings for a specific time and tool
  - ...cancel/modify trainings
- A back-end that allows shop staff to…
  - ...create new training types
  - ...add new tools
  - ...update training types
- Accessibility, Speed

## Nice to have
- Email/Slack/SMS Notifications
- Onboarding for first-time users

## Overview
Phase|Time|Deliverables
---|---|---
1 - *Research*|2 weeks|Updated list of requirements surveyed from shop staff, NINJAs, and students
2 - *Back-end Architecture*|4 weeks|SQL database, data processing, site routing and request processing
3 - *Front-end Design*|4 weeks|Figma/Illustrator/InDesign files showcasing the design of the site
4 - *Front-end Development*|3 weeks|Final site complete for review
5 - *Launch*|1 day|Training for staff, NINJAs, and students

## Phase 1 - *Research*
Before diving head-first into any development, we should survey the actual users to find out what their needs are, and how they are best met. We should consider ease-of-use and functionality of the future site, as well as both advantages and pain-points of the current site.

### Action Points
- [ ] Write and send out surveys to students, NINJAs, and shop staff
- [ ] Collect and process data into a mini report

### Deliverables
- [ ] Mini report on the findings of the research
- [ ] Action points for Phase 2

## Phase 2 - *Back-end Architecture*
This phase involves developing the SQL database, the site's internal API, and the modules used by the site's backend. I will be using Python's Flask package, which allows for easy web app development, along with Jinja for templating.

### Action Points
*(After Phase 1)*

### Deliverables
- [ ] SQL database
- [ ] Site APIs
- [ ] Page router
- [ ] Base page templates

## Phase 3 - *Front-end Design*
Phase 3 involves the actual UX/UI of the site. This will focus on accessibility, organization, and ease of use. Designs will be modular to allow for modular development in Phase 4. 

### Action Points
*(After Phase 2)* 

### Deliverables
- [ ] Figma, Illustrator, or InDesign files detailing design standards and design choices

## Phase 4 - *Front-end Development and Integration*
Once we have the designs, the next step is implementation. One consideration for this phase is the use of JavaScript. There are pros and cons, namely speed-cost versus power, so this is a discussion to be had as we approach Phase 4. If JavaScript will be used, it will likely be a combination of plain (vanilla) JavaScript and ReactJS. This phase will also include continuous integration of the frontend and backend via AJAX requests to the internal API. Styling will be done using Sass (SCSS). Node Package Manager (npm) will be used to handle dependencies.

### Action Points
*(After Phase 3)* 

### Deliverables
- [ ] The final site

## Phase 5 - *Launch*
Now that the site is built, we need to train users and launch the site. There will be detailed documentation for each class of users (shop staff, NINJAs, students), but much of the use of the site should be fairly apparent on the site (i.e. the site should be easy to use and functionality should be obvious).

### Action Points
*(After Phase 4)* 

### Deliverables
- [ ] A short training for the site for shop staff, NINJAs, and students

## Phase 6 - *Beyond*
Beyond the initial launch of the site, a number of features could be added, including:
- Email/SMS/Slack notifications for training additions and cancelations
