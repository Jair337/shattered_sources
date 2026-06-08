import json
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox

# Matplotlib imports for Tkinter integration
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

# Scikit-learn imports
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import (roc_curve, roc_auc_score, precision_recall_curve,
                             average_precision_score, f1_score, precision_score,
                             recall_score, confusion_matrix, ConfusionMatrixDisplay,
                             accuracy_score)
from sklearn.calibration import calibration_curve


class MLModelDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Seerist AI - Logistic Regression Dashboard")
        self.root.geometry("1200x800")

        # UI Variables
        self.noise_var = tk.DoubleVar(value=0.10)
        self.test_size_var = tk.DoubleVar(value=0.20)
        self.max_iter_var = tk.IntVar(value=1000)

        self.setup_ui()

    def setup_ui(self):
        # --- LEFT PANEL: Controls ---
        control_frame = ttk.Frame(self.root, width=300, padding=15, relief="ridge")
        control_frame.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Label(control_frame, text="Model Parameters", font=("Helvetica", 14, "bold")).pack(pady=(0, 15))

        # Noise Slider
        ttk.Label(control_frame, text="Data Noise / Randomness (0 to 1.0):").pack(anchor=tk.W)
        ttk.Scale(control_frame, from_=0.0, to=1.0, variable=self.noise_var, orient=tk.HORIZONTAL).pack(fill=tk.X,
                                                                                                        pady=(0, 5))
        ttk.Label(control_frame, textvariable=self.noise_var).pack(anchor=tk.W, pady=(0, 15))

        # Test Size Slider
        ttk.Label(control_frame, text="Test Set Size (0.1 to 0.5):").pack(anchor=tk.W)
        ttk.Scale(control_frame, from_=0.1, to=0.5, variable=self.test_size_var, orient=tk.HORIZONTAL).pack(fill=tk.X,
                                                                                                            pady=(0, 5))
        ttk.Label(control_frame, textvariable=self.test_size_var).pack(anchor=tk.W, pady=(0, 15))

        # Max Iterations Entry
        ttk.Label(control_frame, text="Max Training Iterations:").pack(anchor=tk.W)
        ttk.Entry(control_frame, textvariable=self.max_iter_var).pack(fill=tk.X, pady=(0, 20))

        # Run Button
        run_btn = ttk.Button(control_frame, text="🚀 Train Model & Plot", command=self.run_pipeline)
        run_btn.pack(fill=tk.X, pady=10)

        # Results Text Box
        ttk.Label(control_frame, text="Results:", font=("Helvetica", 12, "bold")).pack(anchor=tk.W, pady=(20, 5))
        self.results_text = tk.Text(control_frame, height=20, width=35, wrap=tk.WORD, font=("Consolas", 9))
        self.results_text.pack(fill=tk.BOTH, expand=True)

        # --- RIGHT PANEL: Notebook for Graphs ---
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Dictionary to hold the canvas for each tab
        self.tabs = {}
        tab_names = ["ROC Curve", "PR Curve", "Distributions", "Thresholds", "Confusion Matrix", "Feature Weights",
                     "Calibration"]

        for name in tab_names:
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=name)
            self.tabs[name] = frame

    def run_pipeline(self):
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "Loading data and engineering features...\n")
        self.root.update()

        try:
            # 1. LOAD DATA
            with open('../synthetic_seerist_events.json', 'r') as f:
                data = json.load(f)
            df = pd.json_normalize(data['events'])

            # 2. FEATURE ENGINEERING
            df['source_count'] = df['provenance.source_count'].fillna(0)
            df['human_reviewed'] = df['provenance.human_reviewed'].astype(int)
            disruption_map = {"none": 0, "minimal": 1, "localized": 2, "moderate": 3, "significant": 4, "severe": 5}
            df['disruption_score'] = df['impact.likely_disruption'].map(disruption_map).fillna(0)

            df_encoded = pd.get_dummies(df, columns=['category', 'region'], dummy_na=False)
            one_hot_cols = [c for c in df_encoded.columns if c.startswith('category_') or c.startswith('region_')]

            mlb_domains = MultiLabelBinarizer()
            domains_encoded = pd.DataFrame(
                mlb_domains.fit_transform(
                    df['impact.affected_domains'].apply(lambda x: x if isinstance(x, list) else [])),
                columns=[f"domain_{c}" for c in mlb_domains.classes_], index=df.index)

            mlb_tags = MultiLabelBinarizer()
            tags_encoded = pd.DataFrame(
                mlb_tags.fit_transform(df['tags'].apply(lambda x: x if isinstance(x, list) else [])),
                columns=[f"tag_{c}" for c in mlb_tags.classes_], index=df.index)

            feature_cols = ['severity', 'source_count', 'human_reviewed', 'disruption_score'] + one_hot_cols
            X = pd.concat([df_encoded[feature_cols], domains_encoded, tags_encoded], axis=1)

            # 3. TARGET VARIABLE (Using GUI Noise Variable)
            base_rule = (df['severity'] >= 4) | (
                df['impact.affected_domains'].apply(lambda x: 'employee_safety' in x if isinstance(x, list) else False))
            noise_val = self.noise_var.get()
            np.random.seed(42)
            noise = np.random.choice([0, 1], size=len(df), p=[1 - noise_val, noise_val])
            y = base_rule.astype(int) ^ noise

            # 4. TRAIN MODEL (Using GUI variables)
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=self.test_size_var.get(),
                                                                random_state=42)
            model = LogisticRegression(max_iter=self.max_iter_var.get())
            model.fit(X_train, y_train)
            probabilities = model.predict_proba(X_test)[:, 1]

            # Find best threshold for F1
            thresholds = np.arange(0.0, 1.01, 0.01)
            f1_scores = [f1_score(y_test, (probabilities >= t).astype(int), zero_division=0) for t in thresholds]
            best_idx = np.argmax(f1_scores)
            best_threshold = thresholds[best_idx]
            best_preds = (probabilities >= best_threshold).astype(int)
            auc_score = roc_auc_score(y_test, probabilities)

            # Update Text Results
            res = f"🌟 AUC SCORE: {auc_score:.3f}\n"
            res += f"🥇 BEST THRESHOLD: {best_threshold:.2f}\n"
            res += f"   - F1-Score: {f1_scores[best_idx]:.3f}\n"
            res += f"   - Accuracy: {accuracy_score(y_test, best_preds):.3f}\n\n"
            res += "--- Top Positive Features ---\n"

            weights = model.coef_[0]
            idx = np.argsort(weights)
            top_pos = [X.columns[i] for i in idx[-5:]][::-1]
            for f in top_pos: res += f" + {f}\n"

            self.results_text.insert(tk.END, res)

            # 5. GENERATE GRAPHS IN TKINTER
            self.plot_roc(y_test, probabilities, auc_score)
            self.plot_pr(y_test, probabilities)
            self.plot_distribution(y_test, probabilities, best_threshold)
            self.plot_thresholds(y_test, probabilities, thresholds, f1_scores, best_threshold)
            self.plot_confusion(y_test, best_preds, best_threshold)
            self.plot_weights(X.columns, weights)
            self.plot_calibration(y_test, probabilities)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

    # --- PLOTTING HELPER FUNCTIONS ---
    def embed_plot(self, fig, tab_name):
        frame = self.tabs[tab_name]
        for widget in frame.winfo_children():
            widget.destroy()  # Clear old plots
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2Tk(canvas, frame)
        toolbar.update()

    def plot_roc(self, y_test, probabilities, auc_score):
        fig = Figure(figsize=(6, 5), dpi=100)
        ax = fig.add_subplot(111)
        fpr, tpr, _ = roc_curve(y_test, probabilities)
        ax.plot(fpr, tpr, color='blue', lw=2, label=f'AUC = {auc_score:.3f}')
        ax.plot([0, 1], [0, 1], color='gray', linestyle='--')
        ax.set_title('ROC Curve')
        ax.set_xlabel('False Positive Rate')
        ax.set_ylabel('True Positive Rate')
        ax.legend(loc='lower right')
        ax.grid(True, alpha=0.3)
        self.embed_plot(fig, "ROC Curve")

    def plot_pr(self, y_test, probabilities):
        fig = Figure(figsize=(6, 5), dpi=100)
        ax = fig.add_subplot(111)
        precisions, recalls, _ = precision_recall_curve(y_test, probabilities)
        ap = average_precision_score(y_test, probabilities)
        ax.plot(recalls, precisions, color='purple', lw=2, label=f'AP = {ap:.3f}')
        ax.set_title('Precision-Recall Curve')
        ax.set_xlabel('Recall')
        ax.set_ylabel('Precision')
        ax.legend(loc='lower left')
        ax.grid(True, alpha=0.3)
        self.embed_plot(fig, "PR Curve")

    def plot_distribution(self, y_test, probabilities, best_threshold):
        fig = Figure(figsize=(6, 5), dpi=100)
        ax = fig.add_subplot(111)
        ax.hist(probabilities[y_test == 0], bins=30, alpha=0.6, color='blue', label='Class 0')
        ax.hist(probabilities[y_test == 1], bins=30, alpha=0.6, color='red', label='Class 1')
        ax.axvline(best_threshold, color='green', linestyle='--', lw=2, label='Threshold')
        ax.set_title('Probability Distribution')
        ax.legend()
        ax.grid(True, alpha=0.3)
        self.embed_plot(fig, "Distributions")

    def plot_thresholds(self, y_test, probabilities, thresholds, f1_scores, best_threshold):
        fig = Figure(figsize=(6, 5), dpi=100)
        ax = fig.add_subplot(111)
        acc = [accuracy_score(y_test, (probabilities >= t).astype(int)) for t in thresholds]
        ax.plot(thresholds, acc, label='Accuracy', linestyle=':', color='blue')
        ax.plot(thresholds, f1_scores, label='F1-Score', color='purple', lw=2)
        ax.axvline(best_threshold, color='red', lw=2, label='Optimal Threshold')
        ax.set_title('Metrics vs Threshold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        self.embed_plot(fig, "Thresholds")

    def plot_confusion(self, y_test, best_preds, best_threshold):
        fig = Figure(figsize=(6, 5), dpi=100)
        ax = fig.add_subplot(111)
        cm = confusion_matrix(y_test, best_preds)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Ignore', 'Analyze'])
        disp.plot(ax=ax, cmap='Blues', colorbar=False)
        ax.set_title(f'Confusion Matrix (Thresh: {best_threshold:.2f})')
        self.embed_plot(fig, "Confusion Matrix")

    def plot_weights(self, features, weights):
        fig = Figure(figsize=(6, 5), dpi=100)
        ax = fig.add_subplot(111)
        idx = np.argsort(weights)
        idx_top = np.concatenate((idx[:5], idx[-5:]))  # Top 5 pos, Top 5 neg
        colors = ['red' if w < 0 else 'green' for w in weights[idx_top]]
        ax.barh(np.array(features)[idx_top], weights[idx_top], color=colors)
        ax.set_title('Top Feature Weights')
        fig.subplots_adjust(left=0.35)  # Make room for long labels
        self.embed_plot(fig, "Feature Weights")

    def plot_calibration(self, y_test, probabilities):
        fig = Figure(figsize=(6, 5), dpi=100)
        ax = fig.add_subplot(111)
        prob_true, prob_pred = calibration_curve(y_test, probabilities, n_bins=10)
        ax.plot(prob_pred, prob_true, marker='o', lw=2, label='Model')
        ax.plot([0, 1], [0, 1], linestyle='--', color='gray', label='Perfectly Calibrated')
        ax.set_title('Calibration Curve')
        ax.legend()
        ax.grid(True, alpha=0.3)
        self.embed_plot(fig, "Calibration")


if __name__ == "__main__":
    root = tk.Tk()
    app = MLModelDashboard(root)
    root.mainloop()