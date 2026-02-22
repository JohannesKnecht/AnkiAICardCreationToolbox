resource "google_artifact_registry_repository" "container_repo" {
  location      = "us-central1"
  repository_id = "${random_id.default.hex}-repository"
  description   = "docker repository"
  format        = "DOCKER"

  docker_config {
    immutable_tags = true
  }
}
