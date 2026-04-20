import React from 'react';
import styles from './tierComparison.module.css';

const TierComparison = ({
  title,
  tiers = [],
}) => {
  return (
    <div className={styles.container}>
      {title && <h2 className={styles.title}>{title}</h2>}
      <div className={styles.grid}>
        {tiers.map((tier, index) => (
          <div
            key={index}
            className={styles.tier}
            style={{
              '--tier-color': tier.color || '#0066cc',
              '--tier-bg': (tier.color || '#0066cc') + '12',
            }}
          >
            <div className={styles.header}>
              <span className={styles.number}>{index + 1}</span>
              <h3 className={styles.tierTitle}>{tier.name}</h3>
            </div>
            {tier.strength && (
              <div className={styles.strengthBar}>
                <div
                  className={styles.strengthFill}
                  style={{ width: `${tier.strength}%` }}
                />
                <span className={styles.strengthLabel}>{tier.strengthLabel || ''}</span>
              </div>
            )}
            {tier.description && (
              <p className={styles.description}>{tier.description}</p>
            )}
            {tier.points && (
              <ul className={styles.points}>
                {tier.points.map((point, pi) => (
                  <li key={pi}>
                    <span className={styles.pointIcon}>{tier.icon || (index === 0 ? '⚠' : index === tiers.length - 1 ? '✓' : '◐')}</span>
                    {point}
                  </li>
                ))}
              </ul>
            )}
            {tier.example && (
              <div className={styles.example}>
                <code>{tier.example}</code>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default TierComparison;
