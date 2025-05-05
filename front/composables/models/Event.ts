export type EventModel = {
  id: number
  title: string
  description: string
  place: number
  address: string
  note?: number | object
  start_at?: string
  end_at?: string
}
export const EventModelDefaultValue: EventModel = {
  id: 0,
  title: '',
  description: '',
  place: 0,
  address: '',
}

export type CalendarEventModel = {
  title: string
  description?: string
  start: Date
  end: Date
  id: number
  color?: string
  place: number
  address: string
}

export const CalendarEventDefaultValue: CalendarEventModel = {
  id: 0,
  title: '',
  place: 0,
  address: '',
  color: 'green',
  start: new Date(),
  end: new Date(),
}

export type GoogleCalendarMeet = {
  title: string
  link: string
  date: string
  time: string
  duration: string
  googleCalendarData: string
}
