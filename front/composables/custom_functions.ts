export const deepEqual = (x: any, y: any): boolean => {
  const ok = Object.keys
  const tx = typeof x
  const ty = typeof y
  return x && y && tx === 'object' && tx === ty
    ? ok(x).length === ok(y).length
    && ok(x).every(key => deepEqual(x[key], y[key]))
    : x === y
}
export const seoConfig = (title: string = '', extra: Record<string, any> = {}): Record<string, any> => {
  const { t } = useI18n()
  return {
    title: t(title) + ' | ' + t('app_title'),
    meta: [{ name: 'description', content: t('done') }],
    ...extra,
  }
}
export const checkDateBiggerThanToday = (date: Date | unknown): boolean => {
  const yesterDay = new Date()
  yesterDay.setDate(yesterDay.getDate() - 1)
  if (date instanceof Date)
    return date > yesterDay
  return false
}

export const stringifyDate = (date: Date | string | null): string => {
  if (!date) return ''

  const options: Intl.DateTimeFormatOptions = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }
  return new Date(date).toLocaleDateString('en-US', options)
}
export const stringifyDatetime = (date: Date | string | null): string => {
  if (!date) return ''

  const options: Intl.DateTimeFormatOptions = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: true,
  }
  return new Date(date).toLocaleString('en-US', options)
}

export const getTimeOfDate = (date: Date): string => {
  if (!(date instanceof Date) || isNaN(date.getTime())) {
    throw new Error('Invalid Date object')
  }
  const hours = date.getHours().toString().padStart(2, '0')
  const minutes = date.getMinutes().toString().padStart(2, '0')
  return `${hours}:${minutes}`
}

export const getDateOfDate = (date: Date): string => {
  if (!(date instanceof Date) || isNaN(date.getTime())) {
    throw new Error('Invalid Date object')
  }
  const year = date.getFullYear()
  const month = (date.getMonth() + 1).toString().padStart(2, '0')
  const day = date.getDate().toString().padStart(2, '0')
  return `${year}/${month}/${day}`
}

export const dayDistance = (date_1: Date, date_2: Date = new Date()): number => {
  const date_distance = date_1.getTime() - date_2.getTime()
  return Math.floor(date_distance / 86400000)
}
export const timeAgo = (date: Date): string => {
  const { t } = useI18n()
  const now = new Date()
  const seconds = Math.floor((now.getTime() - date.getTime()) / 1000)

  if (seconds < 60) {
    return t('just_now')
  }

  const minutes = Math.floor(seconds / 60)
  if (minutes < 60) {
    return minutes.toString() + ' ' + t('minutes_ago')
  }

  const hours = Math.floor(minutes / 60)
  if (hours < 24) {
    return hours.toString() + ' ' + t('hours_ago')
  }

  const days = Math.floor(hours / 24)
  if (days < 7) {
    return days.toString() + ' ' + t('days_ago')
  }

  const weeks = Math.floor(days / 7)
  if (weeks < 4) {
    return weeks.toString() + ' ' + t('weeks_ago')
  }

  const months = Math.floor(days / 30)
  if (months < 12) {
    return months.toString() + ' ' + t('months_ago')
  }

  const years = Math.floor(days / 365)
  return years.toString() + ' ' + t('years_ago')
}
export function getPercentColor(percentage: number) {
  if (percentage < 0 || percentage > 100) {
    console.warn('Percentage should be between 0 and 100')
    return 'grey' // Default color for invalid input
  }

  if (percentage >= 90) {
    return 'green darken-2' // Excellent
  }
  else if (percentage >= 70) {
    return 'light-green darken-1' // Good
  }
  else if (percentage >= 50) {
    return 'yellow darken-3' // Average
  }
  else if (percentage >= 30) {
    return 'orange darken-3' // Poor
  }
  else {
    return 'red darken-4' // Very Poor
  }
}
export function downloadJsonFile(data: any, fileName = 'export.json') {
  const json = JSON.stringify(data, null, 2) // Convert data to JSON string
  const blob = new Blob([json], { type: 'application/json' }) // Create a Blob
  const url = URL.createObjectURL(blob) // Create a URL for the Blob

  // Create a temporary anchor element and trigger the download
  const a = document.createElement('a')
  a.href = url
  a.download = fileName
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)

  URL.revokeObjectURL(url) // Clean up the URL object
}
