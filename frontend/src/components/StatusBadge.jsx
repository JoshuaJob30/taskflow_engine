// src/components/StatusBadge.jsx
export default function StatusBadge({ status }) {
  const className = `status-badge status-${status?.toLowerCase()}`;

  return <span className={className}>{status}</span>;
}
