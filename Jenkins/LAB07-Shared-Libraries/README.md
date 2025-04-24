# LAB07 - Shared Libraries in Jenkins

In this lab, you’ll modularize your CI/CD logic using **Jenkins Shared Libraries**, which let you reuse functions and pipeline components across multiple Jenkinsfiles.

---

## 🎯 Objectives

By the end of this lab, you will:
- Create a custom shared library for Jenkins pipelines
- Define a simple `vars/` method (e.g., `sayHello`) and call it from Jenkinsfile
- Use version control for reusable logic

---

## 🧰 Prerequisites

- A second GitHub repo to host your shared library (e.g., `jenkins-shared-lib`)
- Jenkins pipeline job set to load a shared library

---

## 🚀 Shared Library Structure

```
jenkins-shared-lib/
├── vars/
│   └── sayHello.groovy
└── README.md
```

### Example `sayHello.groovy`
```groovy
def call(String name = 'World') {
  echo "Hello, ${name} from a shared library!"
}
```

---

## 🔧 Jenkins Configuration

1. Go to: **Manage Jenkins → Configure System → Global Pipeline Libraries**
2. Add a new library:
   - Name: `myLib`
   - Default version: `main`
   - Retrieval method: **Modern SCM** → Git → Paste Git URL

---

## 📝 Jenkinsfile Example (in another repo)

```groovy
@Library('myLib') _

pipeline {
  agent any
  stages {
    stage('Greet') {
      steps {
        sayHello('DevOps Student')
      }
    }
  }
}
```

---

## ✅ Validation Checklist

- [ ] Jenkinsfile references `@Library`
- [ ] Pipeline uses `sayHello()` from shared lib
- [ ] Library loaded via SCM and works on run

---

## 🧹 Cleanup
- Unregister the library in Jenkins config if not needed

---

## 🧠 Key Concepts

- Shared libraries = DRY pipelines
- Place `groovy` logic in `vars/` or `src/`
- Great for enterprise pipelines with multiple teams

---

## 🔁 What’s Next?
Continue to [LAB08 - Secure Credentials](../LAB08-Secure-Credentials/) to safely pass secrets into Jenkins pipelines.

Reusable logic = reliable automation. 🔁📚

