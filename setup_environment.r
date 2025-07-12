# 📦 List of packages to install
cran_packages <- c("dplyr", "tidyr", "ggplot2", "knitr", "devtools")

# 🏗️ Install CRAN packages
install.packages(cran_packages, repos = "https://cloud.r-project.org")

# 🕒 Optional: increase download timeout for large GitHub packages
options(timeout = 600)

# 🧬 Install GitHub-only package (wpp2022)
if (!requireNamespace("wpp2022", quietly = TRUE)) {
  devtools::install_github("PPgp/wpp2022")
}

# ✅ Load everything
lapply(c(cran_packages, "wpp2022"), library, character.only = TRUE)
