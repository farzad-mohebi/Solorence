export interface Journey {
  id?: number
  title: string
  description: string
  action_at: string
};
export const JourneyDefaultValue: Journey = {
  title: '',
  description: '',
  action_at: '',
}
