import React from 'react';
import Feed from './components/Feed';
import Leaderboard from './components/Leaderboard';
import './styles.css';

function App() {
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Playto Community Feed</h1>
      <Leaderboard />
      <Feed />
    </div>
  );
}

export default App;