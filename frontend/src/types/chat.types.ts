export interface ChatListParticipantDTO {
  account_id: number
  username: string
  first_name: string
  last_name: string
  phone_number: string
  avatar_url?: string | null
}

export interface ChatListDTO {
  chat_id: number
  created_at?: string | null
  participants: ChatListParticipantDTO[]
  last_message?: string | null
  last_message_created_at?: string | null
}

export interface ChatMessagesDTO {
  message_id: number
  chat_id: number
  sender_id: number
  created_at?: string | null
  updated_at?: string | null
  message_text?: string | null
}
