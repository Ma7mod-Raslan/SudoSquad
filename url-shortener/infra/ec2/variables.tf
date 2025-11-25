variable "subnet_id" {
  type = string
}

variable "sg_id" {
  type = string
}

variable "instance_type" {
  type = string
  default = "t3.micro"
}