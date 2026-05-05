resource "google_cloud_run_v2_service" "backend_service" {
  name                 = "${random_id.default.hex}-backend-service"
  location             = "us-central1"
  deletion_protection  = false
  ingress              = "INGRESS_TRAFFIC_ALL"
  invoker_iam_disabled = true


  scaling {
    max_instance_count = 1
    min_instance_count = 0
  }

  template {
    containers {
      image = "${google_artifact_registry_repository.container_repo.location}-docker.pkg.dev/ankiaicardcreationtoolbox/${google_artifact_registry_repository.container_repo.repository_id}/ankiaicardcreationtoolboxbackend:latest"
      ports {
        container_port = 8080
      }
      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
      }
    }
  }
}

resource "google_cloud_run_v2_service" "frontend_service" {
  name                 = "${random_id.default.hex}-frontend-service"
  location             = "us-central1"
  deletion_protection  = false
  ingress              = "INGRESS_TRAFFIC_ALL"
  invoker_iam_disabled = true

  scaling {
    max_instance_count = 1
    min_instance_count = 0
  }

  template {
    containers {
      image = "${google_artifact_registry_repository.container_repo.location}-docker.pkg.dev/ankiaicardcreationtoolbox/${google_artifact_registry_repository.container_repo.repository_id}/ankiaicardcreationtoolboxfrontend:latest"
      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
      }
    }
  }
}

output "backend_url" {
  value = google_cloud_run_v2_service.backend_service.uri
}

output "frontend_url" {
  value = google_cloud_run_v2_service.frontend_service.uri
}

output "backend_name" {
  value = google_cloud_run_v2_service.backend_service.name
}
output "frontend_name" {
  value = google_cloud_run_v2_service.frontend_service.name
}
