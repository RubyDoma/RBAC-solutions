terraform {
  required_providers {
    okta = {
      source  = "okta/okta"
      version = "~> 4.6.2"
    }
  }
}

provider "okta" {
  org_name  = var.okta_org_domain
  api_token = var.okta_api_token
}

data "okta_users" "all_users" {}

data "okta_groups" "all_groups" {}

data "okta_roles" "all_roles" {
}

output "users" {
  value = data.okta_users.all_users.users
}

output "groups" {
  value = data.okta_groups.all_groups.groups
}

resource "null_resource" "create_user" {
  triggers = {
    okta_user_roles = jsonencode(data.okta_roles.all_roles.names)
  }

  provisioner "local-exec" {
    command = <<EOT
      curl -X POST \
        -H "Authorization: SSWS ${var.okta_api_token}" \
        -H "Content-Type: application/json" \
        -H "Accept: application/json" \
        -d '{
          "profile": {
            "firstName": "",
            "lastName": "",
            "email": "",
            "login": ""
          },
          "credentials": {
            "password": {
              "value": "temporary_password"
            }
          }
        }' \
        https://${var.okta_org_name}.okta.com/api/v1/users > user_response.json
    EOT
  }
}

resource "okta_user_roles" "user_roles" {
  depends_on = [null_resource.create_user]

  user_id = jsondecode(file("user_response.json")).id

  roles = [
    "Admin",
    "Developer",
    "ReadOnlyUser",
    "HRManager",
    "FinanceTeam"
  ]
}

resource "okta_group_role" "USER_ADMIN" {
  group_id  = ""
  role_type = "Admin"
}

resource "okta_group_role" "USER" {
  group_id  = ""
  role_type = "Developer"
}

resource "okta_group_role" "READ_ONLY" {
  group_id  = ""
  role_type = "ReadOnlyUser"
}

resource "okta_group_role" "READ_ONLY" {
  group_id  = ""
  role_type = "HRManager"
}

resource "okta_group_role" "READ_ONLY" {
  group_id  = ""
  role_type = "FinanceTeam"
}