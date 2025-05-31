def greet(name):
    return f"Hello, {name} from a Jenkins Declarative Pipeline!"

if __name__ == "__main__":
    # This script will be executed by Jenkins.
    print(greet("Student"))
    print("\nPython script executed successfully by Jenkins Pipeline.") 