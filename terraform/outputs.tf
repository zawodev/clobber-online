output "alb_dns" {
  description = "Publiczny DNS Load Balancera"
  value = aws_lb.alb.dns_name
}

output "backend_task_def" {
  value = aws_ecs_task_definition.backend.arn
}
