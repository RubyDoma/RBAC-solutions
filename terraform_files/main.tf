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

# Create Okta Groups
resource "okta_group" "admin" {
  name = "Admin"
}

resource "okta_group" "developer" {
  name = "Developer"
}

resource "okta_group" "read_only_user" {
  name = "ReadOnlyUser"
}

resource "okta_group" "hr_manager" {
  name = "HRManager"
}

resource "okta_group" "finance_team" {
  name = "FinanceTeam"
}

# Map Users to Okta Groups
resource "okta_user" "user1" {
  first_name = ""
  last_name  = ""
  login      = "test@example.com"
  email      = "test@example.com"
}

resource "okta_user_group_memberships" "user1" {
  user_id = okta_user.user1.id
  groups = [
    okta_group.admin.id,
    okta_group.developer.id,
  ]
}


resource "okta_user" "user2" {
  first_name = ""
  last_name  = ""
  login      = "test2@example.com"
  email      = "test2@example.com"
}

resource "okta_user_group_memberships" "user2" {
  user_id = okta_user.user2.id
  groups = [
    okta_group.read_only_user.id,
  ]
}