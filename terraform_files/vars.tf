variable "okta_api_token" {
  default     = ""
  description = "Okta API token for authentication"
  type        = string
  sensitive   = true
}

variable "okta_org_name" {
  default     = ""
  description = "Okta organization name"
  type        = string
  sensitive   = true
}

variable "okta_org_domain" {
  default     = ""
  description = "orgdomain.okta.com"
  type        = string
  sensitive   = true
}

variable "app_id" {
  default     = ""
  description = "okta client id"
  type        = string
  sensitive   = true
}