@Library('dst-shared@master') _

dockerBuildPipeline {
  repository = "cray"
  imagePrefix = "hms"
  app = "mountain-discovery"
  name = "cray-hms-mountain-discovery"
  description = "Utility for facilitating mountain discovery without having to run REDS"
  dockerfile = "Dockerfile"
  slackNotification = ["", "", false, false, true, true]
  product = "csm"
}
