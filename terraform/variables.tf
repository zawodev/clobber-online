variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Prefix dla wszystkich zasobów"
  type        = string
  default     = "clobber"
}

variable "backend_image" {
  description = "ECR URI obrazu backend"
  type        = string
}

variable "frontend_image" {
  description = "ECR URI obrazu frontend"
  type        = string
}

variable "container_port_backend" {
  type    = number
  default = 8000
}

variable "container_port_frontend" {
  type    = number
  default = 8080
}
