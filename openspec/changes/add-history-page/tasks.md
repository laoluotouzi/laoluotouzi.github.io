## 1. Data Model

- [x] 1.1 Add `HistoryItem` dataclass to `blog/src/models.py` with fields: `post` (Post reference), `image_url` (str), `date` (inherited from post), `title` (inherited from post)

## 2. Image Extraction Logic

- [x] 2.1 Add `_extract_history_items()` function in `blog/src/renderer.py` that filters posts containing "老罗投资周记" or "老罗实盘周记" in `content_html`
- [x] 2.2 Within the filter function, use regex to extract `<img>` tags with alt containing "目前持仓" or "持仓股票明细" from `content_html`, returning a list of `HistoryItem` objects sorted by date descending

## 3. Rendering Function

- [x] 3.1 Add `render_history()` function in `blog/src/renderer.py` that takes env, list of HistoryItem, dist_dir, sidebar_context, and per_page
- [x] 3.2 Implement pagination logic in `render_history()` using `_build_page_range()`, outputting to `dist/history/index.html` and `dist/history/page/N/index.html`

## 4. Template

- [x] 4.1 Create `blog/src/templates/history.html` extending `base.html` with content block showing history item cards (date title, lazy-loaded image, "查看原文" link)
- [x] 4.2 Add year/month visual group headers in the template (display "YYYY年M月" before the first item of each month)
- [x] 4.3 Add pagination controls to `history.html` using the same pattern as `index.html` and `archive.html`
- [x] 4.4 Add lightbox overlay markup and inline JS/CSS to `history.html` (open on image click, close on ESC/click-outside/close button)

## 5. Build Integration

- [x] 5.1 Update `blog/src/generator.py` to import `render_history` and call it after `render_archives()`, passing the extracted history items
- [x] 5.2 Add "历史" navigation link in `blog/src/templates/base.html` between "归档" and "关于"

## 6. Verification

- [x] 6.1 Run `python3.11 blog/src/generator.py build` and verify history page renders correctly
- [x] 6.2 Verify navigation link appears on all pages in correct position
- [x] 6.3 Verify pagination works across multiple pages
- [x] 6.4 Verify lightbox opens and closes correctly
