#### The Tree
Nested comments use a self-referential `parent` field. Fetch all in one query with `select_related`, build tree in Python dict, serialize flat list with pre-nested replies.

#### The Math
Karma calculated dynamically: 5 per post like + 1 per comment like in last 24h. Uses two aggregations in SQL, combined in Python.

#### The AI Audit
AI suggested recursive serializer for comments, causing N+1. Fixed by fetching all comments once and building tree in view.