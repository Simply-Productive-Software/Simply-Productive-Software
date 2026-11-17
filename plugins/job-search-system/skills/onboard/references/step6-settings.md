# Step 6: Output

`settings.yaml` already holds the defaults for output and review. This step
checks the part the user cares about with them.

1. Ask which file formats they want for drafts (`output.formats`; default
   Google Doc and PDF; the others are Word `.docx` and plain markdown).
   Mention that PDFs exported from the Google Doc parse well in application
   portals, and that some portals ask for Word files.
2. Show the default folder and file names for one example job, using their
   own name from `profile.yaml`: the folder (`output.folder_name`, default
   `{date} {employer} - {title}`), the resume (`output.resume_file_name`) and
   the cover letter (`output.cover_letter_file_name`). Change them only if
   the user asks.
3. Leave everything else at the defaults. Say that any value can be changed
   later by asking.

Save `settings.yaml`, changing only the lines they chose (read it, then write
the new version as `shared/profile.md` says), and confirm it parses.
