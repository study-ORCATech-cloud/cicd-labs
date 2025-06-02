# TODO_BASE_IMAGE: Specify the base image.
# For a Python application, consider using an official Python slim image for a smaller footprint.
# Hint: Starts with `FROM python:...`

# TODO_WORKDIR: Set the working directory inside the container.
# This will be the base directory for subsequent commands like COPY and RUN.
# Hint: `WORKDIR /chosen_directory_name`

# TODO_COPY_REQUIREMENTS: Copy the requirements.txt file into the container's working directory.
# This allows Docker to cache this layer if requirements don't change.
# Hint: `COPY source_path_on_host destination_in_image`

# TODO_INSTALL_DEPS: Install the Python dependencies using pip.
# Make sure to install packages listed in the requirements.txt you just copied.
# Hint: `RUN pip install ...`

# TODO_COPY_APP: Copy the rest of the application code (the ./app directory) 
# from your host into the container's working directory.
# Hint: `COPY ./app/ .` (if your WORKDIR is already set to the target app directory)

# TODO_EXPOSE_PORT: Expose the port that the Flask application will run on.
# The sample Flask app (app/main.py) is set to run on port 5000.
# Hint: `EXPOSE desired_port_number`

# TODO_CMD: Specify the default command to run when the container starts.
# This command should execute your Python Flask application (main.py).
# Hint: `CMD ["executable", "argument1", "argument2", ...]` 