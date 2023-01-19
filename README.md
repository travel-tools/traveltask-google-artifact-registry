# Travel Task for Google Artifact Registry

A Travel task to download/upload a Python package from/to Google Artifact Registry using pip

## Upload

To upload a package to Google Artifact Registry using the task, add the following config to a Travel `bag.yml`:

```yml
tasks:
  takeoff:
    instead:
      - task: traveltask_google_artifact_registry
        name: upload-to-some-registry
        config:
          project: <project>
          region: <region>
          repository: <repository>
          action: upload
```

## Installation

To install a package from Google Artifact Registry using the task, add the following config to a Travel `bag.yml`:

```yml
tasks:
  setup:
    pre:
      - task: traveltask_google_artifact_registry
        name: download-from-some-registry
        config:
          project: <project>
          region: <region>
          repository: <repository>
          action: install
          packages: <package>[=<version>]
          
    post:
      - task: traveltask_google_artifact_registry
        name: fix-requirements
        config:
          project: <project>
          region: <region>
          repository: <repository>
          action: fix_requirements
```

**N.B.:** In the above example, the Google Artifact Registry config must match between the stages
