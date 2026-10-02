import { useEffect, useState } from "react";
import "./App.css";

const wasteTypes = [
  {
    name: "Organic",
    icon: "✿",
    color: "organic",
    detail: "Food scraps and compostable waste",
  },
  {
    name: "Inorganic",
    icon: "♻",
    color: "inorganic",
    detail: "Paper, plastic, glass and metal",
  },
];

const categoryDetails = {
  organic: {
    title: "Organic",
    icon: "✿",
    description: "This item was identified as organic waste.",
    tip: "Food scraps and other suitable organic materials can be directed to composting.",
  },
  inorganic: {
    title: "Inorganic",
    icon: "♻",
    description:
      "This item was identified as inorganic waste, a category that includes paper, plastic, glass and metal in this project.",
    tip: "Separate materials where possible and follow your local recycling and disposal guidelines.",
  },
};

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    return () => {
      if (previewUrl) URL.revokeObjectURL(previewUrl);
    };
  }, [previewUrl]);

  function handleFileChange(event) {
    const file = event.target.files?.[0];

    if (!file) return;

    if (!file.type.startsWith("image/")) {
      setError("Please choose an image file.");
      return;
    }

    setSelectedFile(file);
    setPreviewUrl(URL.createObjectURL(file));
    setResult(null);
    setError("");
  }

  async function handleClassify() {
    if (!selectedFile) {
      setError("Choose a waste image before starting the analysis.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("The image could not be classified. Please try again.");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(
        err.message || "Could not connect to the classification service."
      );
    } finally {
      setLoading(false);
    }
  }

  function handleReset() {
    setSelectedFile(null);
    setPreviewUrl("");
    setResult(null);
    setError("");

    const input = document.getElementById("waste-image-input");
    if (input) input.value = "";
  }

  const resultDetails = result
    ? categoryDetails[result.category.toLowerCase()]
    : null;

  return (
    <div className="app-shell">
      <div className="ambient ambient-one" />
      <div className="ambient ambient-two" />

      <header className="topbar">
        <a className="brand" href="#home" aria-label="EcoSort home">
          <span className="brand-mark">
            <span>↻</span>
          </span>
          <span className="brand-name">
            Eco<span>Sort</span>
            <small>SMART WASTE INTELLIGENCE</small>
          </span>
        </a>

        <nav className="nav-links">
          <a href="#how-it-works">How it works</a>
          <a href="#waste-types">Waste categories</a>
        </nav>

        <a className="status-pill" href="#classifier">
          <span className="status-dot" />
          AI classifier online
        </a>
      </header>

      <main id="home">
        <section className="hero">
          <div className="hero-copy">
            <div className="eyebrow">
              <span className="eyebrow-line" />
              WASTE SORTING, REIMAGINED
            </div>

            <h1>
              Waste less.
              <br />
              <span>Sort smarter.</span>
            </h1>

            <p className="hero-description">
              Turn a simple photo into a smarter disposal decision. EcoSort
              uses a custom-built image classification model to identify waste
              as Organic or Inorganic and suggest a suitable bin category.
            </p>

            <a className="hero-cta" href="#classifier">
              Classify your waste <span>↓</span>
            </a>

            <div className="hero-note">
              <span className="note-icon">✦</span>
              Image-based classification · 2 waste categories
            </div>
          </div>

          <div
            className="hero-visual"
            aria-label="Illustration of waste sorting"
          >
            <div className="visual-orbit orbit-one" />
            <div className="visual-orbit orbit-two" />

            <div className="visual-label label-top">
              <span className="label-pulse" />
              AI VISION SYSTEM
            </div>

            <div className="visual-center">
              <div className="leaf-art leaf-back">❧</div>
              <div className="visual-recycle">↻</div>
              <div className="visual-caption">
                GIVE WASTE
                <br />
                A NEW PURPOSE
              </div>
            </div>

            <div className="floating-tag tag-left">
              <span className="tag-icon">✿</span>
              <span>
                <strong>Identify</strong>
                <small>Waste category</small>
              </span>
            </div>

            <div className="floating-tag tag-right">
              <span className="tag-icon">⌁</span>
              <span>
                <strong>Recommend</strong>
                <small>Disposal bin</small>
              </span>
            </div>

            <div className="visual-label label-bottom">
              <span>01</span> IMAGE IN <i /> <span>02</span> SMART SORTING
            </div>
          </div>
        </section>

        <section className="process-strip" aria-label="Classification workflow">
          <div className="process-heading">
            <span className="mini-kicker">THE PROCESS</span>
            <strong>From photo to purpose</strong>
          </div>

          <div className="process-step">
            <span className="process-icon">▧</span>
            <span>
              <small>STEP 01</small>
              <strong>Upload image</strong>
            </span>
          </div>

          <span className="process-arrow">→</span>

          <div className="process-step">
            <span className="process-icon">✳</span>
            <span>
              <small>STEP 02</small>
              <strong>Custom CNN classifies</strong>
            </span>
          </div>

          <span className="process-arrow">→</span>

          <div className="process-step">
            <span className="process-icon">♻</span>
            <span>
              <small>STEP 03</small>
              <strong>Get bin guidance</strong>
            </span>
          </div>
        </section>

        <section className="classifier-section" id="classifier">
          <div className="section-heading">
            <div>
              <div className="eyebrow">
                <span className="eyebrow-line" />
                TRY THE CLASSIFIER
              </div>

              <h2>What goes where?</h2>

              <p>
                Upload a picture of a waste item and let the model analyze it.
              </p>
            </div>

            <div className="model-badge">
              <span className="model-badge-icon">✳</span>
              <span>
                <strong>Custom CNN</strong>
                <small>Trained from scratch</small>
              </span>
            </div>
          </div>

          <div className="classifier-grid">
            <div className="upload-card">
              <div className="card-topline">
                <span className="card-index">01 / INPUT</span>
                <span className="card-status">
                  <span className="status-dot" />
                  Ready for image
                </span>
              </div>

              <label
                className={`upload-zone ${previewUrl ? "has-image" : ""}`}
                htmlFor="waste-image-input"
              >
                {previewUrl ? (
                  <>
                    <img
                      className="image-preview"
                      src={previewUrl}
                      alt="Selected waste item preview"
                    />
                    <span className="preview-overlay">
                      <span className="preview-edit-icon">↻</span>
                      Change image
                    </span>
                  </>
                ) : (
                  <div className="upload-prompt">
                    <div className="upload-icon-wrap">
                      <span className="upload-icon">↑</span>
                    </div>
                    <strong>Drop your waste image here</strong>
                    <span>or click to browse your device</span>
                    <small>JPG, PNG, WEBP · Image files only</small>
                  </div>
                )}
              </label>

              <input
                id="waste-image-input"
                className="file-input"
                type="file"
                accept="image/*"
                onChange={handleFileChange}
              />

              <div className="file-info">
                <span className="file-info-icon">▧</span>
                <span className="file-info-text">
                  <strong>
                    {selectedFile ? selectedFile.name : "No image selected"}
                  </strong>
                  <small>
                    {selectedFile
                      ? `${(selectedFile.size / 1024 / 1024).toFixed(2)} MB · Ready to analyze`
                      : "Your image will appear here"}
                  </small>
                </span>

                {selectedFile && (
                  <button
                    className="remove-file"
                    type="button"
                    onClick={handleReset}
                    aria-label="Remove selected image"
                  >
                    ×
                  </button>
                )}
              </div>

              <button
                className="classify-button"
                type="button"
                onClick={handleClassify}
                disabled={!selectedFile || loading}
              >
                {loading ? (
                  <>
                    <span className="button-spinner" />
                    Analyzing image...
                  </>
                ) : (
                  <>
                    Analyze my waste <span>↗</span>
                  </>
                )}
              </button>

              <p className="privacy-note">
                <span>◇</span> Image is processed by your local project API.
              </p>

              {error && (
                <div className="error-message" role="alert">
                  <span>!</span> {error}
                </div>
              )}
            </div>

            <div className={`result-card ${result ? "result-ready" : ""}`}>
              <div className="card-topline">
                <span className="card-index">02 / AI OUTPUT</span>
                <span className={`result-state ${result ? "complete" : ""}`}>
                  <span className="status-dot" />
                  {result ? "Analysis complete" : "Awaiting image"}
                </span>
              </div>

              {result && resultDetails ? (
                <div className="result-content">
                  <div className={`result-symbol ${result.category.toLowerCase()}`}>
                    {resultDetails.icon}
                  </div>

                  <div className="result-kicker">DETECTED CATEGORY</div>
                  <h3>{resultDetails.title}</h3>

                  <p className="result-description">
                    {resultDetails.description}
                  </p>

                  <div className="confidence-block">
                    <div className="confidence-label">
                      <span>Model confidence</span>
                      <strong>{Number(result.confidence).toFixed(2)}%</strong>
                    </div>

                    <div
                      className="confidence-track"
                      role="progressbar"
                      aria-label="Model confidence"
                      aria-valuemin="0"
                      aria-valuemax="100"
                      aria-valuenow={Number(result.confidence)}
                    >
                      <div
                        className="confidence-fill"
                        style={{
                          width: `${Math.min(
                            100,
                            Math.max(0, Number(result.confidence))
                          )}%`,
                        }}
                      />
                    </div>
                  </div>

                  <div className="bin-recommendation">
                    <div className="bin-icon">♻</div>
                    <div>
                      <small>RECOMMENDED DISPOSAL</small>
                      <strong>{result.recommended_bin}</strong>
                    </div>
                    <span className="bin-check">✓</span>
                  </div>

                  <div className="result-tip">
                    <span>✦</span>
                    <p>{resultDetails.tip}</p>
                  </div>

                  <button className="try-again-button" onClick={handleReset}>
                    Classify another item <span>↗</span>
                  </button>
                </div>
              ) : (
                <div className="empty-result">
                  <div className="empty-illustration">
                    <div className="scan-ring ring-a" />
                    <div className="scan-ring ring-b" />
                    <div className="scan-object">?</div>
                    <span className="scan-spark spark-a">✦</span>
                    <span className="scan-spark spark-b">✧</span>
                  </div>

                  <h3>Your result will appear here</h3>

                  <p>
                    Once you upload an image and start the analysis, you’ll see
                    the predicted waste category, confidence, and suggested bin.
                  </p>

                  <div className="empty-steps">
                    <span>01 Select image</span>
                    <i />
                    <span>02 Run analysis</span>
                  </div>
                </div>
              )}
            </div>
          </div>
        </section>

        <section className="categories-section" id="waste-types">
          <div className="section-heading categories-heading">
            <div>
              <div className="eyebrow">
                <span className="eyebrow-line" />
                TWO WASTE CLASSES
              </div>

              <h2>Know your waste.</h2>

              <p>
                The custom CNN classifies waste into Organic and Inorganic
                categories.
              </p>
            </div>

            <span className="category-count">
              02 <small>CATEGORIES</small>
            </span>
          </div>

          <div className="category-grid">
            {wasteTypes.map((type, index) => (
              <article
                className={`category-card ${type.color}`}
                key={type.name}
              >
                <div className="category-card-top">
                  <span className="category-number">0{index + 1}</span>
                  <span className="category-icon">{type.icon}</span>
                </div>

                <h3>{type.name}</h3>
                <p>{type.detail}</p>
                <span className="category-card-arrow">↗</span>
              </article>
            ))}
          </div>

          <p className="category-note">
            In this project, Inorganic includes the glass, metal, paper, and
            plastic images grouped together in the training dataset.
          </p>
        </section>

        <section className="how-section" id="how-it-works">
          <div className="how-intro">
            <div className="eyebrow">
              <span className="eyebrow-line" />
              BEHIND THE SORT
            </div>

            <h2>
              How EcoSort
              <br />
              <span>makes a decision.</span>
            </h2>

            <p>
              A simple image goes through a machine-learning pipeline to produce
              a category prediction and a practical disposal suggestion.
            </p>
          </div>

          <div className="how-timeline">
            <div className="timeline-item">
              <span className="timeline-number">01</span>
              <div>
                <h3>Image input</h3>
                <p>Choose a photo of the item you want to sort.</p>
              </div>
              <span className="timeline-icon">▧</span>
            </div>

            <div className="timeline-item">
              <span className="timeline-number">02</span>
              <div>
                <h3>Image preparation</h3>
                <p>The image is resized and prepared for the model.</p>
              </div>
              <span className="timeline-icon">⌗</span>
            </div>

            <div className="timeline-item">
              <span className="timeline-number">03</span>
              <div>
                <h3>Custom CNN classification</h3>
                <p>
                  A CNN trained from scratch predicts Organic or Inorganic.
                </p>
              </div>
              <span className="timeline-icon">✳</span>
            </div>

            <div className="timeline-item">
              <span className="timeline-number">04</span>
              <div>
                <h3>Disposal guidance</h3>
                <p>The result is paired with a recommended bin category.</p>
              </div>
              <span className="timeline-icon">♻</span>
            </div>
          </div>
        </section>

        <section className="impact-banner">
          <div className="impact-symbol">✿</div>
          <div>
            <span>SMALL ACTIONS. BETTER HABITS.</span>
            <h2>Make the next toss a thoughtful one.</h2>
          </div>
          <a href="#classifier">
            Try the classifier <span>↗</span>
          </a>
        </section>
      </main>

      <footer className="footer">
        <a className="brand footer-brand" href="#home">
          <span className="brand-mark">
            <span>↻</span>
          </span>
          <span className="brand-name">
            Eco<span>Sort</span>
            <small>SMART WASTE INTELLIGENCE</small>
          </span>
        </a>

        <p>
          Image-based waste classification · Built for a smarter sorting habit.
        </p>

        <span className="footer-credit">A STUDENT AI/ML PROJECT</span>
      </footer>
    </div>
  );
}

export default App;