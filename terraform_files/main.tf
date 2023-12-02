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
resource "okta_group" "group_admin" {
  name = "Group_Admin"
}

resource "okta_group" "group_developer" {
  name = "Group_Developer"
}

resource "okta_group" "group_read_only_user" {
  name = "Group_ReadOnlyUser"
}

resource "okta_group" "group_hr_manager" {
  name = "Group_HRManager"
}

resource "okta_group" "group_finance_team" {
  name = "Group_FinanceTeam"
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
    okta_group.group_admin.id,
    okta_group.group_developer.id,
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
    okta_group.group_read_only_user.id,
  ]
}