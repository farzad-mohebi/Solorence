export interface Goal {
  id?: number
  title: string
  description?: string
  user?: any
  progress?: number
  updated_at: string
  created_at: string
};
export const GoalDefaultValue: Goal = {
  title: '',
  description: '',
  progress: 0,
  updated_at: '',
  created_at: '',
}

export interface GoalTarget {
  id?: number
  title: string
  description?: string
  user?: any
  progress?: number
  status: number
  deadline_at?: string
  updated_at?: string
  created_at?: string
};
export const GoalTargetDefaultValue: GoalTarget = {
  title: '',
  description: '',
  status: 0,
  progress: 0,
}
