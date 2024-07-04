# conan-azure-templates

### This repository contains everything to build & upload conan packages in a Azure DevOps pipeline



### Azure pipeline using Microsoft-hosted VM images

The files `buildConanRecipe.yml`, `uploadConanRecipe.py` can be loaded into a Azure pipeline to build and upload conan packages on the [Microsoft-hosted VM images](https://learn.microsoft.com/en-us/azure/devops/pipelines/agents/hosted?view=azure-devops&tabs=yaml#software) like so:

```yml
# Clone this repository to access the template files buildConanRecipe.yml, uploadConanRecipe.py
resources:
  repositories:
    - repository: templates
      type: github
      name: Tereius/conan-azure-templates
      ref: master
      endpoint: Tereius

jobs:
    # A conan build job
  - job: build_sth
    pool:
      vmImage: "ubuntu-latest" # Pick a VM image https://learn.microsoft.com/en-us/azure/devops/pipelines/agents/hosted?view=azure-devops&tabs=yaml#software
    timeoutInMinutes: 20 # Pick a sensible timeout for the build job
    steps:
      - template: buildConanRecipe.yml@templates # Apply the buildConanRecipe.yml template
        parameters:
          conanEnv: # Provide conan parameter via env variables
            CONAN_REMOTES: "https://conan.privatehive.de/artifactory/api/conan/public-conan",

    # A conan upload job
  - job: upload_recipe
    dependsOn:
      - build_sth # Wait for the upload until the build job finished
    condition: and(succeeded(), in(variables['Build.Reason'], 'IndividualCI', 'BatchedCI'))
    pool:
      vmImage: "ubuntu-latest" # Pick the ubuntu-latest image for the upload job
    steps:
      - template: uploadConanRecipe.yml@templates # Apply the uploadConanRecipe.yml template
        parameters:
          conanEnv: # Provide conan parameter via env variables
            CONAN_UPLOAD: "https://conan.privatehive.de/artifactory/api/conan/public-conan",
            CONAN_LOGIN_USERNAME: "ci",
            CONAN_PASSWORD: "$(secret)", # Provide the credentials via a secret pipeline variable
```

The following conan parameter can be provided to the build/upload jobs:

|Name|Description|Mandatory|
|-|-|-|
|CONAN_HOST_PROFILE_PATH|An absolute or relative path pointing to a conan profile that will be used as the host profile|-|
|CONAN_RECIPE_PATH|An absolute or relative path that points to the folder in which the conanfile.py file is located|-|
|CONAN_REMOTES|A list separated by `,` of conan remote urls where conan packages will be downloaded from|-|
|CONAN_OPTIONS|A list separated by `,` of conan options|-|
|CONAN_UPLOAD|The url of the conan remote where the recipe will be uploaded to|in the upload job|
|CONAN_LOGIN_USERNAME|The login username for the remotes declared in CONAN_REMOTES and CONAN_UPLOAD|-|
|CONAN_PASSWORD|The login password for the remotes declared in CONAN_REMOTES and CONAN_UPLOAD|-|

### Azure pipeline using Docker Images

In contrast to the Microsoft-hosted VM images you may want to build the conan package in a Docker Container 
