    import { h, render } from 'preact';
    import { signal, effect } from '@preact/signals';
    import { setup, css } from 'goober';

    // Set up Goober for Preact
    setup(h);

    // Grouped styles with mobile responsiveness
    const styles = {
      container: css`
        max-width: 1200px;
        margin: 1rem auto;
        padding: 1rem;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background: #f8f9fa;
        min-height: 100vh;
        display: flex;
        flex-direction: column;

        @media (max-width: 768px) {
          margin: 0;
          padding: 0.5rem;
        }
      `,
      header: css`
        text-align: center;
        margin: 1rem 0;
        color: #333;
        font-size: 1.5rem;

        @media (max-width: 768px) {
          font-size: 1.2rem;
          margin: 0.5rem 0;
        }
      `,
      uploadArea: css`
        border: 2px dashed #adb5bd;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        margin: 1rem;
        cursor: pointer;
        background: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: all 0.3s ease;

        &:hover {
          border-color: #007bff;
          background: #f0f8ff;
        }

        @media (max-width: 768px) {
          padding: 1.5rem;
          margin: 0.5rem;
          font-size: 0.9rem;
        }
      `,
      fileInput: css`
        display: none;
      `,
      fileList: css`
        flex: 1;
        display: flex;
        flex-direction: column;
        gap: 1rem;
        padding: 1rem;
        overflow-y: auto;

        @media (max-width: 768px) {
          padding: 0.5rem;
          gap: 0.75rem;
        }
      `,
      fileItem: css`
        display: flex;
        flex-direction: column;
        padding: 1rem;
        border-radius: 8px;
        background: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: transform 0.2s;

        &:hover {
          transform: translateY(-2px);
        }

        @media (min-width: 769px) {
          flex-direction: row;
          justify-content: space-between;
          align-items: center;
        }
      `,
      fileInfo: css`
        flex: 1;
        margin-bottom: 0.75rem;
        color: #495057;

        @media (min-width: 769px) {
          margin-bottom: 0;
        }
      `,
      buttonGroup: css`
        display: flex;
        gap: 0.5rem;

        @media (max-width: 768px) {
          justify-content: space-between;
        }
      `,
      button: css`
        padding: 0.75rem 1.5rem;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        font-weight: 500;
        transition: all 0.2s ease;
        min-width: 80px;
        touch-action: manipulation; // Improve touch responsiveness

        &:hover {
          opacity: 0.9;
          transform: scale(1.02);
        }

        @media (max-width: 768px) {
          padding: 0.6rem 1rem;
          font-size: 0.9rem;
          flex: 1;
        }
      `,
      viewButton: css`
        background: #007bff;
        color: white;
      `,
      deleteButton: css`
        background: #dc3545;
        color: white;
      `,
      errorMessage: css`
        color: #dc3545;
        text-align: center;
        margin: 1rem;
        font-size: 0.9rem;

        @media (max-width: 768px) {
          margin: 0.5rem;
          font-size: 0.8rem;
        }
      `,
      noFiles: css`
        text-align: center;
        color: #6c757d;
        margin: 2rem 0;

        @media (max-width: 768px) {
          margin: 1rem 0;
          font-size: 0.9rem;
        }
      `
    };

    // Signals for reactive state
    const files = signal([]);
    const error = signal('');

    // Load files from localStorage on mount
    effect(() => {
      const savedFiles = localStorage.getItem('uploadedFiles');
      if (savedFiles) {
        files.value = JSON.parse(savedFiles);
      }
    });

    // Save files to localStorage whenever files signal changes
    effect(() => {
      localStorage.setItem('uploadedFiles', JSON.stringify(files.value));
    });

    // Convert file to base64
    const toBase64 = (file) => new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result);
      reader.onerror = (error) => reject(error);
    });

    // Handle file upload
    const handleFileUpload = async (e) => {
      const file = e.target.files[0];
      if (!file) return;

      // Validate file size (max 5MB)
      if (file.size > 5 * 1024 * 1024) {
        error.value = 'File size exceeds 5MB limit.';
        return;
      }

      try {
        const base64 = await toBase64(file);
        const newFile = {
          id: Date.now(),
          name: file.name,
          type: file.type,
          size: file.size,
          data: base64,
        };
        files.value = [...files.value, newFile];
        error.value = '';
      } catch (err) {
        error.value = 'Error processing file.';
      }
    };

    // Delete a file
    const deleteFile = (id) => {
      files.value = files.value.filter((file) => file.id !== id);
    };

    // View a file (open in new tab or download)
    const viewFile = (file) => {
      const link = document.createElement('a');
      link.href = file.data;
      link.download = file.name;
      link.click();
    };

    // Main App component using JSX
    const App = () => (
      <div class={styles.container}>
        <h1 class={styles.header}>File Uploader</h1>
        <label class={styles.uploadArea}>
          Tap to upload a file (max 5MB)
          <input
            type="file"
            class={styles.fileInput}
            onChange={handleFileUpload}
          />
        </label>
        {error.value && <div class={styles.errorMessage}>{error.value}</div>}
        <div class={styles.fileList}>
          {files.value.length === 0 && <p class={styles.noFiles}>No files uploaded yet.</p>}
          {files.value.map((file) => (
            <div key={file.id} class={styles.fileItem}>
              <span class={styles.fileInfo}>
                {file.name} ({(file.size / 1024).toFixed(2)} KB)
              </span>
              <div class={styles.buttonGroup}>
                <button class={`${styles.button} ${styles.viewButton}`} onClick={() => viewFile(file)}>
                  View
                </button>
                <button class={`${styles.button} ${styles.deleteButton}`} onClick={() => deleteFile(file.id)}>
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    );

export default App
