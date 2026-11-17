# Step 2: Storage

Everything for this setup goes in one folder, the **system folder**. Inside
it: a `Profile` folder (the user's eight profile files), an `Applications`
folder (one dated folder per application) and the tracker sheet. Nothing for
this setup is kept outside it (decision 020).

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
     onboarded. Read `settings.yaml`, check the tracker link opens, then go
     to "Where to start" in `SKILL.md`.
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
   - Create the system folder, then `Profile` and `Applications` inside it.
5. The tracker sheet is created in the system folder too (see "Tracker
   sheet").
6. Say in one line where everything ended up, and save the links in
   `settings.yaml` (see "Save").

## Profile folder

1. Create `Profile` in the system folder.
2. Upload each file in this skill's `templates/profile/` folder into it,
   with the same name, as plain text: `contentMimeType: text/plain` and
   `disableConversionToGoogleType: true`. They must not become Google Docs;
   the collector reads them as raw text.
3. List the folder and confirm all eight files are there: `profile.yaml`,
   `facts.md`, `wants.md`, `voice.md`, `stories.md`, `answers.md`,
   `sources.yaml`, `settings.yaml`.

## Output folder

Create `Applications` in the system folder. Each application gets a dated
folder inside it.

## Tracker sheet

The tracker is a copy of the template sheet, which has the collector script
inside it. See `template-sheet.md` in this folder for the link.

- **If a template link is listed there:** give the user the link (it ends
  in `/copy`), ask them to click "Make a copy", name it (suggest `Job
  Search Tracker`), and paste the new sheet's URL back here. Then move the
  copy into the system folder (move it yourself if the connector can, or
  ask them to drag it in). A copy keeps
  the script; a new blank sheet would not.
- **If no template link is listed:** use the paste-in path (decision 019).
  It needs no template and no tools beyond the Drive connector.

  1. Create a blank Google Sheet in the system folder named
     `Job Search Tracker`, using the Sheets connector. If
     it cannot create sheets, ask the user to create a blank one and paste
     its URL.
  2. Read `bundle/Code.gs` in this skill's folder. It is one file holding the
     whole collector (about 100 KB). Give it to the user as a file they can
     open, or in pieces if the chat cannot hold it. Never retype or edit it.
  3. Walk the user through, one step at a time:
     - Open the sheet, then Extensions > Apps Script.
     - Click in the editor, select all (Ctrl/Cmd+A) and delete the default
       code.
     - Paste the bundle and click Save (the disk icon). Name the project
       `Job Search Collector` if asked.
     - Close the Apps Script tab and reload the sheet. A **Job Search** menu
       appears after a few seconds.
  4. Ask them to run **Job Search > Set up template**. The first time, Google
     asks them to authorize the script; tell them that is expected, and that
     the script only reads the profile folder, reads alert emails with the
     label they choose, and writes to this sheet. On the "Google hasn't
     verified this app" screen they choose Advanced, then Go to the project
     (the script is their own copy). Setup builds the Leads, Applications,
     Run Log and Seen tabs.
  5. Continue with "Once the user has a tracker URL" below, skipping its
     first item (the tabs now exist).

  If the user runs into trouble, ask what the Apps Script editor shows. Do
  not ask them to edit the code.

Once the user has a tracker URL:

1. Read the Leads tab's header row to confirm it is the tracker (it has a
   Lead ID column). If the tabs are missing, ask the user to open the sheet
   and run Job Search > Set up template, then check again.
2. Ask the user to open the sheet and run **Job Search > Set profile
   folder**, pasting the profile folder's URL (show it on its own line,
   with nothing after it). The first time, Google asks
   them to authorize the script. Tell them that is expected, and be
   accurate about it: Google's screen lists broad access (Drive, Gmail,
   connecting to outside sites) because that is how Apps Script asks. What
   the script's code does is read the profile folder, read and label alert
   emails that carry their alert label, call the job sources they turn on,
   and write to this sheet. The code is in the repo for anyone to check.
3. Ask them to run **Job Search > Check configuration** and tell you what
   it says. Warnings about empty files are expected at this point.

## Save

Write `locations.system_folder_url`, `locations.tracker_sheet_url` and
`locations.output_folder_url` (the `Applications` folder) into
`settings.yaml`, leaving every other line as it is.
