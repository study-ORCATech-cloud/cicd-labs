def greet(name):
    return f"Hello, {name} from a Jenkins Freestyle job!"

if __name__ == "__main__":
    # This script will be executed by Jenkins.
    # It prints a greeting and then a list of files in its current directory.
    print(greet("Student"))

    # Example of accessing environment variables Jenkins might set (optional for this lab)
    # import os
    # build_number = os.getenv('BUILD_NUMBER', 'N/A')
    # job_name = os.getenv('JOB_NAME', 'N/A')
    # print(f"This is build #{build_number} for job {job_name}.")

    print("\nPython script executed successfully by Jenkins.") 