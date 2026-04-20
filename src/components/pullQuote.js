import React from 'react';
import styles from './pullQuote.module.css';

const PullQuote = ({
  children,
  author,
  source,
  color = '#2196F3',
}) => {
  return (
    <blockquote
      className={styles.pullQuote}
      style={{ '--quote-color': color }}
    >
      <div className={styles.mark}>"</div>
      <p className={styles.text}>{children}</p>
      {(author || source) && (
        <footer className={styles.footer}>
          {author && <span className={styles.author}>— {author}</span>}
          {source && <cite className={styles.source}>{source}</cite>}
        </footer>
      )}
    </blockquote>
  );
};

export default PullQuote;
