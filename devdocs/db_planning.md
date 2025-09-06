# Database Planning

_later will merge this with `devdocs/build_principles.md` and `devdocs/notes.md`_

Maybe I'll use SQL for this. It is on hold for now.
caching is on hold for now. we'll go ahead with mongodb. Caching will be done when we have a good idea of what and how much to cache andhow to do it.
Another reason is mongodb provides `primary–replica` set architecture, which is a must for a production-ready system.
Might need GrpahQL for storing relations between users, posts, etc.

```json
[
  {
    "_id": "19d0d713edbf4e5bae2ee8751b38ec85", // uuid
    "username": "hellmakima",
    "is_blocked": true,
    "blocked_till": null, // UTC timestamp or null
    "is_verified": true,
    "is_deleted": false,
    "deleted_ttl": null, // will deleted after this timestamp or null
    "email": "instaclone@gmail.com",
    "phone": null,
    "is_private": false,
    "hashed_password": "$2b$12$yZJX/ONsYHT9UOfQ9AqGBeSgY/Yrc4cEKnF1Ag.z7u6wAxiRz1g1K",
    "created": "2025-08-11T06:04:38.224332+00:00",
    "profile_picture": "link",
    "posts": [
      {
        "id": "jSUYdcfUuP", // nano id
        "media_type": "image",
        /*
          image (png, jpg, svg, gif, jpeg, etc)
          video (mp4, mkv, etc)
        */
        "visibility": "public",
        /*
          public
        */
        "media_link": "link", // post file blob or link
        "created": "2025-08-11T11:30:11.838487+00:00", // timestamp
        "is_deleted": false,
        "likes_count": "2", // cache
        "likes": [
          {
            "user_id": "jsbhfvlshbwurionwekvbwiorbgywsl", // user id
            "timestamp": "2025-08-11T11:30:11.838487+00:00" // liked at
          }
        ],
        "pinned_comment": null, // The pinned comment object is stored here or maybe add comment id
        "creator_comment": null, // either object or comment id
        "comments_count": "2", // TODO: cache and update only in write server ocassionally.
        "comments": [
          // TODO: on report, copy the required fields to a different collection
          {
            "liked_by_creator": true,
            "reply_by_creator": true,
            "user_id": "a12d829146b2431aabecf9281ffb7ba5",
            "timestamp": "2025-08-11T11:30:11.838487+00:00", // liked at
            "is_edited": true,
            "value": "Bro this is dope.", // sanitized text
            "likes": [
              // no cache
              {
                "user_id": "jsbhfvlshbwurionwekvbwiorbgywsl", // user id
                "timestamp": "2025-08-11T11:30:11.838487+00:00" // liked at
              }
            ],
            "replies": [
              {
                "user_id": "a12d829146b2431aabecf9281ffb7ba5",
                "timestamp": "2025-08-11T11:30:11.838487+00:00", // liked at
                "is_edited": false,
                "is_post": true, // if a reply is a post (it can only be a reel)
                "value": "Yes Bro.", // sanitized text
                "likes": [
                  {
                    "user_id": "jsbhfvlshbwurionwekvbwiorbgywsl", // user id
                    "timestamp": "2025-08-11T11:30:11.838487+00:00" // liked at
                  }
                ]
              }
            ]
          }
        ]
      }
    ],
    "saved_collections": [
      {
        "name": "food",
        "posts": [
          {
            "post_id": "23d0d713edbf4e5bae2ee8751b38ec85",
            "saved_at": "2025-08-11T06:04:38.224332+00:00"
          }
        ]
      }
    ]
  }
]
```

---

- timestamp is isoformat in UTC zone eg: 2025-08-11T06:04:38.224332+00:00
  `print(datetime.now(timezone.utc).isoformat())`

---

## Space vs Time trade-off.

- **Storing more** = denormalization ->

  - **Pros:** O(1) reads, fewer joins/scans, better for high-read systems (social feeds).
  - **Cons:** Slightly more storage, risk of stale data if you don't update consistently.

- **Querying more** = normalization ->

  - **Pros:** Less storage, data is always consistent.
  - **Cons:** Slower reads, extra DB hits, bad if you have billions of reads per write.

For **social platforms**, storage is cheap, but latency kills engagement.
That's why Facebook, Twitter, etc. denormalize **small booleans/counters** all over the place.
Flags like `is_creator_reply` or `liked_by_creator` are just **1 byte each**, negligible compared to media blobs or text.

So: **if reads >> writes** -> store the flag.
If writes >> reads and reads are rare -> query instead.

For your case (feeds, likes, comments) -> reads dominate -> **store it**.

## Caching

- fields like likes_count, comments_count, etc. are cached in memory
- these are not updated to the write server, instead only re-computed occasionally.
- the other servers send the actual like object to the write server.

Great - since you're using **MongoDB**, normalization needs to be **balanced**, because over-normalizing in NoSQL often **hurts performance** due to the lack of joins and transactional constraints.

So, let's break it down into three things:

---

## Goal: Balanced Normalization for MongoDB

- **Avoid unnecessary joins** (lookups)
- **Prevent document bloat** (especially when documents grow with time, like comments/replies)
- **Allow for fast reads/writes** (especially on feed, profile, and comment sections)
- Keep the schema **flexible** for updates

---

## What to Normalize vs Embed in MongoDB

### **Embed** when

- The embedded data is **bounded in size** (e.g., past profile pictures, 5–10 items)
- It's **used/read together** with the parent document
- It's **not accessed independently**

### **Reference** when

- Data can grow **unbounded** (e.g., comments, likes)
- It's accessed **independently** (e.g., searching user posts, querying a comment)
- It's **shared** across documents (e.g., same user liking multiple posts)

---

## Final Notes on "How Much to Normalize"

**Normalize**:

- `likes`, `comments`, and `replies` -> reference-based
- Allows efficient querying, avoids unbounded document size

**Embed**:

- Small arrays like `past_profile_pictures`, or creator's own comment in post (if rare)

**Avoid over-normalizing** user metadata, or things that never grow - otherwise every query will require extra lookups (and that's not Mongo's strength).

---

If you're optimizing for:

- **Feed performance** -> denormalize a bit more (cache comment/user names)
- **Moderation/reporting** -> normalize comments and replies fully

---

**Calculate engagement**

- Interaction
  - likes
    - liked post
    - liked comments
  - comment
    - aggregated comment emotion for each direct comment
    - do something for replies
  - share
    - share count
  - save
- View duration
  - scrolled within first .5 seconds
  - viewed duration vs total video length
  - Did user rewatch?
- Did they click "Not Interested"?
  - maybe handle this saparately.

---

**Suggested Improvements and Additional Considerations**
While the provided schema is very good, here are a few points for further consideration and potential refinement:

Optimizing the posts Collection for the Feed
For a social media feed, you often need to display a post along with some of its related data, such as a few comments and the creator's username. The current schema would require multiple lookups to get this information: one for the user, one for the comments, and potentially more for the pinned comment.

To optimize the feed, consider a hybrid approach. You could embed a limited number of the most recent comments and their user information directly in the posts collection.

The replies and comments Collections
The decision to separate comments and replies into two distinct collections is a valid one, but it could introduce complexity in querying. A simpler, more unified approach might be to have a single comments collection where replies are nested or referenced with a parent_comment_id.

---

## **Code snippet for hybrid approach**

Here's a Python example using **PyMongo** for that hybrid normalization pattern:

```python

def add_comment(post_id: str, author_id: str, text: str, max_recent: int = 3):
    post_oid = ObjectId(post_id)
    author_oid = ObjectId(author_id)

    # 1. Insert into comments collection
    comment_doc = {
        "post_id": post_oid,
        "author_id": author_oid,
        "text": text,
        "created_at": datetime.utcnow(),
        "parent_id": None
    }
    comment_id = comments.insert_one(comment_doc).inserted_id

    # 2. Push into recent_comments array in post doc, trim to N
    posts.update_one(
        {"_id": post_oid},
        {
            "$push": {
                "recent_comments": {
                    "$each": [{
                        "comment_id": comment_id,
                        "author_id": author_oid,
                        "text": text,
                        "created_at": comment_doc["created_at"]
                    }],
                    "$slice": -max_recent  # keep last N comments
                }
            },
            "$inc": {"comment_count": 1}
        }
    )

    return str(comment_id)

```

**How this works:**

- Keeps **all** comments in `comments` collection for full history.
- Keeps **last N** comments embedded in `posts.recent_comments` for fast reads.
- `$slice` in `$push` ensures the embedded list never grows beyond `max_recent`.

_There is a method called `$pop` but we dont do that here coz it uses `$slice`._

---

**IMPORTANT:** Look for ondelete cascade in MongoDB

---

## **Subset Pattern**

The technical name for this hybrid data structure approach in MongoDB is the "Subset Pattern" or a combination of "Embedded" and "Referenced" documents. It's a strategy that leverages the strengths of both data modeling approaches to optimize for specific access patterns.

A cached storage of top/hot comments embedded in the post document is an excellent and highly scalable strategy. This approach is a **best practice** for read-heavy applications like social media or news feeds.

---

### How It Works

- **Primary Data:** The real, up-to-the-minute comment data (likes, replies, content) lives in a separate **`comments` collection**.
- **Cached Data:** A denormalized subset of the top comments is embedded directly within the parent **`posts` collection** document.
- **Update Logic:** A background process (e.g., a scheduled job or a microservice) periodically queries the `comments` collection, calculates the "hot" or "top" comments based on your scoring logic, and updates the embedded array in the `posts` document.

---

### Why It's a Scalable Best Practice

1.  **Read Performance:** When a user views a post, your application can fetch both the post content and its top comments in a **single read operation**. This is significantly faster than performing two separate queries and a subsequent join.
2.  **Reduced Load:** It drastically reduces the number of queries to your `comments` collection, which is often very large. The expensive calculation and sorting are done offline, not on every page load.
3.  **User Experience:** For most users, a slightly stale list of "hot" comments (e.g., updated every 5-10 minutes) is perfectly acceptable and provides a great experience. The cache can be updated more frequently for high-traffic posts.

This approach effectively trades some data freshness for massive gains in read performance and scalability, which is the core principle behind building high-performance, read-heavy systems.
