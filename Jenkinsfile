@Library('dst-shared@master') _

dockerBuildPipeline {
        githubPushRepo = "Cray-HPE/hms-mountain-discovery"
  repository = "cray"
  imagePrefix = "hms"
  app = "mountain-discovery"
  name = "cray-hms-mountain-discovery"
  description = "Utility for facilitating mountain discovery without having to run REDS"
  dockerfile = "Dockerfile"
  slackNotification = ["", "", false, false, true, true]
  product = "csm"
}
