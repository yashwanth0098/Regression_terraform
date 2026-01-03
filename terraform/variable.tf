variable "region" {
  default = "ap-south-1"
}

variable "cluster_name" {
  default = "mlops-eks-cluster"
}

variable "cluster_version" {
  default = "1.29"
}

variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "subnet_ids" {
  description = "Subnet IDs"
  type        = list(string)
}

variable "node_instance_type" {
  default = "t3.small"
}

variable "desired_nodes" {
  default = 2
}
