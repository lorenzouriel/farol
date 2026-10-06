---
name: ig-reel-downloader
description: >
  Download Instagram Reels as .mp4 videos directly into the user's workspace Notes Ideas folder,
  organized into per-post subfolders with descriptive names derived from the video caption.
  Uses fastdl.app and Chrome. Use this skill whenever the user shares an Instagram Reel URL
  and wants the video saved, or says anything like "download this reel", "save this IG reel",
  "grab this reel video", "get this Instagram video", or pastes an instagram.com/reel/ link.
  Also trigger when the user mentions downloading, saving, or extracting video from an
  Instagram Reel even if they haven't shared a URL yet — ask for the link.
  Do NOT use this skill for Instagram images or carousels — use ig-image-downloader for those.
---

# Instagram Reel Downloader

Download Instagram Reels as .mp4 videos into the user's workspace `Notes Ideas/` folder, organized into per-post subfolders. Uses fastdl.app as a video extraction service and Chrome MCP to interact with it.

## Prerequisites

- Chrome MCP must be connected and a browser available.
- The workspace network allowlist must include `media.fastdl.app` and `fastdl.app` so curl can reach the video CDN. If downloads fail, tell the user:
  > Add `media.fastdl.app` and `fastdl.app` in **Settings → Capabilities → Network allowlist**, then start a new chat.

## Workflow

### 1. Get a Chrome tab

Use `tabs_context_mcp` with `createIfEmpty: true` to get or create a tab for this session.

### 2. Navigate to fastdl.app Reels page

Navigate to `https://fastdl.app/instagram-reels-download` — this is the Reels-specific page. Do NOT use the carousel page (`/carousel`) as it may not process reels correctly.

```
navigate → https://fastdl.app/instagram-reels-download
```

### 3. Paste the reel URL and submit

Use `find` to locate the input field (placeholder text: "Insert instagram link here"), then `form_input` to set the reel URL. Then `find` the Download button (a submit button labeled "Download") and click it with the `computer` tool.

```
find → "input field for URL"
form_input → ref, value: <reel_url>
find → "Download button"
computer → left_click on the Download button ref
```

### 4. Wait for results to load

Wait 5 seconds for fastdl.app to process the reel. Then scroll down to reveal the video thumbnail and download link — the results appear below the input form.

```
computer → wait 5s
computer → scroll down 5 ticks at center of page
```

Take a screenshot to confirm results loaded. You should see a video thumbnail, a blue "Download" button, and the reel caption text.

### 5. Extract the direct download URL

This is the critical step. Do NOT click the blue "Download" button on the page — that triggers a browser download to the user's Downloads folder, which the workspace sandbox can't access.

Instead, use `find` to locate the download link element — it's an `<a>` tag with an href containing `media.fastdl.app`. Then use `read_page` with `ref_id` set to that element's ref to extract the full href URL.

```
find → "download link with media.fastdl.app URL"
read_page → ref_id: <the ref from find>
```

The href will be a long URL starting with `https://media.fastdl.app/get?...` that contains the actual Instagram CDN video URL as an encoded parameter. Copy this entire URL — it's the direct download link.

### 6. Extract the reel caption for naming

From the results page (visible after step 4), look for the reel caption text. It typically appears just below the blue Download button. Use it to generate a short, descriptive folder and filename (3-6 words, lowercase, hyphens). The folder name must start with `ig-reel-`. For example:

- Caption: "AKA stop being a millennial parent to Claude" → folder: `ig-reel-claude-boomer-parent/`, file: `claude-boomer-parent.mp4`
- Caption: "5 AI tools you need in 2025" → folder: `ig-reel-5-ai-tools-2025/`, file: `5-ai-tools-2025.mp4`
- If no caption is visible → folder: `ig-reel-SHORTCODE/`, file: `ig-reel-SHORTCODE.mp4` (extract shortcode from the original URL)

### 7. Download with curl

Use bash to create the `Notes Ideas/` folder and the per-post subfolder (if they don't exist) and download the video using curl. Use the workspace bash mount path for the user's folder.

```bash
mkdir -p "<workspace-bash-path>/Notes Ideas/ig-reel-<descriptive-name>"
curl -L -o "<workspace-bash-path>/Notes Ideas/ig-reel-<descriptive-name>/<filename>.mp4" "<direct_url_from_step_5>"
```

Remember to translate the workspace path to the bash mount path (check the path mapping in your system prompt — the workspace folder maps to `/sessions/.../mnt/...` or similar in bash).

### 8. Verify and report

Check the downloaded file exists and has a reasonable size (reels are typically 2-20 MB):

```bash
ls -lh "<workspace-bash-path>/Notes Ideas/ig-reel-<descriptive-name>/<filename>.mp4"
```

Then provide the user a `computer://` link to the file so they can open it directly:

```
[View your video](computer://<workspace-file-path>/Notes Ideas/ig-reel-<descriptive-name>/<filename>.mp4)
```

## Troubleshooting

- **fastdl.app shows no results after clicking Download**: The page may need more time. Wait an additional 5 seconds and scroll down again. If still nothing, try scrolling up to check for error messages near the input field.
- **No `media.fastdl.app` link found**: The reel may be private or region-restricted. Let the user know.
- **curl download fails or file is 0 bytes**: The direct URL may have expired (they have time-limited signatures). Go back to step 3 and re-submit the reel URL to get a fresh link.
- **curl returns "not on allowlist" error**: The user needs to add `media.fastdl.app` to their network allowlist in Settings.

## Things that do NOT work

- **Clicking the blue Download button on fastdl.app** — This downloads to the user's local Downloads folder, which the workspace sandbox can't access. Always extract the direct URL and use curl instead.
- **Trying to download reels directly from Instagram** — Instagram doesn't serve reel video files in a way that's easily extractable from the page DOM. Using fastdl.app as an intermediary is the reliable approach.

## Output location

Save videos to the user's workspace `Notes Ideas/` folder, organized into per-post subfolders with descriptive names derived from the video caption. Each post gets its own folder named `ig-reel-<descriptive-name>` (e.g., `ig-reel-claude-boomer-parent`, `ig-reel-5-ai-tools-2025`). The video file goes inside that subfolder. Provide a `computer://` link so the user can view the file directly.
