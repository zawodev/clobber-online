terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# 1) VPC i subnets (skorzystaj z modułu domyślnego lub istniejącej VPC)
data "aws_vpc" "default" {
  default = true
}
data "aws_subnets" "default" {
  filter { 
    name = "vpc-id"
    values = [data.aws_vpc.default.id] 
  }
}

# 2) ECS Cluster
resource "aws_ecs_cluster" "clobber" {
  name = "${var.project_name}-cluster"
}

# 3) IAM Role for Task Execution
resource "aws_iam_role" "ecs_task_exec" {
  name = "${var.project_name}-ecs-task-exec"
  assume_role_policy = data.aws_iam_policy_document.ecs_task_assume.json
}
data "aws_iam_policy_document" "ecs_task_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}
resource "aws_iam_role_policy_attachment" "ecs_task_policy" {
  role       = aws_iam_role.ecs_task_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# 4) Security Group
resource "aws_security_group" "ecs" {
  name        = "${var.project_name}-sg"
  description = "Allow HTTP"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# 5) Load Balancer + Target Groups + Listener
resource "aws_lb" "alb" {
  name               = "${var.project_name}-alb"
  internal           = false
  load_balancer_type = "application"
  subnets            = data.aws_subnets.default.ids
  security_groups    = [aws_security_group.ecs.id]
}
resource "aws_lb_target_group" "backend_tg" {
  name     = "${var.project_name}-backend-tg"
  port     = var.container_port_backend
  protocol = "HTTP"
  vpc_id   = data.aws_vpc.default.id
}
resource "aws_lb_target_group" "frontend_tg" {
  name     = "${var.project_name}-frontend-tg"
  port     = var.container_port_frontend
  protocol = "HTTP"
  vpc_id   = data.aws_vpc.default.id
}
resource "aws_lb_listener" "front" {
  load_balancer_arn = aws_lb.alb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.frontend_tg.arn
  }
}
# listener rule to route /api to backend
resource "aws_lb_listener_rule" "api" {
  listener_arn = aws_lb_listener.front.arn
  priority     = 100
  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.backend_tg.arn
  }
  condition {
    path_pattern {
      values = ["/api/*","/ws/*"]
    }
  }
}

# 6) ECS Task Definitions
resource "aws_ecs_task_definition" "backend" {
  family                   = "${var.project_name}-backend"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "512"
  memory                   = "1024"
  execution_role_arn       = aws_iam_role.ecs_task_exec.arn

  container_definitions = jsonencode([{
    name      = "backend"
    image     = var.backend_image
    portMappings = [{ containerPort = var.container_port_backend, hostPort = var.container_port_backend }]
    environment = [
      { name = "DEBUG", value = "False" },
      { name = "ALLOWED_HOSTS", value = "*" },
      # inne zmienne .env je wypisz tutaj
    ]
  }])
}

resource "aws_ecs_task_definition" "frontend" {
  family                   = "${var.project_name}-frontend"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "512"
  memory                   = "1024"
  execution_role_arn       = aws_iam_role.ecs_task_exec.arn

  container_definitions = jsonencode([{
    name      = "frontend"
    image     = var.frontend_image
    portMappings = [{ containerPort = var.container_port_frontend, hostPort = var.container_port_frontend }]
    environment = [
      { name = "VUE_APP_API_URL", value = "http://${aws_lb.alb.dns_name}/api/v1/" },
      # inne zmienne .env
    ]
  }])
}

# 7) ECS Services
resource "aws_ecs_service" "backend" {
  name            = "${var.project_name}-backend-svc"
  cluster         = aws_ecs_cluster.clobber.id
  task_definition = aws_ecs_task_definition.backend.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = data.aws_subnets.default.ids
    security_groups = [aws_security_group.ecs.id]
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.backend_tg.arn
    container_name   = "backend"
    container_port   = var.container_port_backend
  }
}

resource "aws_ecs_service" "frontend" {
  name            = "${var.project_name}-frontend-svc"
  cluster         = aws_ecs_cluster.clobber.id
  task_definition = aws_ecs_task_definition.frontend.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = data.aws_subnets.default.ids
    security_groups = [aws_security_group.ecs.id]
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.frontend_tg.arn
    container_name   = "frontend"
    container_port   = var.container_port_frontend
  }
}
