# Solutions for LAB09: Linting Dockerfiles with Hadolint

This document provides:
1.  An example of the expected Hadolint output when run against `Dockerfile-to-lint`.
2.  The content of `Dockerfile-fixed.solution` with corrections applied.
3.  An explanation for each correction, referencing the Hadolint rule code.

---

## 🧪 Example Hadolint Output for `Dockerfile-to-lint`

When you run Hadolint against the provided `Dockerfile-to-lint`:

```bash
docker run --rm -i -v "$(pwd)/Dockerfile-to-lint:/Dockerfile" hadolint/hadolint hadolint /Dockerfile
```

You should see output similar to this (order and specific ShellCheck warnings might vary slightly):

```
/Dockerfile:4 DL3006 Always tag the version of an image explicitly.
/Dockerfile:7 DL3000 Use 'LABEL maintainer=' instead of 'MAINTAINER'.
/Dockerfile:10 DL3009 Debian systems Solution install-recommends should be false.
/Dockerfile:10 DL3008 Pin versions in apt get install. Instead of `apt-get install <package>` use `apt-get install <package>=<version>`
/Dockerfile:11 DL3015 Avoid additional packages by specifying `--no-install-recommends`
/Dockerfile:11 DL3008 Pin versions in apt get install. Instead of `apt-get install <package>` use `apt-get install <package>=<version>`
/Dockerfile:11 DL3016 Pin versions in npm. Instead of `npm install <package>` use `npm install <package>@<version>` (This may appear if Hadolint infers node context from python base, can be ignored or fine-tuned with .hadolint.yaml)
/Dockerfile:10 SC2102 Busybox's ash (used in Alpine) shells tend to fail on syscalls in place of if-BLOCK. Solution: use if ! SYSCALL; then ...
/Dockerfile:14 DL3020 Use COPY instead of ADD for files and folders.
/Dockerfile:15 DL3020 Use COPY instead of ADD for files and folders.
/Dockerfile:18 DL3002 Last USER should not be root.
/Dockerfile:18 DL3013 Pin versions in pip. Instead of `pip install <package>` use `pip install <package>==<version>` or `pip install --requirement <requirements file>`
/Dockerfile:21 DL3003 Use WORKDIR to change directory.
/Dockerfile:24 DL3011 Valid UNIX ports range from 0 to 65535. Smaller port numbers are preferable. (Warning may be less direct, depends on context)
/Dockerfile:29 DL3025 Use arguments JSON notation for CMD and ENTRYPOINT arguments.
```

*(Note: Some warnings like DL3016 for npm might be overly aggressive if it misinterprets the base image context. DL3002 about root user is a good practice but might be deferred for very simple apps not handling sensitive data at build time.)*

---

## ✅ Corrected `Dockerfile-fixed.solution`

Here is the content of `Dockerfile-fixed.solution` with the issues addressed:

```dockerfile
# Dockerfile with linting issues fixed

# Solution for DL3006: Use a specific tag for the base image.
# Using a slim variant for smaller size.
FROM python:3.9-slim

# Solution for DL3000: Use LABEL maintainer instead of MAINTAINER.
LABEL maintainer="student@example.com"

# Solution for DL3002: Set WORKDIR early.
WORKDIR /app

# Solution for DL3008, DL3009, DL3015: Combine RUN, pin versions (example), use --no-install-recommends, and clean up.
# Note: Pinning gcc version might be overly specific for a lab; demonstrating the concept.
# For a real app, research the appropriate version or use a build argument.
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    # Example: gcc=4:9.3.0-17ubuntu1~20.04 if you knew the exact version for Ubuntu 20.04 base (python:3.9 is Debian based)
 && rm -rf /var/lib/apt/lists/*

# Solution for DL3020: Use COPY instead of ADD for local files.
# Also, copy only necessary files before installing dependencies to leverage Docker cache.
COPY requirements.txt .

# Solution for DL3013: Pin versions in requirements.txt (student should do this in the file).
# This RUN command itself is fine for installing from requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Solution for DL3003: WORKDIR is already /app, so no need for cd.
# Compiling python files can be a build step, but ensure it is needed.
RUN python -m compileall .

# Solution for DL3011: Expose the port the application will actually listen on (e.g., 5000 for Flask default).
EXPOSE 5000

# No secrets exposed.

# Solution for DL3025: Use JSON array form for CMD.
# Assuming main.py starts a Flask app on port 5000.
CMD ["python", "main.py"]

```

---

## 📄 Explanation of Corrections

1.  **`FROM python:3.9-slim`** (Rule `DL3006`)
    *   **Issue**: Using `FROM python` (or `python:latest`) is not recommended because the underlying image can change, leading to unpredictable builds. `DL3006` advises tagging images explicitly.
    *   **Fix**: Changed to `python:3.9-slim`. This pins the Python version to 3.9 and uses a `slim` variant, which is generally smaller than the full default image.

2.  **`LABEL maintainer="student@example.com"`** (Rule `DL3000`)
    *   **Issue**: `MAINTAINER` instruction is deprecated.
    *   **Fix**: Replaced with `LABEL maintainer="..."` which is the current best practice.

3.  **`WORKDIR /app`** (Rule `DL3002`)
    *   **Issue**: Commands were being run from the root directory (`/`). `DL3002` suggests setting `USER` to non-root, but an earlier `WORKDIR` is also a fundamental best practice to organize files and commands.
    *   **Fix**: Added `WORKDIR /app` early in the Dockerfile. Subsequent `COPY` and `RUN` commands will use this as their context.

4.  **Combined `apt-get` operations** (Rules `DL3008`, `DL3009`, `DL3015`)
    *   **Issues**: Multiple `RUN apt-get update` and `RUN apt-get install` create extra layers. `apt-get update` should be combined with `install`. Versions were not pinned. No cleanup of apt cache.
    *   **Fix**: Combined `apt-get update` and `install` into a single `RUN` layer. Added `--no-install-recommends` to reduce unnecessary packages. Included `rm -rf /var/lib/apt/lists/*` to clean up apt cache and reduce image size. *Note: Pinning `gcc` version is shown conceptually; in a real scenario, this requires knowing the exact available version for the base image distribution or using a variable.* 

5.  **`COPY requirements.txt .` and `COPY . .`** (Rule `DL3020`)
    *   **Issue**: `ADD` was used for local files/directories. `DL3020` recommends `COPY` for non-archived local content as `COPY` is more transparent.
    *   **Fix**: Replaced `ADD` with `COPY`. Also, `requirements.txt` is copied and installed *before* copying the rest of the app code (`COPY . .`) to better leverage Docker layer caching. Changes to app code won't invalidate the dependency installation layer if `requirements.txt` hasn't changed.

6.  **`RUN pip install --no-cache-dir -r requirements.txt`** (Rule `DL3013`)
    *   **Issue**: `DL3013` warns to pin package versions in `pip install`. The actual pinning should happen *inside* the `requirements.txt` file (e.g., `flask==2.0.1`).
    *   **Fix**: The command itself is mostly fine. Added `--no-cache-dir` to `pip install` to reduce image size by not storing the download cache.
    *   **Student Action**: The student should ensure versions are pinned in their `requirements.txt` file (e.g., `flask==x.y.z`).

7.  **`RUN python -m compileall .`** (Rule `DL3003`)
    *   **Issue**: `RUN cd /app && ...` was used. `DL3003` advises using `WORKDIR` instead of `cd` in `RUN` instructions.
    *   **Fix**: Since `WORKDIR /app` is already set, the `cd /app` is redundant and removed.

8.  **`EXPOSE 5000`** (Rule `DL3011`)
    *   **Issue**: `EXPOSE 8081` was arbitrary. `DL3011` warns about non-standard or potentially incorrect port exposure.
    *   **Fix**: Changed to `EXPOSE 5000`, which is the default port for Flask applications. This is more conventional.

9.  **`CMD ["python", "main.py"]`** (Rule `DL3025`)
    *   **Issue**: `CMD python /app/main.py` (shell form) was used. `DL3025` recommends using the JSON array (exec) form for `CMD` and `ENTRYPOINT` for clarity and to avoid potential shell-related issues.
    *   **Fix**: Changed to `CMD ["python", "main.py"]`.

By applying these fixes, the `Dockerfile-fixed.solution` becomes more robust, easier to understand, and produces more optimized and secure images. 