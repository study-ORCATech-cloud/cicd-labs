/**
 * Prints a custom message to the build log.
 * @param message The message to print.
 */
def printMessage(String message) {
    echo "[CustomSteps Shared Library]: ${message}"
}

/**
 * A simple function to simulate running Python tests for a given application path.
 * In a real shared library, this might involve more complex setup or reporting.
 * @param appPath The path to the application directory containing tests.
 * @param pytestPath Path to pytest executable (if not in default PATH for agent)
 */
def runPyTests(Map config = [:]) {
    String appPath = config.appPath ?: '.' // Default to current directory if not specified
    String pytestExecutable = config.pytestPath ?: 'pytest' // Default to 'pytest' if not specified
    
    echo "[CustomSteps Shared Library]: Attempting to run Python tests in '${appPath}/tests' using '${pytestExecutable}'."
    
    // In a real scenario, you might want to return a status or handle errors.
    // For this lab, we just execute the command.
    // Ensure the actual test files are in a subdirectory named 'tests' relative to appPath.
    sh "${pytestExecutable} ${appPath}/tests/"
    echo "[CustomSteps Shared Library]: Python tests execution attempt finished for '${appPath}/tests'."
}

/**
 * Installs Python dependencies from a requirements.txt file.
 * @param appPath The path to the application directory containing requirements.txt.
 * @param pipPath Path to pip executable (if not in default PATH for agent)
 */
def installPythonDependencies(Map config = [:]) {
    String appPath = config.appPath ?: '.'
    String pipExecutable = config.pipPath ?: 'pip' // Often 'pip3' or 'python3 -m pip'
    String pythonExecutable = config.pythonPath ?: 'python' // Often 'python3'

    echo "[CustomSteps Shared Library]: Installing Python dependencies from '${appPath}/requirements.txt'"
    sh "${pythonExecutable} -m pip install --upgrade pip"
    sh "${pipExecutable} install -r ${appPath}/requirements.txt"
    echo "[CustomSteps Shared Library]: Python dependencies installation finished."
}

// Make this script callable
return this; 