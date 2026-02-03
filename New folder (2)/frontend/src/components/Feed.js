import React, { useState, useEffect } from 'react';
import Comments from './Comments';
import LikeButton from './LikeButton';

function Feed() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    fetch('/api/posts/')
      .then(res => res.json())
      .then(data => setPosts(data));
  }, []);

  return (
    <div>
      {posts.map(post => (
        <div key={post.id} className="border p-4 mb-4">
          <p><strong>{post.author}</strong>: {post.text}</p>
          <LikeButton postId={post.id} />
          <Comments postId={post.id} />
        </div>
      ))}
    </div>
  );
}

export default Feed;