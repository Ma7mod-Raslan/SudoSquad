output "ec2_public_ip" {
  value = module.ec2.ec2_public_ip
}

output "app_repo_url" {
  value = module.ecr.app_repo_url
}
