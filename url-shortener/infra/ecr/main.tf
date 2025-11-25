resource "aws_ecr_repository" "app_repo" {
  name = "url-shortener-app"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name = "url-shortener-app-repo"
  }
}
