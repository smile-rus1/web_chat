export interface Account {
  account_id: number
  username: string
  first_name: string
  last_name: string
  phone_number: string
  email: string
  is_admin: boolean
  is_superuser: boolean
  image_url?: string
}
