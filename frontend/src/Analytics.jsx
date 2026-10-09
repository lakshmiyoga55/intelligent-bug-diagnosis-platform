import React, { useEffect, useState } from "react";

function Analytics() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [filters, setFilters] = useState({
    component: "",
    severity: "",
    priority: "",
    exception_type: "",
    start_date: "",
    end_date: ""
  });

  const loadAnalytics = async (currentFilters = filters) => {
    setLoading(true);
    setError("");

    try {
      const params = new URLSearchParams();

      if (currentFilters.component) {
        params.append("component", currentFilters.component);
      }

      if (currentFilters.severity) {
        params.append("severity", currentFilters.severity);
      }

      if (currentFilters.priority) {
        params.append("priority", currentFilters.priority);
      }

      if (currentFilters.exception_type) {
        params.append(
          "exception_type",
          currentFilters.exception_type
        );
      }

      if (currentFilters.start_date) {
        params.append("start_date", currentFilters.start_date);
      }

      if (currentFilters.end_date) {
        params.append("end_date", currentFilters.end_date);
      }

      const response = await fetch(
        `http://127.0.0.1:5000/api/analytics?${params.toString()}`
      );

      if (!response.ok) {
        throw new Error("Analytics request failed");
      }

      const result = await response.json();

      // Backend returns:
      // { success: true, analytics: {...} }
      //
      // So we need to store only the analytics object.
      setData(result.analytics || {});
    } catch (err) {
      console.error("Analytics Error:", err);

      setError(
        "Unable to connect to the analytics backend."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAnalytics();
  }, []);

  const handleChange = (event) => {
    setFilters({
      ...filters,
      [event.target.name]: event.target.value
    });
  };

  const applyFilters = () => {
    loadAnalytics(filters);
  };

  const resetFilters = () => {
    const reset = {
      component: "",
      severity: "",
      priority: "",
      exception_type: "",
      start_date: "",
      end_date: ""
    };

    setFilters(reset);
    loadAnalytics(reset);
  };

  if (loading) {
    return (
      <div style={styles.loadingPage}>
        <div style={styles.spinner}></div>

        <h2>Loading Defect Analytics...</h2>

        <p>
          Analyzing historical and submitted defects.
        </p>
      </div>
    );
  }

  if (error) {
    return (
      <div style={styles.loadingPage}>
        <div style={styles.errorIcon}>!</div>

        <h2>Analytics Unavailable</h2>

        <p>{error}</p>

        <button
          style={styles.primaryButton}
          onClick={() => loadAnalytics()}
        >
          Try Again
        </button>
      </div>
    );
  }

  if (!data) {
    return null;
  }

  const componentData =
    data.component_frequency || {};

  const severityData =
    data.severity_frequency || {};

  const priorityData =
    data.priority_frequency || {};

  const exceptionData =
    data.exception_frequency || {};

  const duplicateData =
    data.duplicate_status_frequency || {};

  const rootCauseData =
    data.root_cause_frequency || {};

  const resolutionData =
    data.resolution_frequency || {};

  return (
    <div style={styles.page}>

      {/* HEADER */}

      <div style={styles.header}>
        <div style={styles.container}>

          <div style={styles.label}>
            DEFECT PATTERN ANALYTICS
          </div>

          <h1 style={styles.mainTitle}>
            Defect Analytics
          </h1>

          <p style={styles.subtitle}>
            Analyze recurring defect patterns, affected
            components, exceptions, root causes and resolutions.
          </p>

        </div>
      </div>

      <div style={styles.container}>

        {/* FILTERS */}

        <div style={styles.filterCard}>

          <div style={styles.cardHeader}>

            <div style={styles.iconBox}>
              🔎
            </div>

            <div>
              <h2 style={styles.cardTitle}>
                Filter Defects
              </h2>

              <p style={styles.cardSubtitle}>
                Filter defect analytics using selected criteria.
              </p>
            </div>

          </div>

          <div style={styles.filterGrid}>

            <Filter
              label="Component"
              name="component"
              value={filters.component}
              onChange={handleChange}
              options={
                data.available_filters?.components || []
              }
              placeholder="All Components"
            />

            <Filter
              label="Severity"
              name="severity"
              value={filters.severity}
              onChange={handleChange}
              options={
                data.available_filters?.severities || []
              }
              placeholder="All Severities"
            />

            <Filter
              label="Priority"
              name="priority"
              value={filters.priority}
              onChange={handleChange}
              options={
                data.available_filters?.priorities || []
              }
              placeholder="All Priorities"
            />

            <Filter
              label="Exception Type"
              name="exception_type"
              value={filters.exception_type}
              onChange={handleChange}
              options={
                data.available_filters?.exception_types || []
              }
              placeholder="All Exception Types"
            />

            <div>
              <label style={styles.fieldLabel}>
                Start Date
              </label>

              <input
                type="date"
                name="start_date"
                value={filters.start_date}
                onChange={handleChange}
                style={styles.input}
              />
            </div>

            <div>
              <label style={styles.fieldLabel}>
                End Date
              </label>

              <input
                type="date"
                name="end_date"
                value={filters.end_date}
                onChange={handleChange}
                style={styles.input}
              />
            </div>

          </div>

          <div style={styles.buttonRow}>

            <button
              style={styles.primaryButton}
              onClick={applyFilters}
            >
              Apply Filters
            </button>

            <button
              style={styles.secondaryButton}
              onClick={resetFilters}
            >
              Reset Filters
            </button>

          </div>

        </div>

        {/* SUMMARY */}

        <div style={styles.summaryGrid}>

          <SummaryCard
            icon="🐛"
            title="Total Bugs"
            value={data.total_bugs || 0}
            description="All analyzed defects"
          />

          <SummaryCard
            icon="🗂"
            title="Historical Bugs"
            value={data.historical_bugs || 0}
            description="Knowledge base defects"
          />

          <SummaryCard
            icon="📥"
            title="Submitted Bugs"
            value={data.submitted_bugs || 0}
            description="Submitted for diagnosis"
          />

          <SummaryCard
            icon="⚙"
            title="Most Affected Component"
            value={
              Array.isArray(data.most_affected_component)
                ? data.most_affected_component[0] || "Unknown"
                : data.most_affected_component || "Unknown"
            }
            description={`${getMostAffectedCount(
              data.most_affected_component
            )} bugs`}
          />

        </div>

        {/* DISTRIBUTION */}

        <SectionTitle
          label="DEFECT DISTRIBUTION"
          title="Defect Statistics"
          description="Overview of defect distribution across different categories."
        />

        <div style={styles.twoColumn}>

          <DistributionCard
            title="Component Distribution"
            icon="⚙"
            data={componentData}
          />

          <DistributionCard
            title="Severity Distribution"
            icon="⚠️"
            data={severityData}
          />

          <DistributionCard
            title="Priority Distribution"
            icon="🚩"
            data={priorityData}
          />

          <DistributionCard
            title="Exception Type Distribution"
            icon="⚡"
            data={exceptionData}
          />

        </div>

        {/* DUPLICATE */}

        <WideCard
          title="Duplicate Status"
          icon="🔗"
          description="Relationship between submitted and historical defects."
        >
          <DistributionBars data={duplicateData} />
        </WideCard>

        {/* ROOT CAUSE + RESOLUTION */}

        <div style={styles.twoColumn}>

          <ListCard
            title="Common Root Causes"
            icon="🧠"
            description="Frequently observed defect causes."
            data={rootCauseData}
          />

          <ListCard
            title="Common Resolutions"
            icon="🔧"
            description="Frequently used defect resolutions."
            data={resolutionData}
          />

        </div>

        {/* RECURRING */}

        <SectionTitle
          label="RECURRING DEFECT PATTERNS"
          title="Recurring Defect Patterns"
          description="Frequently occurring components and exception types."
        />

        <div style={styles.twoColumn}>

          <RecurringCard
            title="Affected Component"
            icon="⚙"
            patterns={
              data.recurring_patterns?.components || []
            }
          />

          <RecurringCard
            title="Exception Type"
            icon="⚡"
            patterns={
              data.recurring_patterns?.exceptions || []
            }
          />

        </div>

        {/* TIME */}

        <WideCard
          title="Time-Based Defect Analysis"
          icon="📅"
          description="Defect activity grouped by time period."
        >
          <TimeChart
            data={data.time_analysis || {}}
          />
        </WideCard>

      </div>

    </div>
  );
}


/* =====================================================
   FILTER
===================================================== */

function Filter({
  label,
  name,
  value,
  onChange,
  options,
  placeholder
}) {
  return (
    <div>

      <label style={styles.fieldLabel}>
        {label}
      </label>

      <select
        name={name}
        value={value}
        onChange={onChange}
        style={styles.input}
      >

        <option value="">
          {placeholder}
        </option>

        {options.map((option, index) => (
          <option
            key={`${option}-${index}`}
            value={option}
          >
            {option}
          </option>
        ))}

      </select>

    </div>
  );
}


/* =====================================================
   SUMMARY CARD
===================================================== */

function SummaryCard({
  icon,
  title,
  value,
  description
}) {
  return (
    <div style={styles.summaryCard}>

      <div style={styles.summaryTop}>

        <div style={styles.summaryIcon}>
          {icon}
        </div>

        <span style={styles.arrow}>
          ↗
        </span>

      </div>

      <div style={styles.summaryValue}>
        {value}
      </div>

      <div style={styles.summaryTitle}>
        {title}
      </div>

      <div style={styles.summaryDescription}>
        {description}
      </div>

    </div>
  );
}


/* =====================================================
   SECTION TITLE
===================================================== */

function SectionTitle({
  label,
  title,
  description
}) {
  return (
    <div style={styles.sectionTitle}>

      <div style={styles.label}>
        {label}
      </div>

      <h2 style={styles.sectionHeading}>
        {title}
      </h2>

      <p style={styles.sectionDescription}>
        {description}
      </p>

    </div>
  );
}


/* =====================================================
   WIDE CARD
===================================================== */

function WideCard({
  title,
  icon,
  description,
  children
}) {
  return (
    <div style={styles.wideCard}>

      <div style={styles.cardHeader}>

        <div style={styles.iconBox}>
          {icon}
        </div>

        <div>

          <h3 style={styles.cardTitle}>
            {title}
          </h3>

          <p style={styles.cardSubtitle}>
            {description}
          </p>

        </div>

      </div>

      {children}

    </div>
  );
}


/* =====================================================
   DISTRIBUTION CARD
===================================================== */

function DistributionCard({
  title,
  icon,
  data
}) {
  const entries = Object.entries(data);

  const maxValue = Math.max(
    ...entries.map(
      ([, value]) => Number(value) || 0
    ),
    1
  );

  return (
    <div style={styles.card}>

      <div style={styles.cardHeader}>

        <div style={styles.iconBox}>
          {icon}
        </div>

        <div>

          <h3 style={styles.cardTitle}>
            {title}
          </h3>

          <p style={styles.cardSubtitle}>
            Defect count by category
          </p>

        </div>

      </div>

      <div>

        {entries.length === 0 ? (

          <p style={styles.emptyText}>
            No data available.
          </p>

        ) : (

          entries.map(([label, value]) => {

            const numberValue =
              Number(value) || 0;

            return (
              <div
                key={label}
                style={styles.barItem}
              >

                <div style={styles.barInfo}>

                  <span style={styles.barLabel}>
                    {label}
                  </span>

                  <strong style={styles.barNumber}>
                    {numberValue}
                  </strong>

                </div>

                <div style={styles.barTrack}>

                  <div
                    style={{
                      ...styles.barFill,
                      width: `${
                        (numberValue / maxValue) * 100
                      }%`
                    }}
                  ></div>

                </div>

              </div>
            );

          })

        )}

      </div>

    </div>
  );
}


/* =====================================================
   DISTRIBUTION BARS
===================================================== */

function DistributionBars({ data }) {
  const entries = Object.entries(data);

  const maxValue = Math.max(
    ...entries.map(
      ([, value]) => Number(value) || 0
    ),
    1
  );

  if (entries.length === 0) {
    return (
      <p style={styles.emptyText}>
        No duplicate status data available.
      </p>
    );
  }

  return (
    <div>

      {entries.map(([label, value]) => {

        const numberValue =
          Number(value) || 0;

        return (
          <div
            key={label}
            style={styles.barItem}
          >

            <div style={styles.barInfo}>

              <span style={styles.barLabel}>
                {label}
              </span>

              <strong style={styles.barNumber}>
                {numberValue}
              </strong>

            </div>

            <div style={styles.barTrack}>

              <div
                style={{
                  ...styles.barFill,
                  width: `${
                    (numberValue / maxValue) * 100
                  }%`
                }}
              ></div>

            </div>

          </div>
        );

      })}

    </div>
  );
}


/* =====================================================
   LIST CARD
===================================================== */

function ListCard({
  title,
  icon,
  description,
  data
}) {
  const entries = Object.entries(data);

  return (
    <div style={styles.card}>

      <div style={styles.cardHeader}>

        <div style={styles.iconBox}>
          {icon}
        </div>

        <div>

          <h3 style={styles.cardTitle}>
            {title}
          </h3>

          <p style={styles.cardSubtitle}>
            {description}
          </p>

        </div>

      </div>

      {entries.length === 0 ? (

        <p style={styles.emptyText}>
          No data available.
        </p>

      ) : (

        entries.map(([label, value], index) => (

          <div
            key={label}
            style={styles.listRow}
          >

            <div style={styles.listNumber}>
              {String(index + 1).padStart(2, "0")}
            </div>

            <div style={styles.listText}>
              {label}
            </div>

            <div style={styles.listCount}>
              {value}
            </div>

          </div>

        ))

      )}

    </div>
  );
}


/* =====================================================
   RECURRING CARD
===================================================== */

function RecurringCard({
  title,
  icon,
  patterns
}) {
  const convertedPatterns =
    convertPatterns(patterns);

  return (
    <div style={styles.card}>

      <div style={styles.recurringIcon}>
        {icon}
      </div>

      <h3 style={styles.recurringTitle}>
        {title}
      </h3>

      {convertedPatterns.length === 0 ? (

        <p style={styles.emptyText}>
          No recurring patterns found.
        </p>

      ) : (

        convertedPatterns.map((item, index) => (

          <div
            key={index}
            style={styles.recurringItem}
          >

            <div>

              <strong style={styles.recurringName}>
                {item.name}
              </strong>

              <span style={styles.recurringSub}>
                {item.count} occurrence
                {item.count !== 1 ? "s" : ""}
              </span>

            </div>

            <strong style={styles.recurringCount}>
              {item.count}
            </strong>

          </div>

        ))

      )}

    </div>
  );
}


/* =====================================================
   TIME CHART
===================================================== */

function TimeChart({ data }) {
  const entries = Object.entries(data);

  if (entries.length === 0) {
    return (
      <p style={styles.emptyText}>
        No time-based defect data available.
      </p>
    );
  }

  const maxValue = Math.max(
    ...entries.map(
      ([, value]) => Number(value) || 0
    ),
    1
  );

  return (
    <div>

      {entries.map(([period, value]) => {

        const numberValue =
          Number(value) || 0;

        return (
          <div
            key={period}
            style={styles.timeRow}
          >

            <span style={styles.timeLabel}>
              {period}
            </span>

            <div style={styles.timeTrack}>

              <div
                style={{
                  ...styles.timeFill,
                  width: `${
                    (numberValue / maxValue) * 100
                  }%`
                }}
              ></div>

            </div>

            <strong style={styles.timeNumber}>
              {numberValue}
            </strong>

          </div>
        );
      })}

    </div>
  );
}


/* =====================================================
   HELPERS
===================================================== */

function getMostAffectedCount(value) {
  if (Array.isArray(value)) {
    return value[1] || 0;
  }

  return 0;
}


function convertPatterns(patterns) {
  if (!patterns) {
    return [];
  }

  if (Array.isArray(patterns)) {

    return patterns.map((item) => {

      if (typeof item === "string") {
        return {
          name: item,
          count: 1
        };
      }

      return {
        name:
          item.name ||
          item.label ||
          item.component ||
          item.exception_type ||
          "Unknown",

        count:
          item.count ||
          item.frequency ||
          1
      };
    });
  }

  if (typeof patterns === "object") {

    return Object.entries(patterns).map(
      ([name, count]) => ({
        name,
        count: Number(count) || 0
      })
    );
  }

  return [];
}


/* =====================================================
   STYLES
===================================================== */

const styles = {

  page: {
    minHeight: "100vh",
    background: "#f5f7fb",
    color: "#172033",
    fontFamily:
      "Arial, Helvetica, sans-serif",
    paddingBottom: "80px"
  },

  container: {
    width: "1180px",
    maxWidth: "calc(100% - 60px)",
    margin: "0 auto"
  },

  header: {
    background: "#ffffff",
    borderBottom:
      "1px solid #e7ebf1",
    padding: "35px 0"
  },

  label: {
    color: "#2563eb",
    fontSize: "11px",
    fontWeight: "800",
    letterSpacing: "1.4px"
  },

  mainTitle: {
    margin: "10px 0 0",
    fontSize: "42px",
    lineHeight: "1.15",
    letterSpacing: "-1px"
  },

  subtitle: {
    maxWidth: "700px",
    margin: "14px 0 0",
    color: "#697586",
    fontSize: "14px",
    lineHeight: "1.7"
  },

  card: {
    padding: "25px",
    background: "#ffffff",
    border: "1px solid #e1e7ef",
    borderRadius: "14px",
    boxShadow:
      "0 8px 25px rgba(15,23,42,0.04)"
  },

  filterCard: {
    marginTop: "40px",
    marginBottom: "30px",
    padding: "28px",
    background: "#ffffff",
    border: "1px solid #e1e7ef",
    borderRadius: "16px",
    boxShadow:
      "0 8px 25px rgba(15,23,42,0.04)"
  },

  cardHeader: {
    display: "flex",
    alignItems: "center",
    gap: "13px",
    paddingBottom: "20px",
    marginBottom: "18px",
    borderBottom:
      "1px solid #edf1f5"
  },

  iconBox: {
    width: "42px",
    height: "42px",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    background: "#eff6ff",
    borderRadius: "10px",
    fontSize: "18px"
  },

  cardTitle: {
    margin: "0",
    color: "#172033",
    fontSize: "16px"
  },

  cardSubtitle: {
    margin: "5px 0 0",
    color: "#98a2b3",
    fontSize: "10px"
  },

  filterGrid: {
    display: "grid",
    gridTemplateColumns:
      "repeat(4, 1fr)",
    gap: "18px"
  },

  fieldLabel: {
    display: "block",
    marginBottom: "7px",
    color: "#475467",
    fontSize: "11px",
    fontWeight: "700"
  },

  input: {
    width: "100%",
    height: "44px",
    padding: "0 12px",
    background: "#ffffff",
    border:
      "1px solid #d7dee8",
    borderRadius: "8px",
    color: "#344054",
    fontSize: "12px",
    outline: "none",
    boxSizing: "border-box"
  },

  buttonRow: {
    display: "flex",
    gap: "10px",
    marginTop: "23px"
  },

  primaryButton: {
    minHeight: "41px",
    padding: "0 19px",
    border: "none",
    borderRadius: "8px",
    background: "#2563eb",
    color: "#ffffff",
    fontSize: "12px",
    fontWeight: "700",
    cursor: "pointer"
  },

  secondaryButton: {
    minHeight: "41px",
    padding: "0 19px",
    border:
      "1px solid #d7dee8",
    borderRadius: "8px",
    background: "#ffffff",
    color: "#475467",
    fontSize: "12px",
    fontWeight: "700",
    cursor: "pointer"
  },

  summaryGrid: {
    display: "grid",
    gridTemplateColumns:
      "repeat(4, 1fr)",
    gap: "18px",
    marginBottom: "55px"
  },

  summaryCard: {
    minHeight: "175px",
    padding: "23px",
    background: "#ffffff",
    border:
      "1px solid #e1e7ef",
    borderRadius: "14px",
    boxShadow:
      "0 8px 25px rgba(15,23,42,0.04)"
  },

  summaryTop: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between"
  },

  summaryIcon: {
    width: "40px",
    height: "40px",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    background: "#eff6ff",
    borderRadius: "9px",
    fontSize: "18px"
  },

  arrow: {
    color: "#98a2b3"
  },

  summaryValue: {
    marginTop: "18px",
    color: "#172033",
    fontSize: "29px",
    fontWeight: "800"
  },

  summaryTitle: {
    marginTop: "6px",
    color: "#475467",
    fontSize: "12px",
    fontWeight: "700"
  },

  summaryDescription: {
    marginTop: "6px",
    color: "#98a2b3",
    fontSize: "10px"
  },

  sectionTitle: {
    marginTop: "50px",
    marginBottom: "25px"
  },

  sectionHeading: {
    margin: "7px 0 0",
    color: "#172033",
    fontSize: "25px"
  },

  sectionDescription: {
    margin: "7px 0 0",
    color: "#7b8798",
    fontSize: "12px"
  },

  twoColumn: {
    display: "grid",
    gridTemplateColumns:
      "repeat(2, 1fr)",
    gap: "20px",
    marginBottom: "20px"
  },

  wideCard: {
    padding: "25px",
    marginBottom: "20px",
    background: "#ffffff",
    border:
      "1px solid #e1e7ef",
    borderRadius: "14px",
    boxShadow:
      "0 8px 25px rgba(15,23,42,0.04)"
  },

  barItem: {
    marginBottom: "17px"
  },

  barInfo: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    marginBottom: "7px"
  },

  barLabel: {
    color: "#475467",
    fontSize: "11px"
  },

  barNumber: {
    color: "#172033",
    fontSize: "11px"
  },

  barTrack: {
    width: "100%",
    height: "7px",
    overflow: "hidden",
    background: "#edf1f5",
    borderRadius: "20px"
  },

  barFill: {
    height: "100%",
    minWidth: "3px",
    background: "#2563eb",
    borderRadius: "20px"
  },

  listRow: {
    display: "flex",
    alignItems: "center",
    gap: "13px",
    minHeight: "55px",
    padding: "10px 0",
    borderBottom:
      "1px solid #f0f2f5"
  },

  listNumber: {
    width: "28px",
    height: "28px",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    background: "#f8fafc",
    borderRadius: "7px",
    color: "#98a2b3",
    fontSize: "9px",
    fontWeight: "800"
  },

  listText: {
    flex: 1,
    color: "#475467",
    fontSize: "11px",
    lineHeight: "1.5"
  },

  listCount: {
    color: "#2563eb",
    fontSize: "12px",
    fontWeight: "800"
  },

  recurringIcon: {
    width: "40px",
    height: "40px",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    marginBottom: "13px",
    background: "#eff6ff",
    borderRadius: "9px"
  },

  recurringTitle: {
    margin: "0 0 17px",
    fontSize: "15px"
  },

  recurringItem: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    padding: "13px 15px",
    marginBottom: "10px",
    background: "#f8fafc",
    border:
      "1px solid #edf1f5",
    borderRadius: "9px"
  },

  recurringName: {
    display: "block",
    color: "#344054",
    fontSize: "11px"
  },

  recurringSub: {
    display: "block",
    marginTop: "4px",
    color: "#98a2b3",
    fontSize: "9px"
  },

  recurringCount: {
    color: "#2563eb",
    fontSize: "17px"
  },

  timeRow: {
    display: "grid",
    gridTemplateColumns:
      "110px 1fr 40px",
    alignItems: "center",
    gap: "15px",
    marginBottom: "18px"
  },

  timeLabel: {
    color: "#475467",
    fontSize: "11px",
    fontWeight: "700"
  },

  timeTrack: {
    height: "11px",
    overflow: "hidden",
    background: "#edf1f5",
    borderRadius: "20px"
  },

  timeFill: {
    height: "100%",
    minWidth: "4px",
    background: "#2563eb",
    borderRadius: "20px"
  },

  timeNumber: {
    color: "#172033",
    fontSize: "12px",
    textAlign: "right"
  },

  emptyText: {
    color: "#98a2b3",
    fontSize: "11px"
  },

  loadingPage: {
    minHeight: "600px",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    flexDirection: "column",
    background: "#f5f7fb",
    color: "#172033"
  },

  spinner: {
    width: "40px",
    height: "40px",
    marginBottom: "18px",
    border:
      "4px solid #e5e7eb",
    borderTopColor: "#2563eb",
    borderRadius: "50%"
  },

  errorIcon: {
    width: "45px",
    height: "45px",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    marginBottom: "15px",
    background: "#fef2f2",
    borderRadius: "50%",
    color: "#dc2626",
    fontSize: "22px",
    fontWeight: "800"
  }

};

export default Analytics;