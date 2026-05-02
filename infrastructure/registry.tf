resource "google_artifact_registry_repository" "container_repo" {
  location      = "us-central1"
  repository_id = "${random_id.default.hex}-repository"
  description   = "docker repository"
  format        = "DOCKER"

  # Keep the latest 10 versions per package/image.
  cleanup_policies {
    id     = "keep-latest-10"
    action = "KEEP"
    most_recent_versions {
      keep_count = 10
    }
  }

  docker_config {
    immutable_tags = false
  }
}
