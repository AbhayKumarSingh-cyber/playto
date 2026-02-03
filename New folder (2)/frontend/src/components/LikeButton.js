import React, { useState, useEffect } from 'react';
import LikeButton from './LikeButton';

function Comments({ postId }) {
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState('');

  useEffect(() => {
    fetch(`/api/comments/?post_id=${postId}`)
      .then(res => res.json())
      .then(data => setComments(data));
  }, [postId]);

  const submitComment = (parentId = null) => {
    fetch('/api/comments/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ post: postId, parent: parentId, text: newComment }),
    }).then(() => {
      setNewComment('');
      // Refresh comments
      fetch(`/api/comments/?post_id=${postId}`)
        .then(res => res.json())
        .then(data => setComments(data));
    });
  };

  const renderComments = (comments, depth = 0) => {
    return comments.map(comment => (
      <div key={comment.id} className={`ml-${depth * 4} border-l pl-4 mb-2`}>
        <p><strong>{comment.author}</strong>: {comment.text}</p>
        <LikeButton commentId={comment.id} />
        <input
          type="text"
          placeholder="Reply..."
          onChange={(e) => setNewComment(e.target.value)}
          className="border p-1 mr-2"
        />
        <button onClick={() => submitComment(comment.id)} className="bg-blue-500 text-white p-1">Reply</button>
        {comment.replies && renderComments(comment.replies, depth + 1)}
      </div>
    ));
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Add comment..."
        value={newComment}
        onChange={(e) => setNewComment(e.target.value)}
        className="border p-2 w-full mb-2"
      />
      <button onClick={() => submitComment()} className="bg-green-500 text-white p-2">Comment</button>
      {renderComments(comments)}
    </div>
  );
}

export default Comments;