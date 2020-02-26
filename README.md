# *Tools.Olin* Project Proposal
Jack Greenberg

## Objective

A redesign and backend-restructuring of tools.olin.edu to include better usability for shop staff, students, and NINJAs. The project will also be well-documented to allow for students or other developers to continue work in the future.

### MVP
- Front-end that shows who is trained to use what tools
  - This already exists on the current site; we will most likely port this over from the current site and adapt it with new tools
- Admin portal that allows for students to be marked as trained in batches on multiple tools at once, as well as functionality to add and remove tools
  - The current system is difficult to manage for shop staff, so an improved system will make workflows easier, and will eventually allow for more features

### Possible Extensions
- Allow NINJAs and staff to post trainings and allow students to sign up for them
- Email/Slack/SMS notifications for trainings

## Timeline
Phase|Time|Deliverables
---|---|---
*User System, Database / UX/UI*|6 weeks|Database, user system with profiles/permissions, user stories, workflows, wireframes, user testing
*Design / API*|4 weeks|Figma/Illustrator designs, API for site-server communication
*Front-end / Back-end integration and deployment*|4 weeks|HTML, CSS, ReactJS, JavaScript for the site's front-end

## Phase 1: *User System, Database / UX/UI*
This phase will include developing the user/permissions system so that we can create different user profiles that have different capabilities. For instance, we could have *shop staff*, *NINJAs*, *students*, and any other group we would need. Each of those profiles would have access to parts of the backend. This will also include the database set up, in which we will create profiles for tools and trainings.

On the front-end side, this will involve developing workflows, user stories, and basic wireframes. Workflows and user stories will help lay the path for site interaction modules. There will also be user testing in the form of interviews or surveys of shop staff and NINJAs to see what the ideal workflow is for the site.

## Phase 2: *Design / API*
For the backend, this phase involves developing an API for the site to query data from the database. This includes data processing and appropriate JSON structure to ensure the easiest processing in the frontend. This will also involve the page router and development of any "helper modules" that will aid server management.

For the frontend, this will include the development of Figma, Illustrator, or InDesign mockups. This will highlight the user-facing functionality of the site for each category of user. Either each page will be displayed, or a few example pages and a general set of design guidelines.

## Phase 3: *Front-end / Back-end integration and deployment*
For the final phase, the frontend will be developed using HTML, CSS, and JavaScript. We will then integrate the front and backend by adding AJAX API queries to create the final product.

Once that is done, we will deploy it to the server and set up the HTTP daemon that will handle all requests and direct them to our Python app file. This part will likely need to be coordinated with IT to ensure that everything is secured and the processes can run uninterrupted.



---

## 02/18 Design Review

Design review took place with NINJAs and machine shop staff.

* Would be nice to check off multiple people on a single page, like on the tools page
* Use yellow color for incomplete
* Automatically have a box for who did what (checking off) and when, but have the ability to change the values
* If NINJA and trainee are not in the same place, the following should happen:
  * After checking off the test piece, NINJA puts in their password, then the student can go to their page, check the disclaimer box, and enter their password to sign
* Make it easy to change tools
* If a student hasn't completed their testpiece at the end of a semester, the training should be unchecked