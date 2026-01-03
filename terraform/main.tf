provider "aws" {
  region = var.region
}

# -------------------
# ECR Repository
# -------------------
resource "aws_ecr_repository" "ml_repo" {
  name = "house-price-mlops"
}

# -------------------
# EKS Cluster
# -------------------
module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = var.cluster_name
  cluster_version = var.cluster_version

  vpc_id     = var.vpc_id
  subnet_ids = var.subnet_ids

  eks_managed_node_groups = {
    default = {
      desired_size   = var.desired_nodes
      instance_types = [var.node_instance_type]
    }
  }
}
