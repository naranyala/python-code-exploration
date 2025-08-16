import { h, render } from "preact"
import { signal, computed } from "@preact/signals"
import { setup, css } from "goober"

setup(h);

// Styles
const styles = {
  body: css`
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        background: #f9f9fb;
        margin: 0;
        padding: 0;
      `,
  container: css`
        max-width: 800px;
        margin: auto;
        padding: 16px;
      `,
  h1: css`
        font-size: 1.6rem;
        margin-bottom: 12px;
      `,
  tabBar: css`
        display: flex;
        background: #e5e5ea;
        border-radius: 8px;
        overflow: hidden;
        margin-bottom: 20px;
      `,
  tabButton: css`
        flex: 1;
        padding: 10px;
        border: none;
        background: transparent;
        font-size: 14px;
        color: #333;
        cursor: pointer;
        transition: background 0.2s;
      `,
  tabButtonActive: css`
        background: white;
        font-weight: 500;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) inset;
      `,
  tabButtonHover: css`
        &:hover:not(.${css`background: white;`}) {
          background: rgba(255, 255, 255, 0.5);
        }
      `,
  formGroup: css`
        display: flex;
        flex-direction: column;
        margin-bottom: 12px;
      `,
  label: css`
        font-size: 13px;
        margin-bottom: 4px;
        color: #555;
      `,
  input: css`
        font-size: 14px;
        padding: 8px;
        border-radius: 6px;
        border: 1px solid #ccc;
        background: white;
        width: 100%;
        box-sizing: border-box;
      `,
  textarea: css`
        min-height: 80px;
        resize: vertical;
      `,
  button: css`
        padding: 8px 12px;
        font-size: 14px;
        border: none;
        border-radius: 6px;
        cursor: pointer;
      `,
  btnPrimary: css`
        background: #007aff;
        color: white;
        &:hover { background: #0062cc; }
      `,
  btnDanger: css`
        background: #ff3b30;
        color: white;
        &:hover { background: #d32f2f; }
      `,
  btnSecondary: css`
        background: #ccc;
      `,
  tableWrapper: css`
        overflow-x: auto;
        background: white;
        border-radius: 6px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
      `,
  table: css`
        border-collapse: collapse;
        width: 100%;
      `,
  th: css`
        padding: 8px;
        border: 1px solid #eee;
        text-align: left;
        background: #f0f0f0;
        font-size: 13px;
      `,
  td: css`
        padding: 8px;
        border: 1px solid #eee;
        text-align: left;
      `,
  searchInput: css`
        width: 100%;
        max-width: 300px;
        margin-bottom: 10px;
      `,
  modalBackdrop: css`
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
      `,
  modal: css`
        background: white;
        padding: 20px;
        border-radius: 8px;
        width: 90%;
        max-width: 400px;
        box-sizing: border-box;
      `,
  modalH3: css`
        margin-top: 0;
      `,
  modalP: css`
        margin: 6px 0;
      `,
  desktopCol: css`
        @media (max-width: 600px) { display: none; }
      `
};

// State
const activeTab = signal('form');
const jobs = signal([]);
const newJob = signal({ title: '', company: '', location: '', salary: '', type: '', description: '' });
const searchQuery = signal('');
const selectedJob = signal(null);

// Computed
const filteredJobs = computed(() => {
  const q = searchQuery.value.trim().toLowerCase();
  return jobs.value.filter(job =>
    job.title.toLowerCase().includes(q) ||
    job.company.toLowerCase().includes(q) ||
    job.location.toLowerCase().includes(q) ||
    job.salary.toLowerCase().includes(q) ||
    job.type.toLowerCase().includes(q) ||
    job.description.toLowerCase().includes(q)
  );
});

// Components
function JobPortal() {
  const addJob = () => {
    if (newJob.value.title && newJob.value.company && newJob.value.location) {
      jobs.value = [...jobs.value, { ...newJob.value }];
      newJob.value = { title: '', company: '', location: '', salary: '', type: '', description: '' };
      activeTab.value = 'table';
    } else {
      alert('Please fill in required fields: Title, Company, Location.');
    }
  };

  const removeJob = (index) => {
    jobs.value = jobs.value.filter((_, i) => i !== index);
  };

  const exportData = () => {
    const blob = new Blob([JSON.stringify(jobs.value, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "jobs.json";
    a.click();
    URL.revokeObjectURL(url);
  };

  const importData = (event) => {
    const file = event.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const data = JSON.parse(e.target.result);
        if (Array.isArray(data)) {
          jobs.value = data;
          activeTab.value = 'table';
        } else {
          alert('Invalid JSON format.');
        }
      } catch {
        alert('Error reading file.');
      }
    };
    reader.readAsText(file);
  };

  const showDetails = (job) => {
    selectedJob.value = job;
  };

  return (
    <div class={styles.container}>
      <h1 class={styles.h1}>Job Recruitment Manager</h1>

      {/* Tabs */}
      <div class={styles.tabBar}>
        <button
          class={`${styles.tabButton} ${activeTab.value === 'form' ? styles.tabButtonActive : ''} ${styles.tabButtonHover}`}
          onClick={() => activeTab.value = 'form'}
        >
          Add Job
        </button>
        <button
          class={`${styles.tabButton} ${activeTab.value === 'table' ? styles.tabButtonActive : ''} ${styles.tabButtonHover}`}
          onClick={() => activeTab.value = 'table'}
        >
          Jobs List
        </button>
        <button
          class={`${styles.tabButton} ${activeTab.value === 'importExport' ? styles.tabButtonActive : ''} ${styles.tabButtonHover}`}
          onClick={() => activeTab.value = 'importExport'}
        >
          Import/Export
        </button>
      </div>

      {/* Form */}
      {activeTab.value === 'form' && (
        <div>
          <h2>Add New Job</h2>
          <div class={styles.formGroup}>
            <label class={styles.label}>Job Title</label>
            <input
              class={styles.input}
              value={newJob.value.title}
              onInput={(e) => (newJob.value = { ...newJob.value, title: e.target.value })}
            />
          </div>
          <div class={styles.formGroup}>
            <label class={styles.label}>Company</label>
            <input
              class={styles.input}
              value={newJob.value.company}
              onInput={(e) => (newJob.value = { ...newJob.value, company: e.target.value })}
            />
          </div>
          <div class={styles.formGroup}>
            <label class={styles.label}>Location</label>
            <input
              class={styles.input}
              value={newJob.value.location}
              onInput={(e) => (newJob.value = { ...newJob.value, location: e.target.value })}
            />
          </div>
          <div class={styles.formGroup}>
            <label class={styles.label}>Salary Range</label>
            <input
              class={styles.input}
              value={newJob.value.salary}
              onInput={(e) => (newJob.value = { ...newJob.value, salary: e.target.value })}
            />
          </div>
          <div class={styles.formGroup}>
            <label class={styles.label}>Job Type</label>
            <select
              class={styles.input}
              value={newJob.value.type}
              onInput={(e) => (newJob.value = { ...newJob.value, type: e.target.value })}
            >
              <option value="">Select Type</option>
              <option>Full-time</option>
              <option>Part-time</option>
              <option>Contract</option>
              <option>Internship</option>
            </select>
          </div>
          <div class={styles.formGroup}>
            <label class={styles.label}>Description</label>
            <textarea
              class={`${styles.input} ${styles.textarea}`}
              value={newJob.value.description}
              onInput={(e) => (newJob.value = { ...newJob.value, description: e.target.value })}
            ></textarea>
          </div>
          <button class={`${styles.button} ${styles.btnPrimary}`} onClick={addJob}>
            Add Job
          </button>
        </div>
      )}

      {/* Table */}
      {activeTab.value === 'table' && (
        <div>
          <h2>Jobs List</h2>
          <input
            class={`${styles.input} ${styles.searchInput}`}
            value={searchQuery.value}
            onInput={(e) => (searchQuery.value = e.target.value)}
            placeholder="Search jobs..."
          />
          <div class={styles.tableWrapper}>
            {filteredJobs.value.length ? (
              <table class={styles.table}>
                <thead>
                  <tr>
                    <th class={styles.th}>#</th>
                    <th class={styles.th}>Title</th>
                    <th class={styles.th}>Company</th>
                    <th class={`${styles.th} ${styles.desktopCol}`}>Location</th>
                    <th class={`${styles.th} ${styles.desktopCol}`}>Salary</th>
                    <th class={`${styles.th} ${styles.desktopCol}`}>Type</th>
                    <th class={`${styles.th} ${styles.desktopCol}`}>Description</th>
                    <th class={styles.th}>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredJobs.value.map((job, index) => (
                    <tr key={index}>
                      <td class={styles.td}>{index + 1}</td>
                      <td class={styles.td}>{job.title}</td>
                      <td class={styles.td}>{job.company}</td>
                      <td class={`${styles.td} ${styles.desktopCol}`}>{job.location}</td>
                      <td class={`${styles.td} ${styles.desktopCol}`}>{job.salary}</td>
                      <td class={`${styles.td} ${styles.desktopCol}`}>{job.type}</td>
                      <td class={`${styles.td} ${styles.desktopCol}`}>{job.description}</td>
                      <td class={styles.td}>
                        <button
                          class={`${styles.button} ${styles.btnSecondary}`}
                          onClick={() => showDetails(job)}
                        >
                          Details
                        </button>
                        <button
                          class={`${styles.button} ${styles.btnDanger} ${styles.desktopCol}`}
                          onClick={() => removeJob(index)}
                        >
                          Remove
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <p>No jobs found.</p>
            )}
          </div>
        </div>
      )}

      {/* Import/Export */}
      {activeTab.value === 'importExport' && (
        <div>
          <h2>Import/Export</h2>
          <button class={`${styles.button} ${styles.btnPrimary}`} onClick={exportData}>
            Export JSON
          </button>
          <input
            type="file"
            accept=".json"
            onChange={importData}
            style="margin-top:10px;"
          />
        </div>
      )}

      {/* Modal */}
      {selectedJob.value && (
        <div
          class={styles.modalBackdrop}
          onClick={(e) => {
            if (e.target === e.currentTarget) selectedJob.value = null;
          }}
        >
          <div class={styles.modal}>
            <h3 class={styles.modalH3}>{selectedJob.value.title}</h3>
            <p class={styles.modalP}>
              <strong>Company:</strong> {selectedJob.value.company}
            </p>
            <p class={styles.modalP}>
              <strong>Location:</strong> {selectedJob.value.location}
            </p>
            <p class={styles.modalP}>
              <strong>Salary:</strong> {selectedJob.value.salary}
            </p>
            <p class={styles.modalP}>
              <strong>Type:</strong> {selectedJob.value.type}
            </p>
            <p class={styles.modalP}>
              <strong>Description:</strong>
            </p>
            <p class={styles.modalP}>{selectedJob.value.description}</p>
            <button
              class={`${styles.button} ${styles.btnSecondary}`}
              onClick={() => (selectedJob.value = null)}
              style="margin-top:10px;"
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default JobPortal
