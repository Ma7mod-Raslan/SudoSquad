
module "vpc" {
  source = "./vpc"
}

module "ecr" {
  source = "./ecr"
}

module "ec2" {
  source    = "./ec2"
  subnet_id = module.vpc.public_subnet_id
  sg_id     = module.security.sg_id
}

module "security" {
  source = "./security"
  vpc_id = module.vpc.vpc_id
}