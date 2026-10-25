# LaTeX Collection and Hugo Site

A repository for organizing, compiling, and automatically publishing LaTeX documents to a Hugo-powered website hosted on GitHub Pages.

## Overview

This repository provides an automated workflow to manage multiple LaTeX projects. Each LaTeX project resides in its own folder and is automatically checked for build errors on changes. Tagging a release compiles the document, archives versioned and latest PDFs on the `gh-pages` branch, and updates the Hugo website.

## Project Structure

```text
.
├── latex_files/                  # Directory containing LaTeX projects
│   └── <project-name>/
│       └── main.tex              # Main entry point for the LaTeX document
├── site/                         # Hugo static site source (PaperMod theme)
│   ├── assets/                   # Site styling and CSS customizations
│   ├── layouts/                  # Custom Hugo layouts and shortcodes
│   ├── hugo.yaml                 # Hugo site configuration
│   └── themes/PaperMod/          # PaperMod theme submodule/files
├── .github/
│   ├── scripts/
│   │   ├── affected_tex.py       # Detects modified LaTeX documents from git diff
│   │   └── generate_hugo_posts.py # Generates Hugo posts for each LaTeX project
│   └── workflows/
│       ├── latex-check.yaml      # CI check to compile changed LaTeX documents
│       ├── latex-deploy.yaml     # Tag-triggered compilation, archiving, and deployment
│       └── deploy-hug.yaml       # Workflow to rebuild and deploy the Hugo site
└── README.md
```

## How It Works

### 1. LaTeX Projects
- Add each LaTeX project inside a subdirectory under `latex_files/` (for example, `latex_files/my-document/`).
- Every document must have a `main.tex` file at the root of its project folder.
- Supporting files (images, `.bib` files, `.sty` stylesheets, subfiles) should be placed in the respective project directory.

### 2. CI Verification (`latex-check.yaml`)
- Triggered on pushes and pull requests that modify `.tex`, `.bib`, `.sty`, or related asset files.
- The workflow determines which `main.tex` files depend on the modified files using `affected_tex.py` and compiles them with `latexmk` via GitHub Actions to prevent broken builds.

### 3. Release and Publishing (`latex-deploy.yaml`)
- Publishing is triggered by pushing a git tag with the format `<project-name>-v<version>`.
  - Example: `git tag test-v1.0.0 && git push origin test-v1.0.0`
- The workflow:
  1. Checks out the tagged commit and compiles `latex_files/<project-name>/main.tex`.
  2. Commits `<project-name>.pdf` and `<project-name>-<version>.pdf` to the `gh-pages` PDF archive.
  3. Builds the Hugo website, generating post entries and PDF download links.
  4. Deploys the site to GitHub Pages.

### 4. Hugo Site Deployment (`deploy-hug.yaml`)
- Triggered on changes to `site/**` or Hugo configuration files on the `main` branch, or via manual dispatch.
- Re-generates the site pages, copies existing archived PDFs, and deploys the updated site to GitHub Pages.

## Adding a New Document

1. Create a new folder under `latex_files/`:
   ```bash
   mkdir -p latex_files/my-paper
   ```
2. Create `latex_files/my-paper/main.tex` and any required assets.
3. Commit and push your changes to `main`:
   ```bash
   git add latex_files/my-paper/
   git commit -m "Add my-paper LaTeX project"
   git push origin main
   ```
4. To publish a new version of the PDF to the website:
   ```bash
   git tag my-paper-v1.0.0
   git push origin my-paper-v1.0.0
   ```

## Local Development

### Compiling LaTeX Locally
You can compile any document using `latexmk` or `pdflatex`:
```bash
cd latex_files/test
latexmk -pdf main.tex
```

### Running the Hugo Site Locally
Make sure you have [Hugo](https://gohugo.io/) (extended edition) installed:
```bash
cd site
hugo server
```

## License

This repository is licensed under the GNU General Public License v2 (GPL-2.0). See the [LICENSE](LICENSE) file for details.