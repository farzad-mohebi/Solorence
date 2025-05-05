export interface Task {
  id?: number
  title: string
  status: number
  due_date: string
  editor_data: any
};
export const TaskDefaultValue: Task = {
  title: '',
  status: 0,
  due_date: '',
  editor_data: '',
}
