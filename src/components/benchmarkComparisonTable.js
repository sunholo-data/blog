import React, { useEffect, useState } from 'react';
import styles from './benchmarkComparisonTable.module.css';

const DEFAULT_DATA_URL = 'https://ailang.sunholo.com/benchmarks/latest.json';

function formatModelName(name) {
  if (name.includes('claude-opus-4-7')) return 'Claude Opus 4.7';
  if (name.includes('claude-sonnet-4-6')) return 'Claude Sonnet 4.6';
  if (name.includes('claude-sonnet-4-5')) return 'Claude Sonnet 4.5';
  if (name.includes('claude-haiku-4-5')) return 'Claude Haiku 4.5';
  if (name.includes('gpt5-5-codex')) return 'GPT-5.5 Codex';
  if (name.includes('gpt5-5-pro')) return 'GPT-5.5 Pro';
  if (name.includes('gpt5-5')) return 'GPT-5.5';
  if (name.includes('gpt5-4-mini')) return 'GPT-5.4 Mini';
  if (name.includes('gpt-5-mini')) return 'GPT-5 Mini';
  if (name.includes('gpt-5')) return 'GPT-5';
  if (name.includes('gemini-3-1-pro')) return 'Gemini 3.1 Pro';
  if (name.includes('gemini-3-flash')) return 'Gemini 3 Flash';
  if (name.includes('gemini-3-pro')) return 'Gemini 3 Pro';
  if (name.includes('gemini-2-5-flash') || name.includes('gemini-2.5-flash')) return 'Gemini 2.5 Flash';
  if (name.includes('gemini-2-5-pro') || name.includes('gemini-2.5-pro')) return 'Gemini 2.5 Pro';
  if (name.startsWith('opencode-')) return 'opencode · ' + formatModelName(name.replace('opencode-', ''));
  if (name.startsWith('pi-')) return 'pi · ' + formatModelName(name.replace('pi-', ''));
  return name.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
}

const ArrowUpDown = ({ className }) => (
  <svg className={className} width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <path d="m21 16-4 4-4-4" />
    <path d="M17 20V4" />
    <path d="m3 8 4-4 4 4" />
    <path d="M7 4v16" />
  </svg>
);

const TrendingUp = ({ className }) => (
  <svg className={className} width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <polyline points="22 7 13.5 15.5 8.5 10.5 2 17" />
    <polyline points="16 7 22 7 22 13" />
  </svg>
);

const TrendingDown = ({ className }) => (
  <svg className={className} width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <polyline points="22 17 13.5 8.5 8.5 13.5 2 7" />
    <polyline points="16 17 22 17 22 11" />
  </svg>
);

function ComparisonTable({ models }) {
  const [sortColumn, setSortColumn] = useState('ailangSuccess');
  const [sortDirection, setSortDirection] = useState('desc');

  const tableData = Object.entries(models)
    .filter(([, stats]) => stats.languages && stats.languages.ailang && stats.languages.python)
    .map(([name, stats]) => {
      const ailang = stats.languages.ailang;
      const python = stats.languages.python;
      const ailangSuccess = (ailang?.successRate || 0) * 100;
      const pythonSuccess = (python?.successRate || 0) * 100;
      const ailangTokens = ailang?.avgTokens || 0;
      const pythonTokens = python?.avgTokens || 1;
      const gap = ailangSuccess - pythonSuccess;
      return {
        modelName: name,
        displayName: formatModelName(name),
        ailangSuccess,
        ailangTokens: Math.round(ailangTokens),
        pythonSuccess,
        pythonTokens: Math.round(python?.avgTokens || 0),
        gap,
        tokenRatio: ailangTokens / pythonTokens,
      };
    });

  const sortedData = [...tableData].sort((a, b) => {
    const aVal = a[sortColumn];
    const bVal = b[sortColumn];
    if (sortDirection === 'asc') return aVal > bVal ? 1 : -1;
    return aVal < bVal ? 1 : -1;
  });

  const handleSort = (column) => {
    if (sortColumn === column) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortColumn(column);
      setSortDirection('desc');
    }
  };

  const SortIcon = ({ column }) => {
    if (sortColumn !== column) {
      return <ArrowUpDown className={`${styles.sortIcon} ${styles.sortIconInactive}`} />;
    }
    return sortDirection === 'asc'
      ? <TrendingUp className={`${styles.sortIcon} ${styles.sortIconActive}`} />
      : <TrendingDown className={`${styles.sortIcon} ${styles.sortIconActive}`} />;
  };

  const badgeColor = (rate) =>
    rate >= 70 ? 'var(--ifm-color-success)' :
    rate >= 50 ? 'var(--ifm-color-warning)' :
    'var(--ifm-color-danger)';

  return (
    <table className={styles.comparisonTable}>
      <thead>
        <tr>
          <th className={styles.tableHeaderSticky}>Model</th>
          <th colSpan="2" className={styles.tableHeaderGroup}>AILANG</th>
          <th colSpan="2" className={styles.tableHeaderGroup}>Python</th>
          <th colSpan="2" className={styles.tableHeaderGroup}>Comparison</th>
        </tr>
        <tr>
          <th className={styles.tableHeaderSticky}></th>
          <th className={styles.tableHeaderClickable} onClick={() => handleSort('ailangSuccess')}>
            % <SortIcon column="ailangSuccess" />
          </th>
          <th className={styles.tableHeaderClickable} onClick={() => handleSort('ailangTokens')}>
            Tok <SortIcon column="ailangTokens" />
          </th>
          <th className={styles.tableHeaderClickable} onClick={() => handleSort('pythonSuccess')}>
            % <SortIcon column="pythonSuccess" />
          </th>
          <th className={styles.tableHeaderClickable} onClick={() => handleSort('pythonTokens')}>
            Tok <SortIcon column="pythonTokens" />
          </th>
          <th className={styles.tableHeaderClickable} onClick={() => handleSort('gap')}>
            Gap <SortIcon column="gap" />
          </th>
          <th className={styles.tableHeaderClickable} onClick={() => handleSort('tokenRatio')}>
            Ratio <SortIcon column="tokenRatio" />
          </th>
        </tr>
      </thead>
      <tbody>
        {sortedData.map((row) => (
          <tr key={row.modelName}>
            <td className={styles.tableModelName}>{row.displayName}</td>
            <td className={styles.tableNumber}>
              <span className={styles.successBadge} style={{ backgroundColor: badgeColor(row.ailangSuccess) }}>
                {row.ailangSuccess.toFixed(1)}
              </span>
            </td>
            <td className={styles.tableNumber}>{row.ailangTokens}</td>
            <td className={styles.tableNumber}>
              <span className={styles.successBadge} style={{ backgroundColor: badgeColor(row.pythonSuccess) }}>
                {row.pythonSuccess.toFixed(1)}
              </span>
            </td>
            <td className={styles.tableNumber}>{row.pythonTokens}</td>
            <td className={styles.tableNumber}>
              <span className={row.gap >= 0 ? styles.gapPositive : styles.gapNegative}>
                {row.gap >= 0 ? '+' : ''}{row.gap.toFixed(1)}
              </span>
            </td>
            <td className={styles.tableNumber}>
              <span className={row.tokenRatio > 1 ? styles.ratioHigher : styles.ratioLower}>
                {row.tokenRatio.toFixed(2)}x
              </span>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

// Reshape the tier model_stats payload into the {totalRuns, languages: {...}}
// shape the table expects. Mirrors buildTierScopedModels in the AILANG
// dashboard so the table matches what the official benchmark page shows.
function buildTierModels(tierModelStats) {
  if (!tierModelStats) return null;
  const out = {};
  for (const [name, langs] of Object.entries(tierModelStats)) {
    if (!langs) continue;
    const ail = langs.ailang;
    const py = langs.python;
    const totalRuns = (ail?.totalRuns || 0) + (py?.totalRuns || 0);
    out[name] = {
      totalRuns,
      languages: {
        ...(ail ? { ailang: ail } : {}),
        ...(py ? { python: py } : {}),
      },
    };
  }
  return out;
}

const BenchmarkComparisonTable = ({
  dataUrl = DEFAULT_DATA_URL,
  tier = 'core',
}) => {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;
    fetch(dataUrl)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((json) => { if (!cancelled) setData(json); })
      .catch((err) => { if (!cancelled) setError(err.message || 'Failed to load benchmark data'); });
    return () => { cancelled = true; };
  }, [dataUrl]);

  if (error) {
    return (
      <div className={styles.error}>
        Couldn't load live benchmark data ({error}). See the{' '}
        <a href="https://ailang.sunholo.com/docs/benchmarks/performance">live benchmark dashboard</a>.
      </div>
    );
  }

  if (!data) {
    return <div className={styles.loading}>Loading live benchmark data…</div>;
  }

  // Prefer the tier scope (matches the official dashboard's default view),
  // fall back to the raw models block if the tier isn't present.
  const tierStats = data.tiers?.[tier]?.model_stats;
  const tierModels = buildTierModels(tierStats);
  const tableModels = tierModels || data.models || {};
  const tierLabel = tier ? tier.charAt(0).toUpperCase() + tier.slice(1) : null;
  const version = data.version;
  const timestamp = data.timestamp
    ? new Date(data.timestamp).toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' })
    : null;

  return (
    <div>
      <div className={styles.tableContainer}>
        <ComparisonTable models={tableModels} />
        <div className={styles.tableFootnote}>
          💡 <strong>Gap</strong> = AILANG − Python success % (positive = AILANG better) ·{' '}
          <strong>Ratio</strong> = AILANG/Python tokens (lower = more efficient) ·{' '}
          <strong>Tok</strong> = avg output tokens
        </div>
      </div>
      <div className={styles.tableMeta}>
        Live data{version ? ` from AILANG ${version}` : ''}{timestamp ? `, ${timestamp}` : ''}
        {tierModels && tierLabel ? ` · ${tierLabel} benchmark tier` : ''} ·{' '}
        <a href="https://ailang.sunholo.com/docs/benchmarks/performance" target="_blank" rel="noreferrer">
          full interactive dashboard →
        </a>
      </div>
    </div>
  );
};

export default BenchmarkComparisonTable;
