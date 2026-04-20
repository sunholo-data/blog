import React, { useState } from 'react';
import styles from './codeCompare.module.css';

const CodeCompare = ({
  title,
  left = {},
  right = {},
  defaultView = 'side-by-side',
}) => {
  const [view, setView] = useState(defaultView);

  const Pane = ({ pane, side }) => (
    <div className={`${styles.pane} ${styles[side]}`}>
      <div
        className={styles.paneHeader}
        style={{ '--pane-color': pane.color || (side === 'left' ? '#ef5350' : '#4CAF50') }}
      >
        <span className={styles.paneName}>{pane.name || (side === 'left' ? 'Before' : 'After')}</span>
        {pane.badge && <span className={styles.paneBadge}>{pane.badge}</span>}
      </div>
      <pre className={styles.code}>
        <code>{pane.code || ''}</code>
      </pre>
      {pane.caption && <p className={styles.caption}>{pane.caption}</p>}
    </div>
  );

  return (
    <div className={styles.container}>
      {title && <h2 className={styles.title}>{title}</h2>}
      <div className={styles.viewToggle}>
        <button
          className={view === 'side-by-side' ? styles.active : ''}
          onClick={() => setView('side-by-side')}
        >
          Side by side
        </button>
        <button
          className={view === 'stacked' ? styles.active : ''}
          onClick={() => setView('stacked')}
        >
          Stacked
        </button>
      </div>
      <div className={`${styles.panes} ${styles[view === 'stacked' ? 'stacked' : 'sideBySide']}`}>
        <Pane pane={left} side="left" />
        <Pane pane={right} side="right" />
      </div>
    </div>
  );
};

export default CodeCompare;
