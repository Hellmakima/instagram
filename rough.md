"""
File: **project/rough.md**

Contains rough notes on the project
"""

### Profile page

- `https://www.instagram.com/<username>/`
  - goes to profile page
  - if it's same as username, the ui changes a bit
- `https://www.instagram.com/<username>/reels/`
- `https://www.instagram.com/<username>/tagged/`

### Core page

- `https://www.instagram.com/`
  - shows recent posts and reels and stuff from algorith (mix of following and explore)
  - includes stories, suggested users, ads, threads from threads
- `https://www.instagram.com/explore/`
- `https://www.instagram.com/reels/`
  - goes to reels page, and loads a specific reel
  - `https://www.instagram.com/reels/<post_id>/`
  - it's just a post served as a reel
- **search, notifications and create** are pop-up windows

### Auth

- `https://www.instagram.com/accounts/login/`
- `https://www.instagram.com/accounts/emailsignup/`

### Messages

- `https://www.instagram.com/direct/inbox/`
- `https://www.instagram.com/direct/t/<thread_id>/`

### Specifics

- `https://www.instagram.com/p/<post_id>/?img_index=4`
  - goes to post (img_index is for multi-image posts)
  - it's a popup window
  - if opeened in new tab, shows related posts below
- `https://www.instagram.com/<username>/following/`
  - pop-up window with following list
