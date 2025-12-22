# Hosting file links for createCreation (Google Drive)

1. Build the final file locally (ZIP or PNG).
2. Upload the files to a Google Drive folder (via UI or API).
3. Mark each file as "anyone with the link can view".
4. Build the direct link using the Drive `fileId`:
   - `https://drive.usercontent.google.com/download?id=<FILE_ID>&export=download&confirm=t&filename=<filename.ext>`
   - Alternative: `https://drive.google.com/uc?export=download&id=<FILE_ID>&filename=<filename.ext>`
5. Links in `fileUrls`/`imageUrls` MUST expose the extension (`.zip`, `.png`, etc.) to avoid "Unknown" names in the dashboard.
6. Each field accepts up to 10 URLs. For additional files beyond `fileUrls`, attach them later with `createBlueprint`.
7. Keep files public while the API pulls them; adjust permissions afterward based on your policy.
