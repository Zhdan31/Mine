terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "eu-central-1"
  access_key = "AKIAYRGW4GCELXDMMP4B"
  secret_key = "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"
}

// To Generate Private Key
resource "tls_private_key" "rsa_2048" {
  algorithm = "RSA"
  rsa_bits  = 2048
}

variable "key_name" {
  description = "Name of the SSH key pair"
}

// Create Key Pair for Connecting EC2 via SSH
resource "aws_key_pair" "key_pair" {
  key_name   = var.key_name
  public_key = tls_private_key.rsa_2048.public_key_openssh
}

// Save PEM file locally
resource "local_file" "private_key" {
  content  = tls_private_key.rsa_2048.private_key_pem
  filename = var.key_name
}

# Create a security group
resource "aws_security_group" "sg_ec2" {
  name        = "sg_ec2"
  description = "Security group for EC2"

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

resource "aws_instance" "borse_instance" {
  ami                    = "ami-0faab6bdbac9486fb"
  instance_type          = "t3.small" #t2.micro
  key_name               = aws_key_pair.key_pair.key_name
  vpc_security_group_ids = [aws_security_group.sg_ec2.id]

  tags = {
    Name = "borse_instance"
  }
  
  timeouts {
    create = "7m"
  }
 
  root_block_device {
    volume_size = 10
    volume_type = "gp2"
  }

  provisioner "remote-exec" {
    inline = [
      "sudo apt-get update",
      "sudo apt-get install -y docker.io",
      "sudo usermod -aG docker $USER",
    ]
    
    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file(var.key_name)
      host        = aws_instance.borse_instance.public_ip
      timeout = "2m"
    }
  }
  #seconda connection per evitare i problemi dovuti all'utenza
  provisioner "remote-exec" {
    inline = [
      "sudo service docker restart",
      "sudo systemctl daemon-reload",
      "sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose",
      "sudo chmod +x /usr/local/bin/docker-compose",
      "sudo systemctl daemon-reload",
      "git clone https://github.com/saleor/saleor-platform.git",
      "cd saleor-platform/",
      "docker-compose build",
      "docker-compose run --rm api python3 manage.py migrate",
      "docker-compose run --rm api python3 manage.py populatedb --createsuperuser",
      "docker-compose up -d"
    ]

    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file(var.key_name)
      host        = aws_instance.borse_instance.public_ip
      timeout = "3m"
    }
  }
}
