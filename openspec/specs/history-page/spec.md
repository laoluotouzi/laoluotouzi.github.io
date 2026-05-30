## ADDED Requirements

### Requirement: History page SHALL be accessible from navigation
The system SHALL render a history page at `/history/` and include a "历史" navigation link in the site header, placed after "归档" and before "关于".

#### Scenario: Navigation link present on all pages
- **WHEN** any blog page is rendered
- **THEN** the site navigation SHALL contain a link labeled "历史" pointing to `/history/`
- **AND** the link SHALL appear between "归档" and "关于" in the navigation order

#### Scenario: History page URL is accessible
- **WHEN** a user navigates to `/history/`
- **THEN** the system SHALL return a valid HTML page with the history content

### Requirement: History page SHALL extract portfolio images from weekly journal posts
The system SHALL scan all posts whose `content_html` contains "老罗投资周记" or "老罗实盘周记" keywords, and extract portfolio snapshot images by matching `<img>` tags whose alt attribute contains "目前持仓" or "持仓股票明细".

#### Scenario: Extract image from post with matching keywords and image
- **WHEN** a post's `content_html` contains "老罗投资周记" AND contains an `<img>` tag with alt containing "目前持仓"
- **THEN** the system SHALL extract that image's `src` as a history item

#### Scenario: Extract image with alt "持仓股票明细"
- **WHEN** a post's `content_html` contains "老罗实盘周记" AND contains an `<img>` tag with alt containing "持仓股票明细（港股已换算为人民币）"
- **THEN** the system SHALL extract that image's `src` as a history item

#### Scenario: Skip posts without matching keywords
- **WHEN** a post's `content_html` does NOT contain "老罗投资周记" or "老罗实盘周记"
- **THEN** the system SHALL skip that post entirely

#### Scenario: Skip posts without portfolio image
- **WHEN** a post contains matching keywords but no `<img>` tag with alt containing "目前持仓" or "持仓股票明细"
- **THEN** the system SHALL skip that post

### Requirement: History page SHALL display items in reverse chronological order with pagination
The system SHALL display history items sorted by post date in descending order, with pagination at 10 items per page.

#### Scenario: Items sorted by date descending
- **WHEN** the history page is rendered
- **THEN** items SHALL be ordered from newest to oldest by post date

#### Scenario: First page at /history/
- **WHEN** the first page of history is requested
- **THEN** items 1-10 SHALL be displayed at `/history/`

#### Scenario: Subsequent pages at /history/page/N/
- **WHEN** page 2 of history is requested
- **THEN** items 11-20 SHALL be displayed at `/history/page/2/`

#### Scenario: Pagination controls displayed
- **WHEN** there are more than 10 history items
- **THEN** the page SHALL display pagination controls with page numbers, prev/next links
- **AND** pagination SHALL use ellipsis for large page counts, consistent with other paginated pages

### Requirement: History page SHALL group items by year and month visually
The system SHALL display year and month group headers as visual separators between items when the year or month changes.

#### Scenario: Year group header displayed
- **WHEN** the first item of a new year appears in the list
- **THEN** a year header (e.g. "2026年") SHALL be displayed before that item

#### Scenario: Month group header displayed
- **WHEN** the first item of a new month appears in the list
- **THEN** a month header (e.g. "2026年3月") SHALL be displayed before that item

### Requirement: Each history item SHALL display date, image, and link to original post
The system SHALL render each history item as a card containing the post date as a title, the portfolio snapshot image, and a link to the original blog post.

#### Scenario: History item card content
- **WHEN** a history item is rendered
- **THEN** it SHALL display the post date formatted as "YYYY年MM月DD日"
- **AND** it SHALL display the portfolio snapshot image with lazy loading
- **AND** it SHALL display a link to the original blog post URL (e.g. "查看原文")

### Requirement: History page SHALL support image lightbox
The system SHALL allow users to click on a portfolio snapshot image to view it in a full-screen lightbox overlay.

#### Scenario: Open lightbox on image click
- **WHEN** a user clicks on a portfolio snapshot image
- **THEN** a full-screen overlay SHALL display the image at a larger size
- **AND** the page background SHALL be dimmed

#### Scenario: Close lightbox
- **WHEN** the lightbox is open and the user clicks the close button, clicks outside the image, or presses Escape
- **THEN** the lightbox SHALL close and normal page scrolling SHALL resume

### Requirement: History page SHALL use consistent blog layout
The history page SHALL inherit `base.html` and include the standard sidebar with recent posts, tags, archive years, and social media links.

#### Scenario: Sidebar present on history page
- **WHEN** the history page is rendered
- **THEN** the standard sidebar widgets (recent posts, tags, archive years, social media) SHALL be displayed

#### Scenario: Header and footer consistent
- **WHEN** the history page is rendered
- **THEN** the site header and footer SHALL match all other blog pages
