# Step 2: Storage

Everything for this setup goes in one folder, the **system folder**. Inside
it: a `Profile` folder (the user's eight profile files), an `Applications`
folder (one dated folder per application) and the tracker sheet. Nothing for
this setup is kept outside it (decision 020). This step creates all of it.

## Choose or create the system folder

1. **Look first.** Search Drive for existing setups with the search in
   `shared/profile.md` ("Finding them"). Do not read inside other folders.
2. **Ask, with the options in front of them:**
   - **Use an existing one.** Offer each system folder you found (name and
     where it sits), and "one I name or paste a link to".
   - **Create a new one.**
   If you found none, offer only "create a new one" and "use a folder I
   already made (paste the link)".
3. **They chose an existing one:**
   - It has a `Profile` folder with a `profile.yaml`: they have already
     onboarded. Read `settings.yaml`, check the tracker link opens and its
     Config tab has `core_schema_version` (`shared/tracker.md`), then go to
     "Where to start" in `SKILL.md`. If there is no tracker, build one as
     below.
   - It has no profile yet (an empty folder they made): use it as the
     system folder and create `Profile`, `Applications` and the tracker
     inside it.
   - They pasted a folder that holds `profile.yaml` itself: that is the
     profile folder. Its parent is the system folder. Say so and confirm.
   - Older layout (a `Job Search Profile` and a `Job Search Applications`
     folder side by side, no system folder): treat their parent as the
     system folder. Move nothing. Everything keeps working as it is.
4. **They chose to create one:**
   - Ask: "What should the folder be called?" Offer the default, **Job
     Search System**. Use what they say.
   - Ask where it goes, with the options: a folder they name or paste, a
     suggestion from their Drive (list top-level folders with
     `parentId = 'root' and mimeType = 'application/vnd.google-apps.folder'`
     and suggest up to three parents that fit, such as one named for
     projects, career or job search, with a reason each), or **My Drive**
     (the default if they have no preference or say "you pick").
   - If a folder with that name already exists in that place, do not create
     a second one quietly. Ask: use that one, or pick another name.
   - Create the system folder (Drive `create_file` with the folder mime type
     `application/vnd.google-apps.folder` and `parentId`), then `Profile` and
     `Applications` inside it.
5. Build the tracker sheet in the system folder (next section).
6. Upload the Profile files (section after that).
7. Say in one line where everything ended up.

## Tracker sheet

Build it from scratch. There is no template to copy and nothing for the user
to paste (decision 028). The layout is in `shared/tracker-schema.yaml`.

1. **Create a blank Google Sheet** named `Job Search Tracker` inside the
   system folder. Use the Sheets connector's create tool if it has one and
   move the sheet into the system folder. Otherwise use Drive `create_file`
   with the spreadsheet mime type `application/vnd.google-apps.spreadsheet`
   and `parentId` set to the system folder. If neither can create a sheet,
   ask the user to create a blank sheet named `Job Search Tracker` in the
   system folder and paste its link, then go on in that sheet.
2. **Tabs.** Rename the first tab `Leads`. Add `Applications` and `Config`.
3. **Headers.** Write row 1 of Leads and Applications from the schema,
   column names exactly as written and in the schema's order.
4. **Config.** Write `Key` and `Value` in row 1, then two rows:
   `core_schema_version` with the value from the schema file, and
   `profile_folder_id` with the Profile folder's ID.
5. **Formatting**, in one batch update where the tool allows it:
   - Leads and Applications: frozen header row, bold with a light gray fill.
   - Leads Status: a strict dropdown with the six statuses from the schema,
     colored by status (green Applied, yellow Ready and Parked, gray
     Skipped and Closed).
   - The other dropdowns the schema lists (Work mode and Review result on
     Leads; Channel, Stage reached and Outcome on Applications).
   - Wider columns for Title, Employer, Notes and Next action.
   - Hide the Config tab.
   Keep every tab a plain range. Never make a Google Sheets table.
6. **Read it back.** Read row 1 of each tab and the Config rows. Confirm the
   header names match the schema, the Config values are right, and the Status
   dropdown exists. If the tabs, headers or Config are wrong, fix them. If
   only a nicety did not take (a color, a width, hiding Config), tell the user
   in one line and go on. If the tools cannot create or write the sheet at
   all, stop: say which connector or permission is missing and that onboarding
   continues from step 2 once it is fixed. Do not leave a half-built sheet
   without saying so.

Dates in the tracker are text in `YYYY-MM-DD` (`shared/tracker.md`).

## Profile folder

1. Create `Profile` in the system folder.
2. Take each file in this skill's `templates/profile/` folder. For
   `settings.yaml`, fill in `locations.system_folder_url`,
   `locations.tracker_sheet_url` and `locations.output_folder_url` (the
   `Applications` folder) before uploading, leaving every other line as it is.
3. Upload each file into `Profile` with the same name, as plain text:
   `contentMimeType: text/plain` and `disableConversionToGoogleType: true`.
   They must not become Google Docs.
4. List the folder and confirm all eight files are there: `profile.yaml`,
   `facts.md`, `wants.md`, `voice.md`, `stories.md`, `answers.md`,
   `sources.yaml`, `settings.yaml`.

Show each link on its own line (see "How to run the interview steps" in
`SKILL.md`).

## Output folder

`Applications` is created in the system folder above. Each application gets
a dated folder inside it when a draft is saved.
