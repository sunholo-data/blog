// Generated into blog/src/components by website/scripts/sync_topics.py.
import React from 'react';
import data from '@site/src/data/topics.json';
import './sharedTopic.css';

export default function SharedTopic({topic, current}) {
  const entry = data.topics[topic];
  if (!entry) return null;
  return <nav className="topic-resources" aria-label={entry.title}>
    <h2>{entry.title}</h2>
    <p>{entry.description}</p>
    <ul>{entry.links.filter(link => link.path.replace(/\/$/, '') !== current.replace(/\/$/, '')).map(link =>
      <li key={link.path}><a href={data.origin + link.path}><small>{link.kind}</small>{link.label}</a></li>
    )}</ul>
  </nav>;
}
