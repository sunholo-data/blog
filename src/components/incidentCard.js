import React from 'react';
import styles from './incidentCard.module.css';

const IncidentCard = ({
  name,
  year,
  description,
  principle,
  principleNumber,
  outcome,
  color = '#ef5350',
  link,
  linkText,
}) => {
  return (
    <div className={styles.card} style={{ '--card-color': color }}>
      <div className={styles.sidebar}>
        <span className={styles.year}>{year}</span>
        {principleNumber && (
          <span className={styles.principleNum}>P{principleNumber}</span>
        )}
      </div>
      <div className={styles.body}>
        <div className={styles.top}>
          <h4 className={styles.name}>{name}</h4>
          {principle && <span className={styles.principle}>{principle}</span>}
        </div>
        <p className={styles.description}>{description}</p>
        <div className={styles.bottom}>
          {outcome && (
            <span className={styles.outcome}>{outcome}</span>
          )}
          {link && (
            <a href={link} target="_blank" rel="noopener noreferrer" className={styles.link}>
              {linkText || 'Source'} →
            </a>
          )}
        </div>
      </div>
    </div>
  );
};

export default IncidentCard;
